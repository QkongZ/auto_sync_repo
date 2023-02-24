#const $ = new Env('tly签到')
import time
import requests
import base64
import json
import random
from datetime import datetime
from os import environ
from sys import stdout, exit
from sendNotify import send
cookies=environ.get('tlyck') if environ.get('tlyck') else '' #账号cookie
if cookies:
    cookieArr = cookies.split('\n')
else:
    print('未填写cookie，退出')
    exit(0)
token='' #验证码token
captcha_username = environ.get('captcha_username') if environ.get('captcha_username') else ''
captcha_pwd = environ.get('captcha_pwd') if environ.get('captcha_pwd') else ''

#session_name = API_ID[:]
if captcha_username and captcha_pwd:
    captcha_usernameArr = captcha_username.split('&')
    captcha_pwdArr = captcha_pwd.split('&')
#token在http://www.bhshare.cn/imgcode/ 自行申请
def print_now(content):
    print(content)
    stdout.flush()

def sj(a, b):
    return random.randint(a, b)
    
def captcha_solver(base64data):
    '''
    with open('./captcha.jpg', 'rb') as tp:
        base64data = base64.b64encode(tp.read())
        #print_now(base64data)
        '''
    captcha_url = 'https://api.apitruecaptcha.org/one/gettext'
    c = random.randint(0, len(captcha_usernameArr) - 1)
    print_now('本次调用账号' + captcha_usernameArr[c])
    data = {
        "userid":captcha_usernameArr[c],
        "apikey":captcha_pwdArr[c],
        'case':'lower',
        "data":base64data
    }
    #print_now(str(base64data.decode('utf-8'))) #'data:image/jpeg;base64,' +  
    try:
        response = requests.post(url=captcha_url, json=data)
        #print_now(response.json())
        solved_result = ''
        if response.json()["result"]:
            print('识别验证码成功')
            solved_result = response.json()["result"]
        else:
            solved_result = '2bf2'
            print_now('识别图片验证码失败，输入2b尝试')

        return solved_result
        #return base64data
    except:
        print_now('验证码识别平台无回应，随便返回一个结果')
        return str(sj(10000,99999))


def imgcode_online(imgurl):
    data = {
   
        'token': token,
        'type': 'online',
        'uri': imgurl
    }
    response = requests.post('http://www.bhshare.cn/imgcode/', data=data)
    print(response.text)
    result = json.loads(response.text)
    if result['code'] == 200:
        print(result['data'])
        return result['data']
    else:
        print(result['msg'])
        return 'error'


def getmidstring(html, start_str, end):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()




def tly(cookie):
    usr = getmidstring(cookie, 'user_email=',';').replace('%40','@')
    print(f'\n开始账号 {usr}\n')
    msg.append(f'\n账号 {usr}\n')
    signUrl="https://tly30.com/modules/index.php"
    hearder={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36','Cookie':cookie}

    res=requests.get(url=signUrl,headers=hearder).text
    zongliuliang = getmidstring(res,'本月总量：','</p>')
    shengyu =  getmidstring(res,'剩余流量：','</p>')
    print(f'剩余流量/总流量：{shengyu}/{zongliuliang}')
    msg.append(f'剩余流量/总流量：{shengyu}/{zongliuliang}')
    signtime=getmidstring(res,'<p>上次签到时间：<code>','</code></p>')
    timeArray = time.strptime(signtime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    t = int(time.time())

    if t-timeStamp>86400:
        print("距上次签到时间大于24小时啦,可签到")
        #获取验证码图片
        captchaUrl="https://tly30.com/other/captcha.php"
        signurl="https://tly30.com/modules/_checkin.php?captcha="
        hearder={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36','Cookie':cookie}
        res1=requests.get(url=captchaUrl,headers=hearder)
        base64_data = base64.b64encode(res1.content)
        oocr=captcha_solver('data:image/jpeg;base64,'+str(base64_data, 'utf-8'))
        
        res2=requests.get(url=signurl+oocr,headers=hearder).text
        print(res2)
        if '获得了' in res2:
            jg = getmidstring(res2,"alert('","')")
            print(f'签到成功 {jg}')
            msg.append(f'签到成功 {jg}')
            send('tly签到', '\n'.join(msg))
    else:
        print("还未到时间！还需等待",f'{round((86400-(t-timeStamp))/3600,2)}h')




   


if __name__ == "__main__":
    msg = []
    for ck in cookieArr:
        if len(ck) > 10:
            tly(ck)
