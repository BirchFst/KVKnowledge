import datetime
import json
import os
import sys

from PyQt5.QtGui import QPalette, QColor, QDesktopServices
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QHBoxLayout, QFrame
from PyQt5.QtCore import pyqtProperty, QPropertyAnimation, QSize, QEvent, QUrl
from qfluentwidgets import ElevatedCardWidget, StrongBodyLabel, BodyLabel, LineEdit, TextEdit, CardWidget, isDarkTheme, \
    IconWidget, FluentIcon, SubtitleLabel, ProgressBar
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


def format_time(timestamp):
    """转换时间格式"""
    now = datetime.datetime.now()
    target = datetime.datetime.fromtimestamp(timestamp)
    diff = now - target

    if diff.days < 7:
        return f"{diff.days}天前"
    elif diff.days < 21:
        return f"{diff.days // 7}周前"
    else:
        return target.strftime("%Y.%m.%d")


class KnowledgeCard(ElevatedCardWidget):
    # 设置初始可见性
    visitable = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initUI()

        self.colorValueOpacity = 0

    def initUI(self):
        """初始化UI"""
        self.setMaximumHeight(260)

        # 初始化布局
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(self.layout)

        # 初始化控件
        self.keyLabel = StrongBodyLabel(self)
        self.keyLabel.setAlignment(Qt.AlignCenter)
        self.keyLabel.setWordWrap(True)
        self.layout.addWidget(self.keyLabel)

        self.valueLabel = BodyLabel(self)
        self.valueLabel.setStyleSheet("color: rgba(0,0,0,0);") if isDarkTheme() else self.valueLabel.setStyleSheet(
            "color: rgba(255,255,255,0);")
        self.valueLabel.setWordWrap(True)
        self.valueLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.valueLabel)

    def setData(self, data):
        self.keyLabel.setText(data["key"])
        self.valueLabel.setText(data["value"])

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)

        self.visitable = False if self.visitable else True

        if self.visitable:
            self.showAnswer()
        else:
            self.hideAnswer()

    def hideAnswer(self):
        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b"valueOpacity")
        self.animation.setStartValue(255)
        self.animation.setEndValue(0)
        self.animation.setDuration(100)

        self.animation.start()

    def showAnswer(self):
        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b"valueOpacity")
        self.animation.setStartValue(0)
        self.animation.setEndValue(255)
        self.animation.setDuration(100)

        self.animation.start()

    def setValueOpacity(self, value):
        if isDarkTheme():
            self.valueLabel.setStyleSheet(f"color: rgba(255,255,255,{value})")
        else:
            self.valueLabel.setStyleSheet(f"color: rgba(0, 0, 0,{value})")

    valueOpacity = pyqtProperty(int, fget=lambda self: self.colorValueOpacity, fset=setValueOpacity)


class KnowledgeView(QWidget):
    data = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        # 设置根布局
        self.rootLayout = QHBoxLayout()
        self.rootLayout.setSpacing(10)
        self.lines = []

        self.setLayout(self.rootLayout)

    def reinitData(self, data):
        self.data = data
        self.reinitLayout()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.data:
            self.reinitLayout(event.oldSize(), event.size())

    def reinitLayout(self, old=None, new=None, visitable=None):
        """重初始化卡片"""

        # 若长宽变化幅度不大则不重新布局
        if old and new and new.height() // 250 == old.height() // 250:
            return

        # 删除所有行
        while self.rootLayout.count():
            item = self.rootLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.lines = []

        # 计算每行的卡片数
        no_cards = self.height() // 250
        no_lines = len(self.data["knowledge_points"]) / no_cards
        no_lines = int(no_lines) if no_lines == int(no_lines) else int(no_lines) + 1  # 向上整取

        # 创建各行布局并初始化
        for line in range(no_lines):
            self.lines.append(QWidget(self))

            self.rootLayout.addWidget(self.lines[line])
            self.lines[line].setLayout(QVBoxLayout(self.lines[line]))
            self.lines[line].setFixedWidth(250)

            self.lines[line].layout().setSpacing(5)
            self.lines[line].layout().setContentsMargins(0, 0, 0, 0)

            # 添加卡片
            for card in range(no_cards * line, no_cards * line + no_cards):
                if card < len(self.data["knowledge_points"]):
                    # 创建卡片
                    c = KnowledgeCard(self.lines[line])
                    c.setData(self.data["knowledge_points"][card])

                    c.showAnswer() if visitable else c.hideAnswer()

                    # 添加至布局
                    self.lines[line].layout().addWidget(c)


class EditKeyFrame(LineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isDarkTheme():
            palette = QPalette()
            palette.setColor(QPalette.Text, QColor(255, 255, 255))

            self.setPalette(palette)
        else:
            palette = QPalette()
            palette.setColor(QPalette.Text, QColor(0, 0, 0))

            self.setPalette(palette)

    def focusOutEvent(self, e):
        """失焦回调"""
        self.parent().saveCardData()


class EditValueFrame(TextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isDarkTheme():
            palette = QPalette()
            palette.setColor(QPalette.Text, QColor(255, 255, 255))

            self.setPalette(palette)
        else:
            palette = QPalette()
            palette.setColor(QPalette.Text, QColor(0, 0, 0))

            self.setPalette(palette)

    def focusOutEvent(self, e):
        """失焦回调"""
        try:
            self.parent().saveCardData()
        except AttributeError:
            return


class KnowledgeEditCard(CardWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

        self.colorValueOpacity = 0

    def initUI(self):
        """初始化UI"""
        # 设置失焦回调
        self.setMaximumHeight(260)

        # 初始化布局
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(self.layout)

        # 初始化控件
        self.keyFrame = EditKeyFrame(self)
        self.keyFrame.setStyleSheet("background: rgba(0,0,0,0);border: 0;font-weight: bold;font-size: 16px")
        self.keyFrame.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.keyFrame)

        self.valueFrame = EditValueFrame(self)
        self.valueFrame.setPlaceholderText("单击编辑知识内容")
        self.valueFrame.setStyleSheet("background: rgba(0,0,0,0);border: 0;font-size: 14px")
        self.valueFrame.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.valueFrame)

    def saveCardData(self):
        """变更卡片数据"""
        self.parent().parent().updateDataFromChildren()  # noqa

    def setData(self, data):
        """设置卡片数据"""
        self.keyFrame.setText(data["key"])
        self.valueFrame.setText(data["value"])

    def setIndex(self, index):
        """设置在全局中的索引"""
        self.index = index


class KnowledgeEditPad(QWidget):
    data = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        # 设置根布局
        self.rootLayout = QHBoxLayout()
        self.rootLayout.setSpacing(10)
        self.lines = []

        self.setLayout(self.rootLayout)

    def reinitData(self, data):
        self.data = data
        self.reinitLayout()

    def addData(self, data):
        self.updateDataFromParent(data)

    def updateDataFromParent(self, data):
        self.data = data
        self.reinitLayout()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.data:
            self.reinitLayout(event.oldSize(), event.size())

    def reinitLayout(self, old=None, new=None):
        """重初始化卡片"""

        # 若长宽变化幅度不大则不重新布局
        if old and new and new.height() // 250 == old.height() // 250:
            return None

        # 删除所有行
        while self.rootLayout.count():
            item = self.rootLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.lines = []

        # 计算每行的卡片数
        self.no_cards = self.height() // 250
        self.no_lines = len(self.data["knowledge_points"]) / self.no_cards
        self.no_lines = int(self.no_lines) if self.no_lines == int(self.no_lines) else int(self.no_lines) + 1  # 向上整取

        # 创建各行布局并初始化
        for line in range(self.no_lines):
            self.lines.append(QWidget(self))
            self.rootLayout.addWidget(self.lines[line])
            self.lines[line].setLayout(QVBoxLayout(self.lines[line]))
            self.lines[line].setFixedWidth(250)

            self.lines[line].layout().setContentsMargins(0, 0, 0, 0)
            self.lines[line].layout().setSpacing(5)

            # 添加卡片
            for card in range(self.no_cards * line, self.no_cards * line + self.no_cards):
                if card < len(self.data["knowledge_points"]):
                    c = KnowledgeEditCard(self.lines[line])

                    c.setData(self.data["knowledge_points"][card])
                    c.setIndex(card)
                    self.lines[line].layout().addWidget(c)

    def updateDataFromChildren(self):
        """更新数据并传回父类"""
        self.data["knowledge_points"] = []
        for line in self.lines:
            for card in line.children():
                if isinstance(card, KnowledgeEditCard):
                    self.data["knowledge_points"].append({
                        "type": "kv",
                        "key": card.keyFrame.text(),
                        "value": card.valueFrame.toPlainText()
                    })

        self.parent().parent().data = self.data
        self.reinitLayout()


class HomeCard(CardWidget):
    """ Example card """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        # 设置布局
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)

        # 添加控件
        self.title = SubtitleLabel(self)  # 标题标签

        self.info = BodyLabel(self)  # 信息标签
        self.info.setStyleSheet("color: gray;")

        self.preview = StrongBodyLabel(self)  # 预览标签

        self.progress = ProgressBar(self)  # 掌握度进度条
        self.progress.setTextVisible(True)

        # 添加至布局
        self.mainLayout.addWidget(self.title)
        self.mainLayout.addWidget(self.info)
        self.mainLayout.addWidget(self.preview)
        self.mainLayout.addWidget(self.progress)

    def initData(self, data):
        # 载入数据
        self.show()

        self.data = data

        self.jsonData = json.loads(open(os.path.join('.\\knowledge\\', data[0]), "r", encoding="utf-8").read())
        kv_points_length = 0
        for i in self.jsonData["knowledge_points"]:
            kv_points_length += 1 if i["type"] == "kv" else None

        # 设置控件信息
        self.title.setText(data[1])  # 标题

        self.info.setText(  # 信息标签
            f"{kv_points_length}个知识块   上次复习{format_time(self.jsonData['last_review_time'])}   "
            f"掌握{int(self.jsonData['mastery_level'] * (1 - self.jsonData['attenuation']) * 100)}%")

        keys = [i["key"] for i in self.jsonData["knowledge_points"]]
        shortKeys = '   '.join(keys)[:40] if len('   '.join(keys)) > 40 else '   '.join(keys)
        self.preview.setText(f"{shortKeys}{'...' if len('   '.join(keys)) > 20 else ''}")  # Key预览标签

        self.progress.setValue(int(self.jsonData['mastery_level'] * (1 - self.jsonData['attenuation']) * 100))  # 设置进度条值

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        p = self.parent().parent().parent().parent()
        p.stackWidget.setCurrentWidget(p.pageKnowledgeReview)  # noqa
        p.pageKnowledgeReview.initData(self.data)  # noqa


if __name__ == '__main__':
    # 实例化运行d
    app = QApplication(sys.argv)
    mainwindow = KnowledgeView()
    mainwindow.show()
    app.exec_()
