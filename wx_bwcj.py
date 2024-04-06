
#!/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author : https://github.com/qingshanh/ymp
# @Time : 2022/8/10 13:23
# const $ = new Env("霸王茶姬签到");


import base64
import threading
from requests import post, get
from time import sleep, time
from datetime import datetime
from hashlib import md5 as md5Encode
from random import randint, uniform, choice, shuffle
from os import environ
from sys import stdout, exit
from base64 import b64encode
from json import dumps
from sendNotify import send
import re

now = datetime.now()
"""读取环境变量"""
bwcjck = environ.get("bwcjck") if environ.get("bwcjck") else True


"""主类"""
def print_now(content):
    print(content)
    msg.append(content)
    stdout.flush()

class bwcj:
    def __init__(self, ck):
        self.c = c
        self.ck = ck
        self.host = f'https://webapi.qmai.cn'
        self.headers = {
                'Accept': "v=1.0",
                'Content-Type': "application/json",
                'qm-from': "wechat",
                'xweb_xhr': "1",
                'qm-from-type': "catering",
                'sec-fetch-site': "cross-site",
                'sec-fetch-mode': "cors",
                'sec-fetch-dest': "empty",
                'referer': "https://servicewechat.com/wxafec6f8422cb357b/145/page-frame.html",
                'accept-language': "zh-CN,zh;q=0.9",
                'User-Agent' : 'Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20230805 MMWEBID/3684 MicroMessenger/8.0.42.2460(0x28002A35) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android',
                'Qm-User-Token' : self.ck,
        }
        #self.headers['Content-Length'] = str(len(self.json))
        self.main()


    def timestamp(self):
        return round(time() * 1000)

    

    def md5(self, str):
        m = md5Encode(str.encode(encoding='utf-8'))
        return m.hexdigest()

    def points_info(self):
        url = self.host + f'/web/catering/crm/points-info'
        json = {
            "appid": "wxafec6f8422cb357b"
        }
        
        try:
            res = post(url, headers = self.headers, json = json)

            if res.json()['code'] == '0':
                print_now(f"当前积分：{res.json()['data']['totalPoints']}")
                if res.json()['data']['expiredTime']:
                    print_now(f"{res.json()['data']['soonExpiredPoints']} 积分将于{res.json()['data']['expiredTime']}过期")
            else:
                print_now(res.text)
        except:
            print_now('查询积分出错了')
    
    def takePartInSign(self):
        url = self.host + '/web/cmk-center/sign/takePartInSign'
        json = {
            "activityId":"947079313798000641",
            "appid":"wxafec6f8422cb357b"
        }
        try:
            res = post(url, headers = self.headers, json = json)
            #print_now(res.text)
            if res.json()['code'] == 0:
                if 'rewardDetailList' in res.json()['data']:
                    res = res.json()['data']['rewardDetailList']
                    print_now('签到成功')
                    for r in res:
                        print_now(f"获得{r['rewardName']} {r['sendNum']}")
                else:
                    print_now(f"{res.json()['message']}")
            else:
                print_now(res.text)
        except:
            print_now('签到出错了')

    def userSignStatistics(self):
        url = self.host + '/web/cmk-center/sign/userSignStatistics'
        json = {
            "activityId":"947079313798000641",
            "appid":"wxafec6f8422cb357b"
        }
        try:
            resp = post(url, headers = self.headers, json = json)
            #print_now(res.text)
            if resp.json()['code'] == 0:
                if 'rewardList' in resp.json()['data']:
                    res = resp.json()['data']['rewardList']
                    #print(res)
                    for r in res:
                        if r['attain'] == 1:
                            print_now(f"签到 {r['signNum']} 天获得 {r['rewardList'][0]['sendNum']} {r['rewardList'][0]['rewardName']}：已完成")
                        elif r['attain'] == 2:
                            print_now(f"签到 {r['signNum']} 天获得 {r['rewardList'][0]['sendNum']} {r['rewardList'][0]['rewardName']}进度：{resp.json()['data']['signDays']}/{r['signNum']}")
                        else:
                            print_now(f'不知道咋回事：{r}')
                else:
                    print_now(f"{res.json()['message']}")
            else:
                print_now(res.text)
        except:
            print_now('查询签到奖励出错')

    def signIn_old(self):
        url = self.host + '/web/catering/integral/sign/signIn'
        json = {"activityId":"100820000000000686","mobilePhone":"16888888888","userName":"萧瑟","appid":"wxafec6f8422cb357b"}
        headers = {
            'Accept-Encoding' : 'gzip,compress,br,deflate',
            'Qm-From' : 'wechat',
            'Host' : 'webapi.qmai.cn',
            'store-id' : '49006',
            'Connection' : 'keep-alive',
            'User-Agent' : 'Mozilla/5.0',
            'Qm-User-Token' : self.ck,
            'Referer' : 'https://servicewechat.com/wxafec6f8422cb357b/83/page-frame.html',
            'Accept' : 'v=1.0',
            'Content-Type' : 'application/json',
            'Qm-From-Type' : 'catering',
            'scene' : '1089',
            'Content-Length' : '122',
        }
        try:
            res = post(url, headers = headers, json = json)
            #print(res.json())
            if res.json()['code'] == '0':
                print_now('旧版签到成功')
            else:
                print_now(f"旧版签到结果：{res.json()['message']}")

        except:
            print_now('旧版签到出错了')
            print(res.text)

    def main(self):
        
        self.points_info()
        self.takePartInSign()
        self.userSignStatistics()
        self.signIn_old()
        

if __name__ == "__main__":
    ckArr = []
    for ck in bwcjck.split('\n'):
        if len(ck) > 10:
            ckArr.append(ck)
    print('共' + str(len(ckArr)) + '个账户')
    c = 0
    u = []
    msg = []
    for i in ckArr:
        c += 1
        print(f"\n****************** 开始账号 {i.split('#')[1]} ******************\n")
        msg.append(f"\n******** 账号 {i.split('#')[1]} ********\n")
        bwcj(i.split('#')[0])
    print('\n\n')
    print('\n'.join(msg))
    send('霸王茶姬签到', '\n'.join(msg))
    exit(0)
