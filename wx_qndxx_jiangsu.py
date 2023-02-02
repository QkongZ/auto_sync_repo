#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yuzai
@file:Qndxx.py   https://github.com/yuzaii/JsQndxx_Python
@time:2022/09/17
new Env('江苏青年大学习');
"""
import json
import re

import requests
from bs4 import BeautifulSoup
from os import environ
from sendNotify import send


laravel_session = environ.get('laravel_session')

if (len(laravel_session) == 0):
    print('没有 laravel_session ，退出运行')
    exit(0)

laravel_sessionArr = laravel_session.split('&')





class Qndxx:
    def __init__(self, laravel_session):
        # 需要传入的laravel_session
        self.laravel_session = laravel_session
        # 请求头
        self.UA = "Mozilla/5.0 (Linux; Android 11; M2012K11AC Build/RKQ1.200826.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3263 MMWEBSDK/20220105 Mobile Safari/537.36 MMWEBID/4883 MicroMessenger/8.0.19.2080(0x2800133D) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64"
        # 江苏省青年大学习接口
        self.loginurl = "https://service.jiangsugqt.org/youth/lesson"
        # 确认信息接口
        self.confirmurl = "https://service.jiangsugqt.org/youth/lesson/confirm"
        # 创建会话
        self.session = requests.session()  # 创建会话
        # 构建用户信息字典
        self.userinfo = {}

    def get_userinfo(self, userinfo):
        # print(userinfo)
        for i in userinfo:
            # print(i)
            # 解析课程姓名编号单位信息
            info_soup = BeautifulSoup(str(i), 'html.parser')
            # print(info_soup.text)
            item = info_soup.get_text()  # 用户信息
            # print(item[:4],item[5:])
            self.userinfo[item[:4]] = item[5:]
        # print(self.userinfo)

    def confirm(self):
        params = {
            "_token": self.userinfo.get('token'),
            "lesson_id": self.userinfo.get('lesson_id')
        }
        # print(params)
        confirm_res = self.session.post(url=self.confirmurl, params=params)
        res = json.loads(confirm_res.text)
        print(f"返回结果:{res}")
        if res["status"] == 1 and res["message"] == "操作成功":
            print("青年大学习已完成")
            print(f"您的信息:{self.userinfo}")
        else:
            raise Exception(f"确认时出现错误:{res['message']}")

    def login(self):
        # 参数
        params = {
            "s": "/youth/lesson",
            "form": "inglemessage",
            "isappinstalled": "0"
        }
        # 构造请求头
        headers = {
            'User-Agent': self.UA,
            'Cookie': "laravel_session=" + self.laravel_session  # 抓包获取
        }
        # 登录
        login_res = self.session.get(url=self.loginurl, headers=headers, params=params)

        # print(login_res.text)
        if '抱歉，出错了' in login_res.text:
            print("laravel_session错误")
            
            send('江苏青年大学习', 'laravel_session出错，可能过期，请重新抓取')
            exit(0)
            raise Exception("laravel_session错误")
        # 正则匹配token和lesson_id
        token = re.findall(r'var token ?= ?"(.*?)"', login_res.text)  # 获取js里的token
        lesson_id = re.findall(r"'lesson_id':(.*)", login_res.text)  # 获取js里的token

        self.userinfo['token'] = token[0]
        self.userinfo['lesson_id'] = lesson_id[0]
        # 解析信息确认页面
        login_soup = BeautifulSoup(login_res.text, 'html.parser')
        # print(soup.select(".confirm-user-info"))
        # 找到用户信息div 课程姓名编号单位
        userinfo = login_soup.select(".confirm-user-info p")
        # print(userinfo)
        self.get_userinfo(userinfo)

if __name__ == '__main__':
    print('共' + str(len(laravel_sessionArr)) + '个账户')
    x = 0
    for i in laravel_sessionArr:
        x = x + 1
        print(f'\n账号{x}：')
        laravel_session = i
        qndxx = Qndxx(laravel_session)
        qndxx.login()
        qndxx.confirm()
