'''
mt论坛签到

'''

import time, random
import requests, json, re, os
from sendNotify import send
# 这里填写COOKIE
mt_cookie = os.getenv("mt")


def mt(cookie):
    login_url = 'https://bbs.binmt.cc/k_misign-sign.html'
    sign_url = f'https://bbs.binmt.cc/plugin.php?id=k_misign:sign&operation=qiandao&format=text&formhash='
    a_url = 'https://bbs.binmt.cc/member.php?mod=logging&action=login&infloat=yes&handlekey=login&inajax=1&ajaxtarget=fwin_content_login'
    header = {

        'referer': 'https://bbs.binmt.cc/k_misign-sign.html',
        'cookie' : cookie,
        'User-agent': 'Mozilla/5.0 (Linux; Android 12.0.1; zh-cn; Pixel 6 Pro; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.4758.46 Mobile Safari/537.36 SearchCraft/3.7.0 (Baidu; P1 9)'
    }
   # try:
    info_html = requests.get(url=login_url, headers=header).text
    #print(info_html)
    if '请登录或注册' not in info_html:
        formhash = re.findall('formhash=(.*?)&', info_html)[0]
        username = re.findall('user_tit fyy">(.*?)<', info_html)[0]
        jifen = re.findall('class="fyy">(积分.*?)<', info_html)[0]
        jinripaiming = re.findall('comiis_tm">今日排名</span>(.*?)<', info_html)[0]
        lianxusign = re.findall('comiis_tm">连续签到</span>(.*?)<', info_html)[0]
        leijisign = re.findall('comiis_tm">累计签到</span>(.*?)<', info_html)[0]
        print(f'账号 {username} {jifen}')
        msg.append(f'账号 {username} {jifen}')
        print(f'今日排名/连续/累计签到：{jinripaiming}/{lianxusign}/{leijisign}')
        msg.append(f'今日排名/连续/累计签到：{jinripaiming}/{lianxusign}/{leijisign}')
        if '已签到' not in info_html:
            print('今日未签到，准备去签到。。。')
            msg.append('今日未签到，准备去签到。。。')
            sign_html = requests.get(url=sign_url+formhash, headers=header).text
            qd = re.findall('<root><(.*?)></root>', sign_html)[0]
            msg.append(f'签到结果：{qd}')
            print(f'签到结果：{qd}')
        #else:
    else:
        msg.append('登录失败，ck可能失效')
        print('登录失败，ck可能失效')
'''
    except:
        content = '签到失败，可能COOKIE失效'
        print(content)
        '''
if __name__ == "__main__":
    cookies = mt_cookie.split("\n")
    msg = f"共获取到{len(cookies)}个账号"
    print(msg)
    msg = []
    for i, cookie in enumerate(cookies, start = 1):
        print(f"\n\n======== ▷ 第 {i} 个账号 ◁ ========\n")
        msg.append(f"\n\n======== ▷ 第 {i} 个账号 ◁ ========\n")
        mt(cookie)
        print("\n随机等待5-10s进行下一个账号")
        if i < len(cookies):
            time.sleep(random.randint(5, 10))
    send('MT论坛签到', '\n'.join(msg))
