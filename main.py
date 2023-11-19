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
from webbrowser import open as web_open
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QHeaderView, QAction, QTableWidgetItem, QVBoxLayout, QHBoxLayout, \
    QWidget, QApplication, QAbstractItemView
import kvkapi
from pages import library, knowledgePreview
from qfluentwidgets import NavigationItemPosition, isDarkTheme, FluentIcon, NavigationBar, FluentTitleBar, ProgressBar, \
    setThemeColor, FlowLayout, PillPushButton, RoundMenu, setTheme, Theme, PopUpAniStackedWidget, ElevatedCardWidget
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
        self.stackWidget.setCurrentWidget(widget)

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

        # 复习
        self.stackWidget.addWidget(self.pageReview)
        self.navigationBar.addItem(
            routeKey=self.pageReview.objectName(),
            icon=FluentIcon.SYNC,
            text="复习",
            onClick=lambda: self.setCurrentPage(self.pageReview),
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

        self.navigationBar.setCurrentItem(self.pageLibrary.objectName())

    def initPages(self):
        self.pageLibrary = PageLibrary(self.stackWidget)
        self.pageKnowledgePreview = PageKnowledgePreview(self.stackWidget)
        self.pageAddFile = Widget("2", self.stackWidget)
        self.pageReview = Widget("3", self.stackWidget)


def setHighDpi():
    """自适应高Dpi缩放"""
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)


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


class PageKnowledgePreview(QWidget, knowledgePreview.Ui_PageKnowledgePreview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        self.visibleToggleButton.setIcon(FluentIcon.HIDE)

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




# 运行
if __name__ == '__main__':
    # 设置主题颜色
    setThemeColor("#0078D4")
    setTheme(Theme.AUTO)

    # 适应Dpi
    setHighDpi()

    # 实例化运行d
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()
