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
import getpass
import time
from webbrowser import open as web_open
import pyperclip
from PyQt5.QtCore import Qt, QLocale, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QLabel, QHeaderView, QAction, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
                             QWidget, QApplication, QAbstractItemView, QFileDialog)
import kvkapi
import pwidgets
from pages import library, knowledgeReview, edit, test, testReport, home
from qfluentwidgets import (NavigationItemPosition, isDarkTheme, FluentIcon, NavigationBar, FluentTitleBar, ProgressBar,
                            setThemeColor, FlowLayout, PillPushButton, RoundMenu, setTheme, Theme,
                            PopUpAniStackedWidget, Action, InfoBar, InfoBarPosition, MessageBox, FluentTranslator,
                            MessageBoxBase, SubtitleLabel, TextEdit, IndeterminateProgressBar, ImageLabel)
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow
import logging

logging.disable(logging.DEBUG)  # 关闭DEBUG日志的打印
logging.disable(logging.WARNING)  # 关闭WARNING日志的打印


class MicaMainWindow(BackgroundAnimationWidget, FramelessWindow):
    """ 启用 Win11 云母材质效果的QMainWindow窗口 """
    enableMica = True

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        if sys.platform != 'win32' or sys.getwindowsversion().build < 22000:
            return

        if self.enableMica:
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())
        else:
            self.windowEffect.removeBackgroundEffect(self.winId())

        self.setBackgroundColor(self._normalBackgroundColor())


class MainWindow(MicaMainWindow):
    """Qt窗口主类"""
    pageLock = False  # 测试时的页面锁定属性

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """初始化UI"""

        # 初始化窗口
        self.setTitleBar(FluentTitleBar(self))  # 配置标题栏
        self.titleBar.raise_()
        self.setWindowTitle('Key-Value Knowledge')

        self.resize(1000, 650)  # 配置窗口大小

        # 初始化布局
        self.rootLayout = QHBoxLayout(self)  # 根布局
        self.navigationBar = NavigationBar(self)  # 侧导航栏
        self.stackWidget = PopUpAniStackedWidget(self)  # 主面板

        # 在布局中添加控件
        self.rootLayout.addWidget(self.navigationBar)
        self.rootLayout.addWidget(self.stackWidget)

        # 配置控件属性
        self.navigationBar.setMaximumWidth(70)  # 设置侧导航栏最大宽度

        self.rootLayout.setSpacing(0)  # 布局间隙
        self.rootLayout.setContentsMargins(0, 50, 0, 0)  # 布局边框

        # 设置控件qss
        if not isDarkTheme():
            self.stackWidget.setStyleSheet(  # 设置亮色主题Qss
                "#stack{background: rgba(253,253,253,150);"
                "border-top-left-radius: 8px;"
                "border: 1px solid rgba(200,200,200,100)}")
        else:
            self.stackWidget.setStyleSheet(  # 设置暗色主题Qss
                "#stack{background: rgba(15,15,15,150);"
                "border-top-left-radius: 8px;"
                "border: 1px solid rgba(200,200,200,100)}")

        self.stackWidget.setObjectName("stack")

        # 初始化各页面
        self.initPages()

        # 初始化侧边导航栏
        self.initNavigationBar()

    def setCurrentPage(self, widget):
        """设置当前页面"""
        if not self.pageLock:
            self.stackWidget.setCurrentWidget(widget)
            widget.reinit()
        else:
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
        # 主页按钮
        self.stackWidget.addWidget(self.pageHome)
        self.navigationBar.addItem(
            routeKey=self.pageHome.objectName(),
            icon=FluentIcon.HOME,
            text="主页",
            onClick=lambda: self.setCurrentPage(self.pageHome),
            position=NavigationItemPosition.TOP,
        )
        # 库按钮
        self.stackWidget.addWidget(self.pageKnowledgeManager)
        self.navigationBar.addItem(
            routeKey=self.pageKnowledgeManager.objectName(),
            icon=FluentIcon.IOT,
            text="仓库",
            onClick=lambda: self.setCurrentPage(self.pageKnowledgeManager),
            position=NavigationItemPosition.TOP,
        )

        # 新建
        self.stackWidget.addWidget(self.pageEdit)
        self.navigationBar.addItem(
            routeKey=self.pageEdit.objectName(),
            icon=FluentIcon.ADD_TO,
            text="添加",
            onClick=lambda: self.setCurrentPage(self.pageEdit),
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

        # 其他非可导航的页面
        self.stackWidget.addWidget(self.pageKnowledgeReview)
        self.stackWidget.addWidget(self.pageKnowledgeTest)
        self.stackWidget.addWidget(self.pageKnowledgeTestReport)

        # 设置默认页面为主页
        self.navigationBar.setCurrentItem(self.pageHome.objectName())

    def initPages(self):
        """初始化各页面"""
        self.pageHome = PageHome(self.stackWidget)  # 主页
        self.pageKnowledgeManager = PageKnowledgeManager(self.stackWidget)  # 知识管理页面
        self.pageKnowledgeReview = PageKnowledgeReview(self.stackWidget)  # 知识复习页面
        self.pageEdit = PageEdit(self.stackWidget)  # 新建文件页面
        self.pageKnowledgeTest = PageTest(self.stackWidget)  # 测试页面
        self.pageKnowledgeTestReport = PageKnowledgeTestReport(self.stackWidget)  # 测试报告页面


class PageKnowledgeManager(QWidget, library.Ui_PageLibrary):
    """库页面Widget"""

    collation = 0x00
    collationList = {
        0x00: ["创建日期", FluentIcon.DATE_TIME.icon],
        0x01: ["创建日期(倒序)", FluentIcon.DATE_TIME.icon],
        0x02: ["名称 A-Z", FluentIcon.TAG.icon],
        0x03: ["名称 Z-A", FluentIcon.TAG.icon],
        0x04: ["掌握程度", FluentIcon.MARKET.icon],
        0x05: ["掌握程度(倒叙)", FluentIcon.MARKET.icon],
    }

    filterRules = None

    # TODO 更改拟定数据
    tags = ["语文", "数学", "英语", "物理", "地理", "生物", "政治", "历史", "Python"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化UI
        self.setupUi(self)
        self.initUI()
        self.initWidgets()

        # 初始化数据
        self.initLibrary()

    def sortOptionsCallBack(self, index):
        """
        排序方式更改时的回调函数
        """
        self.collation = index
        self.collationSelector.setIcon(self.collationList[self.collation][1]())
        self.collationSelector.setText(self.collationList[self.collation][0])

        self.initLibrary()

        self.parent().setCurrentIndex(2, duration=0)
        self.parent().setCurrentIndex(1, duration=0)
        self.parent().setCurrentIndex(2, duration=0)
        self.parent().setCurrentIndex(1, duration=0)

    def filterOptionsCallBack(self, tag):
        """
        筛选方式更改时的回调函数
        """
        self.filterRules = tag
        self.filterSelector.setText(tag)

        self.initLibrary()

        self.parent().setCurrentIndex(2, duration=0)
        self.parent().setCurrentIndex(1, duration=0)
        self.parent().setCurrentIndex(2, duration=0)
        self.parent().setCurrentIndex(1, duration=0)

    def enterKnowledgeCallBack(self, item):
        self.parent().parent().stackWidget.setCurrentWidget(self.parent().parent().pageKnowledgeReview)  # noqa
        self.parent().parent().pageKnowledgeReview.initData(self.data[item.row()])  # noqa

    def initWidgets(self):
        """初始化控件功能"""

        # 设置下拉框控件
        self.collationSelector.setIcon(FluentIcon.SCROLL.icon())
        self.collationSelectorMenu = RoundMenu()
        for c in self.collationList.keys():
            # 添加菜单项并绑定事件
            action = QAction(self.collationList[c][1](), self.collationList[c][0])
            exec(f"action.triggered.connect(lambda :self.sortOptionsCallBack({c}))", locals(), locals())  # noqa

            self.collationSelectorMenu.addAction(action)

        self.collationSelector.setMenu(self.collationSelectorMenu)

        # 筛选下拉框
        self.filterSelector.setIcon(FluentIcon.FILTER.icon())
        self.filterSelectorMenu = RoundMenu()

        for tag in self.tags:
            action = QAction(FluentIcon.TAG.icon(), tag)
            exec(f"action.triggered.connect(lambda :self.filterOptionsCallBack(\"{tag}\"))", locals(), locals())  # noqa

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
        self.knowledgeTable.itemClicked.connect(self.enterKnowledgeCallBack)

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
        self.data = list(filter(lambda x: self.filterRules in x[3], self.data))

    def initLibrary(self):
        """初始化仓库信息"""

        # 更新遗忘率
        kvkapi.updateAttenuation()

        # 获取知识点数据
        self.data = kvkapi.getKnowledgeData()

        # 筛选数据
        self.filterByTag() if self.filterRules is not None else None

        # 排序数据
        if self.collation == 0x00 or self.collation == 0x01:
            self.sortByDate(self.collation == 0x01)
        elif self.collation == 0x02 or self.collation == 0x03:
            self.sortByName(self.collation == 0x03)
        elif self.collation == 0x04 or self.collation == 0x05:
            self.sortByMastery(self.collation == 0x05)

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

            # 设置第四列知识点掌握程度
            itemLayout = QVBoxLayout()
            itemLayout.setSpacing(5)
            itemLayout.setContentsMargins(18, 18, 18, 18)

            print(row)
            item = QLabel(str(int(row[4] * 100)) + "%")
            item.setStyleSheet("font-family: SIMHEI;font-size: 13px;color: black;") if not isDarkTheme() \
                else item.setStyleSheet("font-family: SIMHEI;font-size: 13px;color: white;")
            item.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            itemLayout.addWidget(item)

            item = ProgressBar(self)  # noqa

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
        self.parent().setCurrentIndex(2, duration=0)
        self.parent().setCurrentIndex(1, duration=0)
        self.parent().setCurrentIndex(2, duration=0)
        self.parent().setCurrentIndex(1, duration=200)


class PageKnowledgeReview(QWidget, knowledgeReview.Ui_PageKnowledgeReview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        self.visibleToggleButton.setIcon(FluentIcon.VIEW)

        self.SingleDirectionScrollArea.smoothScroll.orient = Qt.Horizontal

        # 绑定按钮事件
        self.listenButton.clicked.connect(self.TTSOutput)
        self.testButton.clicked.connect(
            lambda: self.parent().parent().setCurrentPage(self.parent().parent().pageKnowledgeTest))
        self.visibleToggleButton.clicked.connect(self.visibleToggleCallBack)
        self.editButton.clicked.connect(self.editButtonCallBack)
        self.deleteButton.clicked.connect(self.deleteButtonCallBack)

    def visibleToggleCallBack(self):
        if self.visibleToggleButton.isChecked():
            self.mainWidget.reinitLayout(None, None, True)
        else:
            self.mainWidget.reinitLayout(None, None, False)

    def deleteButtonCallBack(self):
        w = MessageBox("确定删除", "一旦删除永远不可恢复", self.window())
        w.yesButton.setStyleSheet(
            """    color: rgb(240,240,240);background: rgb(255, 0, 0);
            border: 1px solid rgba(0, 0, 0, 0.073);border-bottom: 2px solid rgba(0, 0, 0, 0.183);
            border-radius: 5px;padding: 5px 12px 6px 12px;outline: none;""")
        if w.exec_():  # noqa
            os.remove(self.path)
            self.parent().parent().setCurrentPage(self.parent().parent().pageKnowledgeManager)

    def editButtonCallBack(self):
        self.parent().parent().setCurrentPage(self.parent().parent().pageEdit)
        self.parent().parent().pageEdit.loadData(self.data)

    def saveNewData(self, newData):
        """保存测试完成后的新数据"""
        with open(self.path, "w", encoding="utf-8") as file:
            file.write(json.dumps(newData))
            file.close()

    def TTSOutput(self):
        """TTS: 导出音频"""
        path = QFileDialog.getSaveFileName(self, "选择音频保存的路径", self.knowledgeTitle.text(), "MP3音频(*.mp3)")
        kvkapi.textToSpeech(
            "知识点," + self.data["name"] + "。" + ";".join(
                [i["key"] + ": " + i["value"] for i in self.data["knowledge_points"]]),
            path[0],
        )

    def initData(self, data):
        """初始化数据"""
        self.path = os.path.join('.\\knowledge\\', data[0])
        self.data = json.loads(open(self.path, "r", encoding="utf-8").read())

        kv_points_length = 0
        for i in self.data["knowledge_points"]:
            kv_points_length += 1 if i["type"] == "kv" else None

        self.knowledgeTitle.setText(data[1])
        self.masteryRing.setValue(int(data[4] * 100))
        self.knowledgeInfoTitle.setText(
            f"{kv_points_length}个知识块   上次复习{pwidgets.format_time(self.data['last_review_time'])}")

        self.mainWidget.reinitData(self.data)


class PageEdit(QWidget, edit.Ui_PageEdit):
    # 初始化数据
    data = {
        "name": "新的专题",
        "tags": [],
        "created_time": time.time(),
        "last_review_time": time.time(),
        "review_time": 1,
        "mastery_level": 1.0,
        "attenuation": 0,
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
                "review_time": 1,
                "mastery_level": 1.0,
                "attenuation": 0,
                "knowledge_points": []
            }

            print(self.data)
            self.data["created_time"] = time.time()
            self.data["last_review_time"] = time.time()

            self.saved = False
            self.mainWidget.updateDataFromParent(self.data)
            self.mainWidget.reinitLayout()

    def loadData(self, data):
        self.data = data
        self.knowledgeTitle.setText(self.data["name"])
        self.mainWidget.reinitData(self.data)

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
        self.commandBar.addAction(Action(FluentIcon.PHOTO, "从图片中提取", triggered=self.OCR))
        self.commandBar.addAction(Action(FluentIcon.ROBOT, "一键导入", triggered=self.autoImport))
        self.commandBar.addAction(Action(FluentIcon.SAVE, "保存", triggered=self.saveData))
        self.commandBar.addAction(Action(FluentIcon.TAG, "标签", triggered=self.setTags))
        self.commandBar.addAction(Action(FluentIcon.ADD, "新建知识页", triggered=self.newData))

        # 绑定滚轮横向移动
        self.SingleDirectionScrollArea.smoothScroll.orient = Qt.Horizontal

        # 设置QSS
        self.knowledgeTitle.setStyleSheet(
            "background: rgba(0,0,0,0);border: 0;font-size: 29px;color: #FFFFFF") if isDarkTheme() \
            else self.knowledgeTitle.setStyleSheet(
            "background: rgba(0,0,0,0);border: 0;font-size: 29px;color: #000000")
        self.saved = False

    def autoImport(self):
        """一键自动导入"""
        """调用OCR技术"""
        path = QFileDialog.getOpenFileName(self, "选择图像", "", "图像文件(*.jpg *.gif *.png *.jpeg *.bmp)")
        self.w = MessageBoxAutoLoadWaiting(self.window(), path[0])  # noqa
        self.kvText = ""

        threading.Thread(target=self.importDataThread, args=(path[0],)).start()

        # 等待数据处理完成
        self.imageHandle = False
        self.toKV = False
        self.OCRResult = []

        self.waitForTarget(self.importDataUpdate)

        self.w.exec_()

    def importDataThread(self, path):
        """自动导入等待进程"""

        # 二值化处理
        kvkapi.toGray(path)
        self.imageHandle = True

        # 文本提取
        self.OCRResult = kvkapi.readText()
        kvkapi.drawOCRLine(self.OCRResult[1][0])

        # AI修正
        c = kvkapi.correctText(self.OCRResult[0])

        text = c if c.split(" ") else self.OCRResult[0]

        # Key = Value化
        kv = kvkapi.KVText(text)
        text = json.loads(kv.replace("\n", ""))

        print(text)

        for i in text.keys():
            self.data["knowledge_points"].append({
                "type": "kv",
                "key": i,
                "value": text[i],
            })

        self.toKV = True

    def importDataUpdate(self):
        """
        自动导入循环进程
        """
        pixmap = QPixmap(".\\BINARY_PHOTO.png").scaledToWidth(500)
        self.w.imageFrame.setPixmap(pixmap)

        if self.toKV:
            self.mainWidget.updateDataFromParent(self.data)
            self.w.close()
            self.timer.stop()

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

        self.saveTitleData()

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

    def waitForTarget(self, target):
        self.timer = QTimer()
        self.timer.setInterval(500)
        self.timer.timeout.connect(target)  # noqa
        self.timer.start()

    def OCR(self):
        """调用OCR技术"""
        path = QFileDialog.getOpenFileName(self, "选择图像", "", "图像文件(*.jpg *.gif *.png *.jpeg *.bmp)")
        self.w = MessageBoxOCRWaiting(self.window())
        self.ocrText = None

        threading.Thread(target=self.OCRThread, args=(path[0],)).start()

        # 等待OCR处理完成
        self.waitForTarget(self.ocrUpdate)

        self.w.exec_()

    def ocrUpdate(self):
        """OCR等待循环进程"""
        if self.ocrText:
            self.w.textFrame.setText(self.ocrText[0])  # noqa
            self.w.title.setText("提取完成")
            self.w.progressBar.stop()
            self.timer.stop()

    def OCRThread(self, path):
        """OCR等待进程"""
        self.ocrText = kvkapi.readText(path)

    def newData(self):
        """新建知识页"""
        if not self.saved:
            if MessageBox("当前知识页未保存", "新建将丢弃当前未保存的知识页，确定操作吗", self.window()).exec():  # noqa
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
        w = PageEditSetTagsBox(self.window(), self.data["tags"])  # noqa
        e = w.exec_()

        if e is not None:
            self.data["tags"] = e  # noqa


class MessageBoxAutoLoadWaiting(MessageBoxBase):
    data = None

    def __init__(self, parent, path):
        super().__init__(parent)
        self.path = path

        self.initUI()

    def initUI(self):
        """初始化UI"""
        # 标题
        self.title = SubtitleLabel(self)
        self.title.setText("正在提取文本...")
        self.viewLayout.addWidget(self.title)

        # 图片框
        self.imageFrame = ImageLabel(self)
        pixmap = QPixmap(self.path).scaledToWidth(500)

        self.imageFrame.setPixmap(pixmap)
        self.viewLayout.addWidget(self.imageFrame)

        # 进度条
        self.progressBar = IndeterminateProgressBar(self)
        self.viewLayout.addWidget(self.progressBar)

        # 按钮
        self.hideCancelButton()
        self.hideYesButton()


class MessageBoxOCRWaiting(MessageBoxBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        # 初始化布局
        self.setLayout(self.viewLayout)

        # 标题
        self.title = SubtitleLabel(self)
        self.title.setText("正在提取文本...")
        self.viewLayout.addWidget(self.title)

        # 文本框
        self.textFrame = TextEdit(self)
        self.viewLayout.addWidget(self.textFrame)

        # 进度条
        self.progressBar = IndeterminateProgressBar(self)
        self.viewLayout.addWidget(self.progressBar)

        # 按钮
        self.yesButton.setText("复制")
        self.yesButton.clicked.connect(self.copyText)
        self.cancelButton.setText("关闭")

    def copyText(self):
        pyperclip.copy(self.textFrame.toPlainText())


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

        self.flowWidget = QWidget(self)  # noqa
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


class PageTest(QWidget, test.Ui_PageTest):
    answerEditFrameMaxHeight = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        self.answerEdit.setMaximumHeight(100)
        self.answerEdit.textChanged.connect(self.updateAnswerEditFrameHeight)

        self.progressLabel.setWordWrap(True)

        self.enterButton.clicked.connect(self.callBackEnterButton)

    def startTest(self):
        """开始测试"""
        # 锁定页面
        self.parent().parent().lock = True

        # 获取数据
        self.data = self.parent().parent().pageKnowledgeReview.data

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
        self.TestOne(self.data["knowledge_points"][self.current_question])

    def TestOne(self, question):
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

        # 更新数据到本地知识点
        newData = self.parent().parent().pageKnowledgeReview.data.copy()
        newData["last_review_time"] = time.time()
        newData["mastery_level"] = (self.report["no_all"] - self.report["no_wrong"]) / self.report["no_all"]

        self.parent().parent().pageKnowledgeReview.saveNewData(newData)

        # 重新设置UI
        self.parent().parent().setCurrentPage(self.parent().parent().pageKnowledgeTestReport)
        self.parent().parent().pageKnowledgeTestReport.initData(self.report)

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

            self.TestOne(self.data["knowledge_points"][self.current_question])

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

        print(self.report)

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
        self.startTest()


class PageKnowledgeTestReport(QWidget, testReport.Ui_PageTestReport):
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
        # 显示界面
        self.nOKnoeledgeLabel.setText(str(data["no_all"]))
        self.timeLabel.setText(f'{int(data["end_time"] - data["start_time"])} 秒')
        self.missingLabel.setText(f'{data["no_wrong"]} 个块')

        self.progressRing.setValue(int((data["no_all"] - data["no_wrong"]) / data["no_all"] * 100))

        # 更新数据

        self.returnButton.clicked.connect(
            lambda: self.parent().parent().setCurrentPage(self.parent().parent().pageKnowledgeManager))


class PageHome(QWidget, home.Ui_PageHome):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUI()
        self.reinit()

    def initUI(self):
        """初始化UI"""

        # 获取当前时间
        now = datetime.datetime.now()

        # 根据时间判断问候语
        if now.hour < 12:
            greeting = "上午好"
        elif now.hour < 18:
            greeting = "下午好"
        else:
            greeting = "晚上好"

        # 获取当前用户名
        username = getpass.getuser()

        # 输出问候语和用户名
        self.welcomeLabel.setText(f"{greeting},  {username}!")

    def reinit(self):
        # 更新遗忘率
        kvkapi.updateAttenuation()

        # 筛选数据
        self.data = kvkapi.getKnowledgeData()
        self.dataLowMastery = sorted(self.data, key=lambda x: x[-1])
        self.dataLowMastery = self.dataLowMastery[:2] if len(self.dataLowMastery) >= 2 else self.dataLowMastery
        self.dataLongCycle = sorted(self.data, key=lambda x: x[2])
        self.dataLongCycle = self.dataLongCycle[:2] if len(self.dataLongCycle) >= 2 else self.dataLongCycle

        # 隐藏空卡
        self.card1.hide()
        self.card2.hide()
        self.card3.hide()
        self.card4.hide()

        if len(self.dataLowMastery) == 1:
            self.card1.initData(self.dataLowMastery[0])
        elif len(self.dataLowMastery) == 2:
            self.card1.initData(self.dataLowMastery[0])
            self.card2.initData(self.dataLowMastery[1])

        if len(self.dataLongCycle) == 1:
            self.card3.initData(self.dataLongCycle[0])
        elif len(self.dataLongCycle) == 2:
            self.card3.initData(self.dataLongCycle[0])
            self.card4.initData(self.dataLongCycle[1])


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
    setTheme(Theme.LIGHT)

    # 适应Dpi
    setHighDpi()

    # 实例化
    app = QApplication(sys.argv)

    # 设置语言
    locale = QLocale()
    translator = FluentTranslator(locale)
    app.installTranslator(translator)  # noqa

    # 运行
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()
