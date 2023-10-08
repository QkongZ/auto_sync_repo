#!/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author : https://github.com/qingshanh/ymp
# @Time : 2023/10/8 20:23
# const $ = new Env("今日热榜");

import base64
import threading
import string, random
from requests import post, get
from time import sleep, time
import datetime
from hashlib import md5 as md5Encode
from random import randint, uniform, choice, shuffle
from os import environ
from sys import stdout, exit
from base64 import b64encode
from json import dumps
from sendNotify import send
import re

salt = 'aA4@ud^926U(}^r9'
msg = []
tophub = environ.get("tophub") if environ.get("tophub") else True

"""主类"""
def print_now(content):
    print(content)
    stdout.flush()
    msg.append(content)

def timestamp():
    return round(time())  

def md5(str):
    m = md5Encode(str.encode(encoding='utf-8'))
    return m.hexdigest()
def generate_random_string(length=16):
    # 定义字符集，包括大写字母、小写字母和数字
    characters = string.ascii_letters + string.digits
    # 生成指定长度的随机字符串
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def get_date_as_eight_digit_string():
    # 获取当前日期
    current_date = datetime.date.today()    
    # 将日期格式化为八位数字（YYYYMMDD）
    formatted_date = current_date.strftime("%Y%m%d")  
    return formatted_date
class jrrb:
    def __init__(self, ck):
        self.ck = ck
        self.url = f'https://api2.tophub.app'
        self.headers = {
            'Host': 'api2.tophub.app', 
            'authorization': self.ck ,
            'accept': 'application/vnd.tophub.v1+json' ,
            'user-agent': 'TophubApp/1.0 Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36' ,
            'x-network-type': 'NETWORK_WIFI' ,
            'accept-encoding': 'gzip',
        }
        #self.headers['Content-Length'] = str(len(self.json))

    def info(self):
        ti = timestamp()
        nonce = generate_random_string()
        jm = md5(f'{self.url}/my/profilenonce={nonce}&timestamp={ti}{salt}')
        url = f'{self.url}/my/profile?nonce={nonce}&sign={jm}&timestamp={ti}'
        res = get(url, headers = self.headers).json()    
        if res['status'] == 200 and res['error'] == False:
            res = res['data']
            print_now(f"用户 {res['username']}\n剩余/总金币：{res['remain_coins']}/{res['total_coins']}")
        else:
            print(res)
    def checkin(self):
        ti = timestamp()
        nonce = generate_random_string()
        jm = md5(f'{self.url}/account/taskchannel=CHECKIN&nonce={nonce}&timestamp={ti}{salt}')
        url = f'{self.url}/account/task'
        body = {
            'channel': 'CHECKIN',
            'nonce': nonce,
            'sign': jm,
            'timestamp': ti
        }

        res = post(url, headers = self.headers, data = body).json()
        if res['status'] == 200 and res['error'] == False:
            res = res['data']
            if res["coins"] > 0:
                print_now(f"签到获得金币：{res['coins']}")
            else:
                print_now(res["msg"])
        else:
            print_now(res)
    def read(self):
        ti = timestamp()
        nonce = generate_random_string()
        jm = md5(f'{self.url}/account/taskchannel=READ&nonce={nonce}&timestamp={ti}{salt}')
        url = f'{self.url}/account/task'
        body = {
            'channel': 'READ',
            'nonce': nonce,
            'sign': jm,
            'timestamp': ti
        }

        res = post(url, headers = self.headers, data = body).json()
        if res['status'] == 200 and res['error'] == False:
            res = res['data']
            print(res)
            print_now(f"阅读获得金币：{res['coins']}")
        else:
            print_now(res)
    def share(self):
        ti = timestamp()
        nonce = generate_random_string()
        jm = md5(f'{self.url}/account/taskchannel=SHARE&nonce={nonce}&timestamp={ti}{salt}')
        url = f'{self.url}/account/task'
        body = {
            'channel': 'SHARE',
            'nonce': nonce,
            'sign': jm,
            'timestamp': ti
        }
        res = post(url, headers = self.headers, data = body).json()
        if res['status'] == 200 and res['error'] == False:
            res = res['data']
            print_now(f"分享获得金币：{res['coins']}")
        else:
            #print_now('分享任务已完成')
            print_now(res)    
    def stat(self):
        ti = timestamp()
        nonce = generate_random_string()
        day = get_date_as_eight_digit_string()
        jm = md5(f'{self.url}/hot/itemday={day}&limit=7&nonce={nonce}&timestamp={ti}{salt}')
        url = f'{self.url}/hot/item?day={day}&limit=7&nonce={nonce}&sign={jm}&timestamp={ti}'
        idArr = []
        res = get(url, headers = self.headers).json()
        if res['status'] == 200 and res['error'] == False:
            res = res['data']
            #print(res)
            for x in res['items']:
                idArr.append(x['ID'])
                if len(idArr)>21:
                    break
            print(f'获取{len(idArr)}篇文章')
            for d in idArr:
                t = timestamp()
                non = generate_random_string()
                j = md5(f'{self.url}/statnonce={non}&t=item&tid={d}&timestamp={t}{salt}')
                u = f'{self.url}/stat'
                body = {
                    'nonce': non,
                    'sign': j,
                    't': 'item',
                    'tid': d,
                    'timestamp': t
                }  
                r = post(u, headers = self.headers, data = body).json()
                if r['status'] == 200 and r['error'] == False:
                    #print('阅读成功')  
                    continue
                    print(r)
            self.read()
                
            #print_now(f"分享获得金币：{r['coins']}")
        else:
            #print_now('分享任务已完成')
            print_now(res)
    def main(self):
        self.info()
        self.checkin()
        self.share()
        self.stat()


if __name__ == "__main__":
    ckArr = []
    for ck in tophub.split('\n'):
        if len(ck) > 5:
            ckArr.append(ck)
    print('共' + str(len(ckArr)) + '个账户')
    c = 0
    for ck in ckArr:
        c += 1
        print_now(f'\n**********开始账号{c}**********\n')
        jrrb = jrrb(ck)
        jrrb.main()
    #shuffle(phone_numArr)
    #print(mtckArr)
    u = []
    print('\n'.join(msg))
    send('今日热榜', '\n'.join(msg))
    exit(0)
