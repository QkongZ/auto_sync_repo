## const $ = new Env("小白下载签到");
import requests
from os import environ
from sendNotify import send
msg = []
xbcookie = environ.get("xbxz") if environ.get("xbxz") else True
def xb(ck):
    url = "https://xb.xiaobaigongju.com/v1/app/m/sign/add"

    headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.43 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/29.09091)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'thirdSession': ck
    }

    response = requests.post(url, headers=headers)
    print(response.json())
    msg.append(response.json()['msg'])

if __name__ == "__main__":
    ckArr = []
    for ck in xbcookie.split('\n'):
        if len(ck) > 5:
            ckArr.append(ck)
    print('共' + str(len(ckArr)) + '个账户')
    c = 0
    for ck in ckArr:
        c += 1
        msg.append(f'\n**********账号{c}**********\n')
        print(f'\n**********开始账号{c}**********\n')
        xb(ck)
    #shuffle(phone_numArr)
    #print(mtckArr)
    u = []
    print('\n'.join(msg))
    send('小白下载签到', '\n'.join(msg))
    exit(0)
