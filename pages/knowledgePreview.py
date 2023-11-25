# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\pageKnowledgePreview.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PageKnowledgePreview(object):
    def setupUi(self, PageKnowledgePreview):
        PageKnowledgePreview.setObjectName("PageKnowledgePreview")
        PageKnowledgePreview.resize(700, 600)
        font = QtGui.QFont()
        font.setPointSize(7)
        PageKnowledgePreview.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(PageKnowledgePreview)
        self.verticalLayout.setContentsMargins(36, 36, 36, 9)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TopWidget = QtWidgets.QWidget(PageKnowledgePreview)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.TopWidget.setFont(font)
        self.TopWidget.setObjectName("TopWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.TopWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TitleWidget = QtWidgets.QWidget(self.TopWidget)
        self.TitleWidget.setObjectName("TitleWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.TitleWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.knowledgeTitle = TitleLabel(self.TitleWidget)
        self.knowledgeTitle.setObjectName("knowledgeTitle")
        self.verticalLayout_2.addWidget(self.knowledgeTitle)
        self.knowledgeInfoTitle = BodyLabel(self.TitleWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(False)
        self.knowledgeInfoTitle.setFont(font)
        self.knowledgeInfoTitle.setStyleSheet("color: #666666;")
        self.knowledgeInfoTitle.setObjectName("knowledgeInfoTitle")
        self.verticalLayout_2.addWidget(self.knowledgeInfoTitle)
        self.horizontalLayout.addWidget(self.TitleWidget)
        self.masteryRing = ProgressRing(self.TopWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.masteryRing.sizePolicy().hasHeightForWidth())
        self.masteryRing.setSizePolicy(sizePolicy)
        self.masteryRing.setMinimumSize(QtCore.QSize(70, 70))
        self.masteryRing.setMaximumSize(QtCore.QSize(70, 70))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(13)
        font.setBold(False)
        self.masteryRing.setFont(font)
        self.masteryRing.setProperty("value", 50)
        self.masteryRing.setTextVisible(True)
        self.masteryRing.setOrientation(QtCore.Qt.Horizontal)
        self.masteryRing.setInvertedAppearance(False)
        self.masteryRing.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.masteryRing.setUseAni(True)
        self.masteryRing.setVal(50.0)
        self.masteryRing.setObjectName("masteryRing")
        self.horizontalLayout.addWidget(self.masteryRing)
        self.verticalLayout.addWidget(self.TopWidget)
        self.SingleDirectionScrollArea = SingleDirectionScrollArea(PageKnowledgePreview)
        self.SingleDirectionScrollArea.setStyleSheet("border:1px solid rgba(120,120,120,80);border-radius:10px;background: rgba(0,0,0,0)")
        self.SingleDirectionScrollArea.setWidgetResizable(True)
        self.SingleDirectionScrollArea.setObjectName("SingleDirectionScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 626, 403))
        self.scrollAreaWidgetContents.setStyleSheet("border:0;background: rgba(0,0,0,0)")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.mainWidget = KnowledgeView(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainWidget.sizePolicy().hasHeightForWidth())
        self.mainWidget.setSizePolicy(sizePolicy)
        self.mainWidget.setObjectName("mainWidget")
        self.horizontalLayout_3.addWidget(self.mainWidget)
        self.SingleDirectionScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.SingleDirectionScrollArea)
        self.BottomWidget = QtWidgets.QWidget(PageKnowledgePreview)
        self.BottomWidget.setObjectName("BottomWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.BottomWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.testButton = PushButton(self.BottomWidget)
        self.testButton.setMinimumSize(QtCore.QSize(100, 0))
        self.testButton.setObjectName("examButton")
        self.horizontalLayout_2.addWidget(self.testButton)
        self.listenButton = PushButton(self.BottomWidget)
        self.listenButton.setMinimumSize(QtCore.QSize(100, 0))
        self.listenButton.setObjectName("listenButton")
        self.horizontalLayout_2.addWidget(self.listenButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.visibleToggleButton = TransparentToggleToolButton(self.BottomWidget)
        self.visibleToggleButton.setObjectName("visibleToggleButton")
        self.horizontalLayout_2.addWidget(self.visibleToggleButton)
        self.editButton = PushButton(self.BottomWidget)
        self.editButton.setMinimumSize(QtCore.QSize(100, 0))
        self.editButton.setObjectName("editButton")
        self.horizontalLayout_2.addWidget(self.editButton)
        self.verticalLayout.addWidget(self.BottomWidget)

        self.retranslateUi(PageKnowledgePreview)
        QtCore.QMetaObject.connectSlotsByName(PageKnowledgePreview)

    def retranslateUi(self, PageKnowledgePreview):
        _translate = QtCore.QCoreApplication.translate
        PageKnowledgePreview.setWindowTitle(_translate("PageKnowledgePreview", "Form"))
        self.knowledgeTitle.setText(_translate("PageKnowledgePreview", "Title label"))
        self.knowledgeInfoTitle.setText(_translate("PageKnowledgePreview", "x个知识块   上次复习x天前"))
        self.masteryRing.setFormat(_translate("PageKnowledgePreview", "%p%"))
        self.testButton.setText(_translate("PageKnowledgePreview", "测试"))
        self.listenButton.setText(_translate("PageKnowledgePreview", "随听"))
        self.editButton.setText(_translate("PageKnowledgePreview", "编辑"))
from pwidgets import KnowledgeView
from qfluentwidgets import BodyLabel, ProgressRing, PushButton, SingleDirectionScrollArea, TitleLabel, TransparentToggleToolButton
