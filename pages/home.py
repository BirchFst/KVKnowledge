# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\pageHome.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PageHome(object):
    def setupUi(self, PageHome):
        PageHome.setObjectName("PageHome")
        PageHome.resize(700, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(PageHome)
        self.verticalLayout.setContentsMargins(36, 36, 36, 36)
        self.verticalLayout.setObjectName("verticalLayout")
        self.welcomeLabel = TitleLabel(PageHome)
        self.welcomeLabel.setMaximumSize(QtCore.QSize(16777215, 100))
        self.welcomeLabel.setObjectName("welcomeLabel")
        self.verticalLayout.addWidget(self.welcomeLabel)
        self.Title1 = BodyLabel(PageHome)
        self.Title1.setMaximumSize(QtCore.QSize(16777215, 50))
        self.Title1.setObjectName("Title1")
        self.verticalLayout.addWidget(self.Title1)
        self.widget_1 = QtWidgets.QWidget(PageHome)
        self.widget_1.setObjectName("widget_1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.card1 = HomeCard(self.widget_1)
        self.card1.setObjectName("card1")
        self.horizontalLayout.addWidget(self.card1)
        self.card2 = HomeCard(self.widget_1)
        self.card2.setObjectName("card2")
        self.horizontalLayout.addWidget(self.card2)
        self.verticalLayout.addWidget(self.widget_1)
        self.Title2 = BodyLabel(PageHome)
        self.Title2.setMaximumSize(QtCore.QSize(16777215, 50))
        self.Title2.setObjectName("Title2")
        self.verticalLayout.addWidget(self.Title2)
        self.widget_2 = QtWidgets.QWidget(PageHome)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.card3 = HomeCard(self.widget_2)
        self.card3.setObjectName("card3")
        self.horizontalLayout_2.addWidget(self.card3)
        self.card4 = HomeCard(self.widget_2)
        self.card4.setObjectName("card4")
        self.horizontalLayout_2.addWidget(self.card4)
        self.verticalLayout.addWidget(self.widget_2)

        self.retranslateUi(PageHome)
        QtCore.QMetaObject.connectSlotsByName(PageHome)

    def retranslateUi(self, PageHome):
        _translate = QtCore.QCoreApplication.translate
        PageHome.setWindowTitle(_translate("PageHome", "Form"))
        self.welcomeLabel.setText(_translate("PageHome", "Welcome!"))
        self.Title1.setText(_translate("PageHome", "低掌握度"))
        self.Title2.setText(_translate("PageHome", "周期较长"))
from pwidgets import HomeCard
from qfluentwidgets import BodyLabel, TitleLabel
