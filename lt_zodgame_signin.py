# -*- coding: utf-8 -*-
# python版本 >=3.8
# cron "10 1 * * *" co_zodgame.py, tag: Gtloli 社区签到
import os
import requests
import asyncio
from sendNotify import send
from bs4 import BeautifulSoup
import re

cookie = os.getenv('ZODGAME_COOKIES')
if cookie is None:
    print('请设置环境变量 ZODGAME_COOKIES')
    send('ZODGAME 签到执行失败！', '请设置环境变量 ZODGAME_COOKIES')
    exit(1)
cookies = []
for line in cookie.split('\n'):
    #name, value = line.strip().split('=', 1)
    if len(line) > 10:
        cookies.append(line)
        

def task(c):
    notify_message = '[ZODGAME 签到结果]\n'
    cookie = c
    print('获取 Formhash...')
    r = requests.get('https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
        'Referer': 'https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
        'cookie': cookie,
    })
    if r.status_code != 200:
        raise Exception('获取 Formhash 失败！')
    pattern = r'formhash" value="([0-9a-z]+)"'
    formhash = re.search(pattern, r.text)[1]
    print('formhash: {}'.format(formhash))
    print('执行社区签到任务...')
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': cookie,
        'origin': 'https://zodgame.xyz',
        'referer': 'https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }
    data = {
        'formhash': formhash,
        'qdxq': 'fd',
    }
    response = requests.post('https://zodgame.xyz/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1', headers=headers, data=data).text
    yonghuzu = ''
    jifen = ''
    if '用户组' in response:
        yonghuzu = re.search(r'>(用户组:.*?)<', response)[1]
    if '积分' in response:
        jifen = re.search(r'>(积分:.*?)<', response)[1]
    #print(jifen)
    #print(response)
    if '已经签到' in response:
        if yonghuzu:
            print(yonghuzu)
        if jifen:
            print(jifen)
        print('今日已签到')
    else:
        print(response)
    notify_message += '社区签到: ' + ' ' + response + '\n'
    send('[ZODGAME] 签到完成', notify_message)





if __name__ == '__main__':
    for c in cookies:
        task(c)
