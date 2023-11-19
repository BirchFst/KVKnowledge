import sys
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QHBoxLayout
from PyQt5.QtCore import pyqtProperty, QPropertyAnimation
from qfluentwidgets import ElevatedCardWidget, StrongBodyLabel, BodyLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


class KnowledgeCard(ElevatedCardWidget):
    showAnswer = False

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
        self.valueLabel.setStyleSheet("color: rgba(0,0,0,0)")
        self.valueLabel.setWordWrap(True)
        self.valueLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.valueLabel)

    def setData(self, data):
        self.keyLabel.setText(data["key"])
        self.valueLabel.setText(data["value"])

    def mouseReleaseEvent(self, e):
        self.showAnswer = False if self.showAnswer else True

        if self.showAnswer:
            self.animation = QPropertyAnimation(self)
            self.animation.setTargetObject(self)
            self.animation.setPropertyName(b"valueOpacity")
            self.animation.setStartValue(0)
            self.animation.setEndValue(255)
            self.animation.setDuration(100)

            self.animation.start()

        else:
            self.animation = QPropertyAnimation(self)
            self.animation.setTargetObject(self)
            self.animation.setPropertyName(b"valueOpacity")
            self.animation.setStartValue(255)
            self.animation.setEndValue(0)
            self.animation.setDuration(100)

            self.animation.start()

    def setValueOpacity(self, value):
        self.valueLabel.setStyleSheet(f"color: rgba(0,0,0,{value})")

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

    def reinitLayout(self, old=None, new=None):
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

            self.lines[line].layout().setContentsMargins(0, 0, 0, 0)
            self.lines[line].layout().setSpacing(5)

            # 添加卡片
            for card in range(no_cards * line, no_cards * line + no_cards):
                c = KnowledgeCard(self.lines[line]) if card < len(self.data["knowledge_points"]) else QWidget(
                    self.lines[line])

                c.setData(self.data["knowledge_points"][card]) if isinstance(c, KnowledgeCard) else None
                self.lines[line].layout().addWidget(c)


if __name__ == '__main__':
    # 实例化运行d
    app = QApplication(sys.argv)
    mainwindow = KnowledgeView()
    mainwindow.show()
    app.exec_()
