#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""
@File    :   main.py
@Time    :   23.11.11
@Author  :   DrakHorse
@Version :   0.4.0a
@Contact :   https://github.com/DrakHorse
@License :   GNU GENERAL PUBLIC LICENSE
"""
import datetime
import json
import os.path
import sys
import threading
import time
from webbrowser import open as web_open
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import (QLabel, QHeaderView, QAction, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
                             QWidget, QApplication, QAbstractItemView, QFileDialog)
import kvkapi
from pages import library, knowledgePreview, edit, exam, examReport
from qfluentwidgets import (NavigationItemPosition, isDarkTheme, FluentIcon, NavigationBar, FluentTitleBar, ProgressBar,
                            setThemeColor, FlowLayout, PillPushButton, RoundMenu, setTheme, Theme,
                            PopUpAniStackedWidget, Action, InfoBar, InfoBarPosition, MessageBox, FluentTranslator,
                            MessageBoxBase, SubtitleLabel)
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow


class Widget(QWidget):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class AcrylicWindow(BackgroundAnimationWidget, FramelessWindow):
    """ Win11亚克力效果窗口 """

    def __init__(self, parent=None):
        self._isMicaEnabled = False
        super().__init__(parent=parent)

        # enable mica effect on win11
        self.setMicaEffectEnabled(True)

    def setMicaEffectEnabled(self, isEnabled: bool):
        """ 启用亚克力效果 """
        if sys.platform != 'win32' or sys.getwindowsversion().build < 22000:
            return

        self._isMicaEnabled = isEnabled

        if isEnabled:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self._normalBackgroundColor())

    def isMicaEffectEnabled(self):
        return self._isMicaEnabled


class MainWindow(AcrylicWindow):
    """Qt窗口主类"""
    lock = False

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        """初始化UI"""

        # 初始化窗口
        self.setTitleBar(FluentTitleBar(self))
        self.titleBar.raise_()

        self.setWindowTitle('Key-Value Knowledge')
        self.setGeometry(100, 100, 1000, 650)

        # 初始化布局
        self.layout = QHBoxLayout(self)
        self.navigationBar = NavigationBar(self)
        self.stackWidget = PopUpAniStackedWidget(self)

        self.layout.addWidget(self.navigationBar)
        self.layout.addWidget(self.stackWidget)

        self.navigationBar.setMaximumWidth(80)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 50, 0, 0)

        self.stackWidget.setStyleSheet(  # 设置亮色主题Qss
            "#stack{background: rgba(253,253,253,150);"
            "border-top-left-radius: 8px;"
            "border: 1px solid rgba(200,200,200,100)}") if not isDarkTheme() \
            else self.stackWidget.setStyleSheet(  # 设置暗色主题Qss
            "#stack{background: rgba(15,15,15,150);"
            "border-top-left-radius: 8px;"
            "border: 1px solid rgba(200,200,200,100)}")
        self.stackWidget.setObjectName("stack")

        # 初始化页面
        self.initPages()

        # 初始化侧边导航栏
        self.initNavigationBar()

    def setCurrentPage(self, widget):
        """设置当前页面"""
        if not self.lock:
            self.stackWidget.setCurrentWidget(widget)
            widget.reinit()
        else:
            self.navigationBar.setCurrentItem(self.pageLibrary.objectName())
            InfoBar.error(
                title='禁止切出',
                content="测试完毕后即可切换页面",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )

    def initNavigationBar(self):
        """初始化侧边导航栏"""
        # 库按钮
        self.stackWidget.addWidget(self.pageLibrary)
        self.navigationBar.addItem(
            routeKey=self.pageLibrary.objectName(),
            icon=FluentIcon.IOT,
            text="仓库",
            onClick=lambda: self.setCurrentPage(self.pageLibrary),
            position=NavigationItemPosition.TOP,
        )

        # 新建
        self.stackWidget.addWidget(self.pageAddFile)
        self.navigationBar.addItem(
            routeKey=self.pageAddFile.objectName(),
            icon=FluentIcon.ADD_TO,
            text="添加",
            onClick=lambda: self.setCurrentPage(self.pageAddFile),
            position=NavigationItemPosition.TOP,
        )

        # 关于
        self.navigationBar.addItem(
            routeKey="About",
            icon=FluentIcon.HELP,
            text="关于",
            onClick=lambda: web_open("https://github.com/BirchFst/KVKnowledge/"),
            position=NavigationItemPosition.BOTTOM,
            selectable=False,
        )

        self.stackWidget.addWidget(self.pageKnowledgePreview)
        self.stackWidget.addWidget(self.pageExam)
        self.stackWidget.addWidget(self.pageExamReport)

        self.navigationBar.setCurrentItem(self.pageLibrary.objectName())

    def initPages(self):
        self.pageLibrary = PageLibrary(self.stackWidget)
        self.pageKnowledgePreview = PageKnowledgePreview(self.stackWidget)
        self.pageAddFile = PageEdit(self.stackWidget)
        self.pageExam = PageExam(self.stackWidget)
        self.pageExamReport = PageExamReport(self.stackWidget)


class PageLibrary(QWidget, library.Ui_PageLibrary):
    """库页面Widget"""

    sortOrder = 0x00
    sortOrderOptions = {
        0x00: ["创建日期", FluentIcon.DATE_TIME.icon],
        0x01: ["创建日期(倒序)", FluentIcon.DATE_TIME.icon],
        0x02: ["名称 A-Z", FluentIcon.TAG.icon],
        0x03: ["名称 Z-A", FluentIcon.TAG.icon],
        0x04: ["掌握程度", FluentIcon.MARKET.icon],
        0x05: ["掌握程度(倒叙)", FluentIcon.MARKET.icon],
    }

    filterOrder = None

    # TODO 更改拟定数据
    tags = [
        "历史",
        "数学",
        "物理",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化UI
        self.setupUi(self)
        self.initUI()
        self.initWidgets()

        # 初始化数据
        self.initLibrary()

    def callBackSortOptions(self, index):
        """
        排序方式更改时的回调函数
        """
        self.sortOrder = index
        self.sortSelector.setIcon(self.sortOrderOptions[self.sortOrder][1]())
        self.sortSelector.setText(self.sortOrderOptions[self.sortOrder][0])

        self.initLibrary()

    def callBackFilterOptions(self, tag):
        """
        筛选方式更改时的回调函数
        """
        self.filterOrder = tag
        self.filterSelector.setText(tag)

        self.initLibrary()

    def callBackEnterKnowledge(self, item):
        self.parent().parent().stackWidget.setCurrentWidget(self.parent().parent().pageKnowledgePreview)  # noqa
        self.parent().parent().pageKnowledgePreview.initData(self.data[item.row()])  # noqa

    def initWidgets(self):
        """初始化控件功能"""

        # 设置下拉框控件
        self.sortSelector.setIcon(FluentIcon.SCROLL.icon())
        self.sortSelectorMenu = RoundMenu()
        for a in self.sortOrderOptions.keys():
            # 添加菜单项并绑定事件
            action = QAction(self.sortOrderOptions[a][1](), self.sortOrderOptions[a][0])
            exec(f"action.triggered.connect(lambda :self.callBackSortOptions({a}))", locals(), locals())  # noqa

            self.sortSelectorMenu.addAction(action)

        self.sortSelector.setMenu(self.sortSelectorMenu)

        # 筛选下拉框
        self.filterSelector.setIcon(FluentIcon.FILTER.icon())
        self.filterSelectorMenu = RoundMenu()

        for tag in self.tags:
            action = QAction(FluentIcon.TAG.icon(), tag)
            exec(f"action.triggered.connect(lambda :self.callBackFilterOptions(\"{tag}\"))", locals(), locals())  # noqa

            self.filterSelectorMenu.addAction(action)

        self.filterSelector.setMenu(self.filterSelectorMenu)

    def initUI(self):
        """初始化UI"""

        # 设置表格边框
        self.knowledgeTable.setBorderVisible(True)
        self.knowledgeTable.setBorderRadius(8)

        # 设置表格布局
        self.knowledgeTable.setColumnCount(4)
        self.knowledgeTable.setHorizontalHeaderLabels(["知识", "日期", "标签", "掌握"])
        self.knowledgeTable.verticalHeader().hide()

        # 设置表格列宽
        self.knowledgeTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.knowledgeTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.knowledgeTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.knowledgeTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.knowledgeTable.horizontalHeader().setMinimumSectionSize(200)

        self.knowledgeTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 设置表格点击回调
        self.knowledgeTable.itemClicked.connect(self.callBackEnterKnowledge)

        # 顶层控件
        self.addKnowledge.setIcon(FluentIcon.ADD)

    def sortByDate(self, reverse=False):
        """
        根据日期排序列表数据
        """
        self.data = sorted(self.data, key=lambda x: x[2], reverse=reverse)

    def sortByName(self, reverse=False):
        """
        根据知识点名称排序列表数据
        """
        self.data = sorted(self.data, key=lambda x: ''.join(map(lambda c: str(ord(c)), x[1])), reverse=reverse)

    def sortByMastery(self, reverse=False):
        """
        根据掌握程度排序列表数据
        """
        self.data = sorted(self.data, key=lambda x: x[-1], reverse=reverse)

    def filterByTag(self):
        """
        根据标签筛选列表数据
        """
        self.data = list(filter(lambda x: self.filterOrder in x[3], self.data))

    def initLibrary(self):
        """初始化仓库信息"""

        # 获取知识点数据
        self.data = kvkapi.getKnowledgeData()

        # 筛选数据
        self.filterByTag() if self.filterOrder is not None else None

        # 排序数据
        if self.sortOrder == 0x00 or self.sortOrder == 0x01:
            self.sortByDate(self.sortOrder == 0x01)
        elif self.sortOrder == 0x02 or self.sortOrder == 0x03:
            self.sortByName(self.sortOrder == 0x03)
        elif self.sortOrder == 0x04 or self.sortOrder == 0x05:
            self.sortByMastery(self.sortOrder == 0x05)

        self.knowledgeTable.setRowCount(len(self.data))
        # 填充表格
        for r in range(len(self.data)):
            row = self.data[r]
            # 设置第一列知识点名称
            self.knowledgeTable.setItem(r, 0, QTableWidgetItem(row[1]))

            # 设置第二列知识点日期
            item = QTableWidgetItem(row[2])
            item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.knowledgeTable.setItem(r, 1, item)

            # 设置第三列知识点标签
            itemWidget = QWidget()
            itemWidget.setFixedHeight(50)
            itemLayout = FlowLayout()
            tags = row[3]
            for tag in tags:
                item = PillPushButton(tag, itemWidget, FluentIcon.TAG)
                item.setCheckable(False)
                item.setFixedHeight(30)
                itemLayout.addWidget(item)

            itemWidget.setLayout(itemLayout)
            self.knowledgeTable.setCellWidget(r, 2, itemWidget)

            # 设置第三列知识点掌握程度
            itemLayout = QVBoxLayout()
            itemLayout.setSpacing(5)
            itemLayout.setContentsMargins(18, 18, 18, 18)

            item = QLabel(str(int(row[4] * 100)) + "%")
            item.setStyleSheet("font-family: SIMHEI;font-size: 13px;color: black;") if not isDarkTheme() \
                else item.setStyleSheet("font-family: SIMHEI;font-size: 13px;color: white;")
            item.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            itemLayout.addWidget(item)

            item = ProgressBar(self)

            item.setMaximumWidth(160)
            item.setFixedHeight(5)
            item.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            item.setValue(int(row[4] * 100))
            itemLayout.addWidget(item)

            itemWidget = QWidget()
            itemWidget.setLayout(itemLayout)

            self.knowledgeTable.setCellWidget(r, 3, itemWidget)

    def reinit(self):
        self.initLibrary()

        # 刷新2次保证界面不错乱(某种玄学Bug导致)
        self.parent().setCurrentIndex(1)
        self.parent().setCurrentIndex(0)
        self.parent().setCurrentIndex(1)
        self.parent().setCurrentIndex(0)


class PageKnowledgePreview(QWidget, knowledgePreview.Ui_PageKnowledgePreview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        self.visibleToggleButton.setIcon(FluentIcon.HIDE)

        self.SingleDirectionScrollArea.smoothScroll.orient = Qt.Horizontal

        # 绑定按钮事件
        self.listenButton.clicked.connect(self.TTSOutput)
        self.examButton.clicked.connect(lambda: self.parent().parent().setCurrentPage(self.parent().parent().pageExam))

    def TTSOutput(self):
        """TTS: 导出音频"""
        path = QFileDialog.getSaveFileName(self, "选择音频保存的路径", self.knowledgeTitle.text(), "MP3音频(*.mp3)")
        kvkapi.textToSpeech(
            "知识点," + self.jsonData["name"] + "。" + ";".join(
                [i["key"] + ": " + i["value"] for i in self.jsonData["knowledge_points"]]),
            path[0],
        )

    def initData(self, data):
        """初始化数据"""
        self.jsonData = json.loads(open(os.path.join('.\\knowledge\\', data[0]), "r", encoding="utf-8").read())
        kv_points_length = 0
        for i in self.jsonData["knowledge_points"]:
            kv_points_length += 1 if i["type"] == "kv" else None

        self.knowledgeTitle.setText(data[1])
        self.masteryRing.setValue(int(data[4] * 100))
        self.knowledgeInfoTitle.setText(
            f"{kv_points_length}个知识块   上次复习{self.format_time(self.jsonData['last_review_time'])}")

        self.mainWidget.reinitData(self.jsonData)

    @staticmethod
    def format_time(timestamp):
        now = datetime.datetime.now()
        target = datetime.datetime.fromtimestamp(timestamp)
        diff = now - target

        if diff.days < 7:
            return f"{diff.days}天前"
        elif diff.days < 21:
            return f"{diff.days // 7}周前"
        else:
            return target.strftime("%d/%m/%y")


class PageEdit(QWidget, edit.Ui_PageEdit):
    # 初始化数据
    data = {
        "name": "新的专题",
        "tags": [],
        "created_time": time.time(),
        "last_review_time": time.time(),
        "mastery_level": 0.0,
        "knowledge_points": []
    }

    saved = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUI()

    def reinit(self):
        """重初始化"""
        if self.saved:
            self.knowledgeTitle.setText("新的专题")
            self.data = {
                "name": "新的专题",
                "tags": [],
                "created_time": time.time(),
                "last_review_time": time.time(),
                "mastery_level": 0.0,
                "knowledge_points": []
            }

            self.saved = False
            self.mainWidget.updateDataFromParent(self.data)
            self.mainWidget.reinitLayout()

    def saveTitleData(self):
        """保存标题数据"""
        self.data["name"] = self.knowledgeTitle.text()
        self.saved = False

    def initUI(self):
        """初始化UI"""
        self.knowledgeTitle.setText("新的专题")
        self.knowledgeTitle.editingFinished.connect(self.saveTitleData)

        # 初始化工具栏
        self.commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 添加工具栏工具项
        self.commandBar.addAction(Action(FluentIcon.ADD_TO, "添加块", triggered=self.addBlock))
        self.commandBar.addAction(Action(FluentIcon.UP, "向前放置", triggered=lambda: self.moveBlock(True)))
        self.commandBar.addAction(Action(FluentIcon.DOWN, "向后放置", triggered=lambda: self.moveBlock(False)))
        self.commandBar.addAction(Action(FluentIcon.DELETE, "删除块", triggered=self.deleteBlock))
        self.commandBar.addAction(Action(FluentIcon.SAVE, "保存", triggered=self.saveData))
        self.commandBar.addAction(Action(FluentIcon.TAG, "标签", triggered=self.setTags))
        self.commandBar.addAction(Action(FluentIcon.ADD, "新建知识页", triggered=self.newData))

        # 绑定滚轮横向移动
        self.SingleDirectionScrollArea.smoothScroll.orient = Qt.Horizontal

        # 设置QSS
        self.knowledgeTitle.setStyleSheet(
            "background: rgba(0,0,0,0);border: 0;font-size: 29px;color: #FFFFFF") if isDarkTheme() else self.knowledgeTitle.setStyleSheet(
            "background: rgba(0,0,0,0);border: 0;font-size: 29px;color: #000000")
        self.saved = False

    def moveBlock(self, forward: True):
        """移动数据块将其调换顺序"""
        self.saved = False

        try:
            # 尝试获取行和列
            index = self.focusWidget().parent().index

            # 选中卡片保存内容
            w = self.focusWidget()
            w.parent().saveCardData()

            # 禁止首项前移或尾项后移
            if not index and forward or index == len(self.data["knowledge_points"]) - 1 and not forward:
                return

            # 交换数据顺序
            if forward:
                self.data["knowledge_points"][index], self.data["knowledge_points"][index - 1] = \
                    self.data["knowledge_points"][index - 1], self.data["knowledge_points"][index]
            else:
                self.data["knowledge_points"][index], self.data["knowledge_points"][index + 1] = \
                    self.data["knowledge_points"][index + 1], self.data["knowledge_points"][index]

            self.mainWidget.updateDataFromParent(self.data)

        except AttributeError:
            pass

    def deleteBlock(self):
        """删除选中的数据块"""
        self.saved = False

        try:
            # 尝试获取行和列
            index = self.focusWidget().parent().index

            # 删除并更新数据
            del self.data["knowledge_points"][index]
            self.mainWidget.updateDataFromParent(self.data)

        except AttributeError:
            pass

    def addBlock(self):
        """添加块"""
        self.saved = False

        try:
            self.focusWidget().parent().saveCardData()
        except AttributeError:
            pass

        # 更新数据
        self.data["knowledge_points"].append({
            "type": "kv",
            "key": "关键线索",
            "value": "",
        })

        # 更新UI
        self.mainWidget.addData(self.data)

    def saveData(self):
        """保存数据"""

        # 保存当前知识块数据
        try:
            self.focusWidget().parent().saveCardData()
        except AttributeError:
            pass

        # 打开文件
        with open(f".\\knowledge\\{self.data['created_time']}.kvk", "w", encoding="utf-8") as file:
            file.write(json.dumps(self.data))
            file.close()

        self.saved = True

        # 显示保存成功消息
        InfoBar.success(
            title='保存成功',
            content="切换页面后将退出本知识页编辑器，可在仓库中找到该知识页以修改",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    def newData(self):
        """新建知识页"""
        if not self.saved:
            if MessageBox("当前知识页未保存", "新建将丢弃当前未保存的知识页，确定操作吗", self).exec():
                self.saved = True
                self.reinit()
                InfoBar.success(
                    title='新建完成',
                    content="未保存的知识页已被清除",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
            else:
                return
        else:
            self.saved = True
            self.reinit()
            InfoBar.success(
                title='新建完成',
                content="原数据已保存至仓库",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )

    def setTags(self):
        """设置标签"""
        w = PageEditSetTagsBox(self, self.data["tags"])
        e = w.exec_()
        print(e)
        if e is not None:
            self.data["tags"] = e
        print(self.data["tags"])


class PageEditSetTagsBox(MessageBoxBase):
    """ Custom message box """
    data = []
    tags = ["语文", "数学", "英语", "物理", "地理", "生物", "政治", "历史", "Python"]

    def __init__(self, parent, data):
        super().__init__(parent)

        # 设置数据
        self.data = data.copy()

        # 初始化控件

        self.titleLabel = SubtitleLabel('在下方选中标签', self)

        self.flowWidget = QWidget(self)
        self.flowLayout = FlowLayout(self.flowWidget)

        # 在布局中添加控件
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.flowWidget)

        for tag in self.tags:
            tagButton = PillPushButton(self.flowWidget)
            tagButton.setText(tag)
            tagButton.setChecked(True) if tag in self.data else None

            exec(f"tagButton.clicked.connect(lambda: self.clickedEvent('{tag}'))", locals(), locals())
            self.flowLayout.addWidget(tagButton)

        self.yesButton.setText("确定")
        self.cancelButton.setText("取消")

        self.widget.setMinimumWidth(350)

    def clickedEvent(self, text):
        """选中标签事件"""
        self.data.remove(text) if text in self.data else self.data.append(text)

    def exec_(self):
        if super().exec_():
            return self.data


class PageExam(QWidget, exam.Ui_PageExam):
    answerEditFrameMaxHeight = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        self.answerEdit.setMaximumHeight(100)
        self.answerEdit.textChanged.connect(self.updateAnswerEditFrameHeight)

        self.enterButton.clicked.connect(self.callBackEnterButton)

    def startExam(self):
        """开始测试"""
        # 锁定页面
        self.parent().parent().lock = True

        # 获取数据
        self.data = self.parent().parent().pageKnowledgePreview.jsonData

        # 获取数据中信息
        self.no_question = len(self.data["knowledge_points"]) - 1  # 总题数
        self.current_question = 0  # 当前题数
        self.current_step = 0  # 当前步骤

        self.titleLabel.setText(self.data["name"])

        # 设置数据
        self.report = dict(
            start_time=time.time(),
            no_wrong=0,
            wrong_questions=[],
            no_all=len(self.data["knowledge_points"])
        )

        # 测试
        self.toExam(self.data["knowledge_points"][self.current_question])

    def toExam(self, question):
        """测试某题"""

        self.current_step = 0

        self.progressLabel.setText(f"进度 {self.current_question + 1}/{self.no_question + 1}")
        self.progressBar.setValue(int((self.current_question + 1) / (self.no_question + 1) * 100))
        self.answerEdit.clear()

        self.questionLabel.setText(question["key"])

    def finish(self):
        """完成测试"""
        # 解锁页面
        self.parent().parent().lock = False

        # 修改数据
        self.report["end_time"] = time.time()

        # 重新设置UI
        self.parent().parent().setCurrentPage(self.parent().parent().pageExamReport)
        self.parent().parent().pageExamReport.initData(self.report)

    def callBackEnterButton(self):
        """提交按钮回调"""
        if not self.current_step:
            # 步骤为0时按钮为批改
            self.progressLabel.setText("AI 批改中...")
            threading.Thread(target=self.correcting).start()
        else:
            # 检测测试进程完毕
            if self.current_question == self.no_question:
                self.finish()
                return

            # 按钮为下一题
            self.current_question += 1

            # 重新设置UI
            self.progressLabel.setStyleSheet("color: #FFFFFF") if isDarkTheme() else self.progressLabel.setStyleSheet(
                "color: #000000")
            self.enterButton.setText("提交")

            self.toExam(self.data["knowledge_points"][self.current_question])

    def correcting(self):
        try:
            # 获取数据
            c_json = json.loads(kvkapi.sd_correct(self.data['knowledge_points'][self.current_question]['key'],
                                                  self.data['knowledge_points'][self.current_question]['value'],
                                                  self.answerEdit.toPlainText()))

            c = "正确" if c_json["result"] else "错误"

            # 记录错误题目
            self.report["no_wrong"] += 1 if not c_json["result"] else self.report["no_wrong"]
            self.report["wrong_questions"].append(self.current_question) if not c_json["result"] else None

            # 更新UI显示数据
            self.progressLabel.setStyleSheet("color: green") if c_json["result"] else self.progressLabel.setStyleSheet(
                "color: red")
            self.progressLabel.setText(f"正确答案: {self.data['knowledge_points'][self.current_question]['value']}\n"
                                       f"AI 批改: {c} \n"
                                       f"AI 见解: {c_json['describe']}")
        except json.decoder.JSONDecodeError:
            self.progressLabel.setText(f"正确答案: {self.data['knowledge_points'][self.current_question]['value']}\n"
                                       f"AI 批改失败， 请自行批阅")

        self.enterButton.setText("继续测试")
        self.current_step = 1

        return

    def updateAnswerEditFrameHeight(self):
        """更新回答框的高度"""
        if self.answerEditFrameMaxHeight > self.answerEdit.document().size().height() > 100:
            self.answerEdit.setMaximumHeight(int(self.answerEdit.document().size().height()))
        elif self.answerEditFrameMaxHeight < self.answerEdit.document().size().height():
            self.answerEdit.setMaximumHeight(self.answerEditFrameMaxHeight)
        else:
            self.answerEdit.setMaximumHeight(100)

    def reinit(self):
        # 开始测试
        self.startExam()


class PageExamReport(QWidget, examReport.Ui_PageExamReport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        """初始化UI"""

    def reinit(self):
        """重初始化"""

    def initData(self, data):
        """初始化数据并展示"""
        self.nOKnoeledgeLabel.setText(str(data["no_all"]))
        self.timeLabel.setText(f'{int(data["end_time"] - data["start_time"])} 秒')
        self.missingLabel.setText(f'{data["no_wrong"]} 个块')

        self.progressRing.setValue(int((data["no_all"] - data["no_wrong"]) / data["no_all"] * 100))
        self.returnButton.clicked.connect(
            lambda: self.parent().parent().setCurrentPage(self.parent().parent().pageLibrary))


def setHighDpi():
    """自适应高Dpi缩放"""
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)


if __name__ == '__main__':
    # 设置主题颜色
    setThemeColor("#0078D4")
    setTheme(Theme.AUTO)

    # 适应Dpi
    setHighDpi()

    # 实例化
    app = QApplication(sys.argv)

    # 设置语言
    locale = QLocale()
    translator = FluentTranslator(locale)
    app.installTranslator(translator)

    # 运行
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()
