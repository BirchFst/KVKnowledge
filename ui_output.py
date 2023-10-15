# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './UiResources/ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 740)
        self.RootWidget = QtWidgets.QWidget(MainWindow)
        self.RootWidget.setStyleSheet("")
        self.RootWidget.setObjectName("RootWidget")
        self.HLytRoot = QtWidgets.QHBoxLayout(self.RootWidget)
        self.HLytRoot.setContentsMargins(0, 0, 0, 0)
        self.HLytRoot.setSpacing(0)
        self.HLytRoot.setObjectName("HLytRoot")
        self.PadSide = QtWidgets.QWidget(self.RootWidget)
        self.PadSide.setMinimumSize(QtCore.QSize(300, 0))
        self.PadSide.setMaximumSize(QtCore.QSize(300, 16777215))
        self.PadSide.setStyleSheet("")
        self.PadSide.setObjectName("PadSide")
        self.VLyt = QtWidgets.QVBoxLayout(self.PadSide)
        self.VLyt.setObjectName("VLyt")
        self.SBtnKnowledge = PSideButton(self.PadSide)
        self.SBtnKnowledge.setObjectName("SBtnKnowledge")
        self.VLyt.addWidget(self.SBtnKnowledge)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.VLyt.addItem(spacerItem)
        self.HLytRoot.addWidget(self.PadSide)
        self.PadMain = QtWidgets.QStackedWidget(self.RootWidget)
        self.PadMain.setObjectName("PadMain")
        self.PadMainPage1 = QtWidgets.QWidget()
        self.PadMainPage1.setObjectName("PadMainPage1")
        self.PadMain.addWidget(self.PadMainPage1)
        self.HLytRoot.addWidget(self.PadMain)
        MainWindow.setCentralWidget(self.RootWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.SBtnKnowledge.setText(_translate("MainWindow", "知识库"))
from project_widget import PSideButton