#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 23.10.15

@author      : LeafJutN  Daniell233
@File        : ui_control.py
@Description : Front end control program.

Warning      : The following code comments are in Chinese!

"""
from PyQt5.QtWidgets import QMainWindow
import ui_output

QSS_PATH = "UiResources/qss/light.qss"  # 选中的QSS路径


class MainWindow(QMainWindow, ui_output.Ui_MainWindow):
    """主窗口类"""

    def __init__(self):
        super(MainWindow, self).__init__()

        # 实例化UI文件
        self.setupUi(self)

        # 附加QSS
        self.setStyleSheet(open(QSS_PATH, "r", encoding="utf-8").read())

