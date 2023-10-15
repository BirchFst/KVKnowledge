#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Created on 23.10.15

@author      : LeafJutN  Daniell233
@File        : project_widget.py
@Description : Unique widgets for the project interface.

Warning      : The following code comments are in Chinese!

"""
from PyQt5.QtWidgets import QPushButton, QWidget
import re


def ss_block_selector(style_sheet_string: str):
    """将样式表(CSS,QSS等)中的选择器分块"""
    # 准备样式表字符串
    text = "\n" + style_sheet_string

    # 替换换行符
    text = text.replace("\n", "&enter;")

    # 搜索选择器与样式表
    blocks = re.findall("&enter[^&{}]*\{[^{}]*}", text)

    # 转回将每个块的换行符
    blocks = [i.replace("&enter;", "\n") for i in blocks]

    return blocks


def ss_block_to_dict(style_sheet_string: str):
    """将样式表(CSS,QSS等)中的选择器块转为python字典"""

    text = style_sheet_string.replace("\n", "")  # 去除换行符

    head = re.match("^(.*?)\{", text).group(1).strip()  # 获取选择器
    text = re.search("\{(.*?)}", text)[0].strip()[1:-1]  # 去除大括号

    text_list = text.split(";")  # 去除分号并转为列表

    # 以冒号分割转为字典，并去除首位空格
    text_dict = {i.split(":")[0].strip(): i.split(":")[1].strip() for i in text_list if ":" in i}

    return {head: text_dict}


def dict_to_ss_block(style_dict: dict) -> str:
    """将Python字典转为样式表(CSS, QSS等)中的选择器块字符串"""

    selector = list(style_dict.keys())[0]  # 获取选择器

    properties = style_dict[selector]  # 获取属性字典

    # 将属性字典转换为样式表字符串
    properties_str = ""
    for key, value in properties.items():
        properties_str += f"{key}: {value}; "

    return f"{selector} {{ {properties_str}}}"


def change_ss(root: str, key: str, value: str):
    """更改样式表其中的元素"""
    d = ss_block_to_dict(root)
    d[list(d.keys())[0]][key] = value

    return dict_to_ss_block(d)


class QssWidget(QWidget):
    """能够以example[key]=value格式设置与更改QSS的QWidget"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._qss = {".QssWidget": {}}
        self._selector = ".QssWidget"
        self._root_ss = ""

    def __getitem__(self, key):
        return self._qss[list(self._qss.keys())[0]][key]

    def __setitem__(self, key, value):
        self._qss[list(self._qss.keys())[0]][key] = value
        self.setStyleSheet(dict_to_ss_block(self._qss))

    def setRootStyleSheet(self, ss):
        self._qss = ss_block_to_dict(ss)
        self._root_ss = ss
        self.setStyleSheet(ss)

    def returnToRootStyleSheet(self):
        self.setStyleSheet(self._root_ss)
        self._qss = ss_block_to_dict(self._root_ss)

    def setSelectorName(self, selector):
        d = self._qss[self._selector]
        self._qss = {selector: d}
        self._selector = selector


class PSideButton(QPushButton, QssWidget):
    """侧边栏按钮"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initWidget()
        self.setSelectorName("PSideButton")

    def initWidget(self):
        self.setMinimumHeight(30)
        pass

    def enterEvent(self, a0):
        self["background"] = "#FFFFFF"
        self["border"] = "5px solid #000000"
        print(self.styleSheet())
