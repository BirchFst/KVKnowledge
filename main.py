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

# 导入所需依赖
import sys
from PyQt5.QtWidgets import QLabel, QStackedWidget, QHeaderView, QAction, QTableWidgetItem, QVBoxLayout, QHBoxLayout, \
    QWidget, QApplication
from PyQt5.QtCore import Qt
from qfluentwidgets import NavigationItemPosition, isDarkTheme, FluentIcon, NavigationBar, FluentTitleBar, ProgressBar, \
    setThemeColor
from qfluentwidgets.common.animation import BackgroundAnimationWidget
from qfluentwidgets.components.widgets.frameless_window import FramelessWindow
import kvkapi
from pages import library


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
        self.stackWidget = QStackedWidget(self)

        self.layout.addWidget(self.navigationBar)
        self.layout.addWidget(self.stackWidget)

        self.navigationBar.setMaximumWidth(80)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 50, 0, 0)

        self.stackWidget.setStyleSheet(
            "#stack{background: rgba(253,253,253,150);"
            "border-top-left-radius: 8px;"
            "border: 1px solid rgba(200,200,200,100)}")
        self.stackWidget.setObjectName("stack")

        # 初始化页面
        self.initPages()

        # 初始化侧边导航栏
        self.initNavigationBar()

    def initNavigationBar(self):
        """初始化侧边导航栏"""

        # 库按钮
        self.stackWidget.addWidget(self.pageLibrary)
        self.navigationBar.addItem(
            routeKey=self.pageLibrary.objectName(),
            icon=FluentIcon.IOT,
            text="仓库",
            onClick=lambda: self.stackWidget.setCurrentWidget(self.pageLibrary),
            position=NavigationItemPosition.TOP,
        )

        # 新建
        self.stackWidget.addWidget(self.pageAddFile)
        self.navigationBar.addItem(
            routeKey=self.pageAddFile.objectName(),
            icon=FluentIcon.ADD_TO,
            text="添加",
            onClick=lambda: self.stackWidget.setCurrentWidget(self.pageAddFile),
            position=NavigationItemPosition.TOP,
        )

        self.stackWidget.addWidget(self.pageReview)
        self.navigationBar.addItem(
            routeKey=self.pageReview.objectName(),
            icon=FluentIcon.SYNC,
            text="复习",
            onClick=lambda: self.stackWidget.setCurrentWidget(self.pageReview),
            position=NavigationItemPosition.TOP,
        )

        self.navigationBar.setCurrentItem(self.pageLibrary.objectName())

    def initPages(self):
        self.pageLibrary = PageLibrary(self.stackWidget)
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 初始化UI
        self.setupUi(self)
        self.initUI()

        # 初始化数据
        self.initLibrary()

    def initUI(self):
        """初始化UI"""

        # 初始化表格

        # 设置表格边框
        self.knowledgeTable.setBorderVisible(True)
        self.knowledgeTable.setBorderRadius(8)

        # 设置表格布局
        self.knowledgeTable.setRowCount(5)
        self.knowledgeTable.setColumnCount(4)
        self.knowledgeTable.setHorizontalHeaderLabels(["知识", "日期", "标签", "掌握"])
        self.knowledgeTable.verticalHeader().hide()

        # 设置表格列宽
        self.knowledgeTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.knowledgeTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.knowledgeTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.knowledgeTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.knowledgeTable.horizontalHeader().setMinimumSectionSize(200)

        # 顶层控件
        self.addKnowledge.setIcon(FluentIcon.ADD)

    def initLibrary(self):
        """初始化仓库信息"""

        # 获取知识点数据
        self.data = kvkapi.getKnowledgeData()

        for r in range(len(self.data)):
            row = self.data[r]

            self.knowledgeTable.setItem(r, 0, QTableWidgetItem(row[1]))

            item = QTableWidgetItem(row[2])
            item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.knowledgeTable.setItem(r, 1, item)

            item = QTableWidgetItem(row[3])
            item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.knowledgeTable.setItem(r, 2, item)

            itemLayout = QVBoxLayout()
            itemLayout.setSpacing(0)

            item = QLabel(str(int(row[4] * 100)) + "%")
            item.setAlignment(Qt.AlignCenter)
            itemLayout.addWidget(item)

            item = ProgressBar(self)
            item.setMaximumWidth(160)
            item.setAlignment(Qt.AlignCenter)
            item.setValue(int(row[4] * 100))
            itemLayout.addWidget(item)

            itemWidget = QWidget()
            itemWidget.setLayout(itemLayout)

            self.knowledgeTable.setCellWidget(r, 3, itemWidget)


# 运行
if __name__ == '__main__':
    # 设置主题颜色
    setThemeColor("#0078D4")

    # 适应Dpi
    setHighDpi()

    # 实例化运行
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    app.exec_()
