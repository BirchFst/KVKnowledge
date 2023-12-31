# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\pageTest.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PageTest(object):
    def setupUi(self, PageTest):
        PageTest.setObjectName("PageTest")
        PageTest.resize(700, 600)
        font = QtGui.QFont()
        font.setPointSize(7)
        PageTest.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(PageTest)
        self.verticalLayout.setContentsMargins(36, 36, 36, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleLabel = SubtitleLabel(PageTest)
        self.titleLabel.setObjectName("titleLabel")
        self.verticalLayout.addWidget(self.titleLabel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.questionLabel = TitleLabel(PageTest)
        self.questionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.questionLabel.setObjectName("questionLabel")
        self.verticalLayout.addWidget(self.questionLabel)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.answerEdit = TextEdit(PageTest)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.answerEdit.sizePolicy().hasHeightForWidth())
        self.answerEdit.setSizePolicy(sizePolicy)
        self.answerEdit.setMinimumSize(QtCore.QSize(0, 100))
        self.answerEdit.setMaximumSize(QtCore.QSize(16777215, 200))
        self.answerEdit.setObjectName("answerEdit")
        self.verticalLayout.addWidget(self.answerEdit)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.enterButton = TransparentPushButton(PageTest)
        self.enterButton.setObjectName("enterButton")
        self.verticalLayout.addWidget(self.enterButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.progressLabel = BodyLabel(PageTest)
        self.progressLabel.setMinimumSize(QtCore.QSize(0, 100))
        self.progressLabel.setMaximumSize(QtCore.QSize(16777215, 100))
        self.progressLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.progressLabel.setObjectName("progressLabel")
        self.verticalLayout.addWidget(self.progressLabel)
        self.progressBar = ProgressBar(PageTest)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(PageTest)
        QtCore.QMetaObject.connectSlotsByName(PageTest)

    def retranslateUi(self, PageTest):
        _translate = QtCore.QCoreApplication.translate
        PageTest.setWindowTitle(_translate("PageTest", "Form"))
        self.titleLabel.setText(_translate("PageTest", "专题"))
        self.questionLabel.setText(_translate("PageTest", "题目"))
        self.answerEdit.setPlaceholderText(_translate("PageTest", "在此处输入答案"))
        self.enterButton.setText(_translate("PageTest", "提交"))
        self.progressLabel.setText(_translate("PageTest", "进度 3/5"))
from qfluentwidgets import BodyLabel, ProgressBar, SubtitleLabel, TextEdit, TitleLabel, TransparentPushButton
