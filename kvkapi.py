#!/usr/bin/python3
# -*-coding:utf-8 -*-
"""
@File    :   main.py
@Time    :   23.11.11
@Author  :   DrakHorse
@Version :   0.4.0a
@Contact :   https://github.com/DrakHorse
@License :   GNU GENERAL PUBLIC LICENSE
"""
import json
import os
import time


def getKnowledgeData():
    """
    获取知识点数据

    注意：该函数暂未完成，代码仅为实力
    """
    # TODO 清楚示例数据完成读取功能
    knowledge_lst = []
    for f in os.listdir(".\\knowledge\\"):
        file_data = json.loads(open(os.path.join(".\\knowledge", f), 'rb').read())
        knowledge_lst.append([
            f,
            file_data["name"],
            time.strftime("%y/%m/%d", time.gmtime(file_data["created_time"])),
            file_data["tags"],
            file_data["mastery_level"]
        ])

    return knowledge_lst
