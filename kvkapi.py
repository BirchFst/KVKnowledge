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
import os
import pyttsx3
import time
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse, urlencode
import ssl
import websocket
from wsgiref.handlers import format_date_time  # noqa
from time import mktime

# 创建星火Api密钥
SD_APP_ID = "your_app_id"
SD_API_SECRET = "your_api_secret"
SD_API_KEY = "your_api_key"
DEBUG_MODE = False
exec(open(".\\ApiData").read(), globals(), globals())

sd_answer = ""


class WsParam:
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    def create_url(self):
        date = format_date_time(mktime(datetime.datetime.now().timetuple()))
        signature_sha = hmac.new(
            self.APISecret.encode('utf-8'),
            ("host: " + self.host + "\n" + "date: " + date + "\n" + "GET " + self.path + " HTTP/1.1").encode('utf-8'),
            digestmod=hashlib.sha256,
        ).digest()
        authorization = base64.b64encode(
            (f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", '
             f'signature="{base64.b64encode(signature_sha).decode(encoding="utf-8")}"').encode('utf-8')).decode(
            encoding='utf-8')
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        return self.Spark_url + '?' + urlencode(v)


def _socket_on_error(ws, error):  # noqa
    print("### error:", error)


def _socket_on_close(ws, one, two):  # noqa
    print(" ")


def _socket_on_open(ws):
    thread.start_new_thread(_thread_run, (ws,))


def _thread_run(ws, *args):  # noqa
    data = json.dumps(_gen_params(appid=ws.appid, domain=ws.domain, question=ws.question))
    ws.send(data)


def _socket_on_message(ws, message):
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        global sd_answer
        sd_answer += content
        if status == 2:
            ws.close()


def _gen_params(appid, domain, question):
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {
            "chat": {
                "domain": domain,
                "random_threshold": 0.5,
                "max_tokens": 1024,
                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


def sd_request(appid, api_key, api_secret, Spark_url, domain, question):
    wsParam = WsParam(appid, api_key, api_secret, Spark_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=_socket_on_message, on_error=_socket_on_error,
                                on_close=_socket_on_close, on_open=_socket_on_open)
    ws.appid = appid
    ws.question = question
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


def sd_correct(question: str, correct_answer: str, students_answer: str):
    global SD_APP_ID, SD_API_KEY, SD_API_SECRET, sd_answer

    if DEBUG_MODE:
        return """
        {"result": true,"describe": "DEBUG MODE ENABLED"}"""

    question = [{
        "role": "user",
        "content": "I need you to help me grade my homework. I will provide you with a JSON format assignment that "
                   "includes questions, correct answers, and student answers\n"
                   "You only need to return JSON data, which contains' result ': correct or incorrect as a Boolean"
                   "value, and can contain a parsing description in string form' describe ',If the problem is in "
                   "Chinese, you can also explain it in Chinese,"
                   "Note: The answers to most questions (especially subjective questions) do not need to be word for "
                   "word"
                   "{\n"
                   f"question: \"{question}\",\n"
                   f"correct_answer: \"{correct_answer}\",\n"
                   f"students_answer: \"{students_answer}\"\n"
                   "}"
    }]
    sd_answer = ""
    sd_request(SD_APP_ID, SD_API_KEY, SD_API_SECRET, "ws://spark-api.xf-yun.com/v2.1/chat", "generalv2", question)
    return sd_answer


def getKnowledgeData():
    """
    获取知识库数据
    """
    knowledge_lst = []
    for f in os.listdir(".\\knowledge\\"):
        file_data = json.loads(open(os.path.join(".\\knowledge", f), 'rb').read())
        knowledge_lst.append([
            f,
            file_data["name"],
            time.strftime("%Y.%m.%d", time.gmtime(file_data["last_review_time"])),
            file_data["tags"],
            file_data["mastery_level"]
        ])

    return knowledge_lst


def textToSpeech(text, path, rate=200):
    """
    Pyttsx3 文本音频生成保存为mp3文件

    :param text: 文本
    :param path: 保存路径
    :param rate: 语速
    """
    engine = pyttsx3.init()  # 初始化语音引擎
    engine.setProperty('rate', rate)  # 设置语速
    engine.setProperty('voice', engine.getProperty('voices')[0].id)

    engine.save_to_file(text, path)
    engine.runAndWait()


def readText(path):
    """
    使用EasyOCR读取文字

    :param path: 图片路径
    """
    try:
        cv2  # noqa
        easyocr  # noqa
    except NameError:
        import cv2
        import easyocr

    img = cv2.imread(path)  # 使用OpenCV二值化图片
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转成灰度图片
    cv2.imwrite(".\\BINARY_PHOTO.png", img[1])  # 保存为暂存图片
    # 实例化EasyOCR阅读器
    reader = easyocr.Reader(["ch_sim", "en"], gpu=True)
    result = reader.readtext(".\\BINARY_PHOTO.png", detail=0)  # 识别文本

    return '\n'.join(result) if result else ""
