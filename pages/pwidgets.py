import sys

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy, QFrame, QApplication, QLayout, QHBoxLayout, \
    QSpacerItem
from PyQt5.QtCore import QSize

from qfluentwidgets import ElevatedCardWidget, FlowLayout, StrongBodyLabel

from PyQt5.QtWidgets import QLayout, QLayoutItem, QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLayout, QLayoutItem, QWidget


class KnowledgeCard(ElevatedCardWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        self.setMaximumWidth(260)

        # 初始化布局
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # 初始化控件
        self.textLabel = StrongBodyLabel(self)
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.textLabel)

    def setData(self, data):
        self.textLabel.setText(data["key"])


class KnowledgeView(QWidget):
    data = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        """初始化UI"""
        # 设置根布局
        self.rootLayout = QVBoxLayout()
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
        if old and new and new.width() // 250 == old.width() // 250:
            return

        # 删除所有行
        while self.rootLayout.count():
            item = self.rootLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.lines = []

        # 计算每行的卡片数
        no_cards = self.width() // 250
        no_lines = len(self.data["knowledge_points"]) / no_cards
        no_lines = int(no_lines) if no_lines == int(no_lines) else int(no_lines) + 1  # 向上整取

        # 创建各行布局并初始化
        for line in range(no_lines):
            self.lines.append(QWidget(self))
            self.rootLayout.addWidget(self.lines[line])
            self.lines[line].setLayout(QHBoxLayout(self.lines[line]))
            self.lines[line].setFixedHeight(250)

            self.lines[line].layout().setContentsMargins(0, 0, 0, 0)
            self.lines[line].layout().setSpacing(10)

            # 添加卡片
            for card in range(no_cards * line, (no_cards - 1) * (line + 1) + 1):
                c = KnowledgeCard(self.lines[line]) if no_cards * line + card <= no_lines * no_lines else QWidget(
                    self.lines[line])
                c.setData(self.data["knowledge_points"][no_cards * line + card]) if isinstance(c, KnowledgeCard) else None
                self.lines[line].layout().addWidget(c)

        null_widget = QWidget(self)
        self.rootLayout.addWidget(null_widget)


if __name__ == '__main__':
    # 实例化运行d
    app = QApplication(sys.argv)
    mainwindow = KnowledgeView()
    mainwindow.show()
    app.exec_()
