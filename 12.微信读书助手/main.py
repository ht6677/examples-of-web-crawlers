#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: main.py
@author: Shengqiang Zhang
@time: 2020/4/11 02:32
@mail: sqzhang77@gmail.com
"""


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile,QWebEngineSettings,QWebEnginePage
import sys
import json
import requests
import time


def get_notebooklist(headers):
    """获取笔记书单"""
    url = "https://i.weread.qq.com/user/notebooks"
    r = requests.get(url,headers=headers,verify=False)

    if r.ok:
        data = r.json()
        print(data)
    else:
        data = r.json()
        print(data)
        # raise Exception(r.text)
    # books = []
    # for b in data['books']:
    #     book = b['book']
    #     b = Book(book['bookId'],book['title'],book['author'],book['cover'],book['category'])
    #     books.append(b)
    # books.sort(key=itemgetter(-1))
    # return books


def login_success(headers):
    """判断是否登录成功"""
    url = "https://i.weread.qq.com/user/notebooks"
    r = requests.get(url,headers=headers,verify=False)

    if r.ok:
        return True
    else:
        return False



class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.DomainCookies = {}

        self.setWindowTitle('微信读书助手') # 设置窗口标题
        self.resize(900, 600) # 设置窗口大小
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint) # 禁止最大化按钮
        self.setFixedSize(self.width(), self.height()) # 禁止调整窗口大小

        url = 'https://weread.qq.com/#login' # 目标地址
        self.browser = QWebEngineView() # 实例化浏览器对象

        QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies() # 初次运行软件时删除所有cookies

        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd) # cookies增加时触发self.onCookieAdd()函数
        self.browser.loadFinished.connect(self.onLoadFinished) # 网页加载完毕时触发self.onLoadFinished()函数

        self.browser.load(QUrl(url)) # 加载网页
        self.setCentralWidget(self.browser) # 设置中心窗口



    # 网页加载完毕事件
    def onLoadFinished(self):

        # 获取cookies
        cookies = ['{}={};'.format(key, value)for key,value in self.DomainCookies.items()]
        cookies = ' '.join(cookies)

        # 设置header
        headers = {
            'Host': 'i.weread.qq.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

        # 添加Cookie到header
        headers.update(Cookie=cookies)


        # 判断是否成功登录微信读书
        if login_success(headers):
            print('登录微信读书成功!')
            exit()
        else:
            print('请扫描二维码登录微信读书...')


    # 添加cookies事件
    def onCookieAdd(self, cookie):
        if 'weread.qq.com' in cookie.domain():
            name = cookie.name().data().decode('utf-8')
            value = cookie.value().data().decode('utf-8')
            if name not in self.DomainCookies:
                self.DomainCookies.update({name: value})


    # 窗口关闭事件
    def closeEvent(self, event):
        """
        重写closeEvent方法，实现窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """

        self.setWindowTitle('退出中……')  # 设置窗口标题

        # 关闭软件软件之前删除所有cookies
        # 此代码不可删除，否则下次打开软件会自动加载浏览器中旧的cookies
        QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies()




if __name__=='__main__':

    # 创建应用
    app = QApplication(sys.argv)
    # 创建主窗口
    window = MainWindow()
    # 显示窗口
    window.show()
    # 运行应用，并监听事件
    app.exec_()