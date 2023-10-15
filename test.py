#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 23.10.15

@author      : LeafJutN  Daniell233
@File        : test.py
@Description : Program testing environment, please do not package this file.

Warning      : The following code comments are in Chinese!
"""

import os
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    """编译UI文件"""
    os.system(
        "python3 -m PyQt5.uic.pyuic ./UiResources/ui.ui -o ./ui_output.py")

    """实例化并运行"""
    from ui_control import MainWindow

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
