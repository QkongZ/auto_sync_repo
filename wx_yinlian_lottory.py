import requests
from sendNotify import send
c_url = "https://members.95516.com/wxxcx/club/lottery/findLotteryHomePage"

d_url = "https://members.95516.com/wxxcx/club/lottery/drawLottery"

f_url = 'https://members.95516.com/wxxcx/club/user/findBaseUserInfo'

ckArr = []

data = {"activityId": "4881"}

def f(ck):

    headers = {

        "Host": "members.95516.com",

        "Connection": "keep-alive",

        "Content-Length": "21",

        "authorization": ck,

        "charset": "utf-8",

        "User-Agent": "Mozilla/5.0 (Linux; Android 13; M2012K11AC Build/TKQ1.220829.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 XWEB/1160065 MMWEBSDK/20230805 MMWEBID/4599 MicroMessenger/8.0.42.2460(0x28002A35) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android",

        "content-type": "application/json",

        "Accept-Encoding": "gzip,compress,br,deflate",

        "Referer": "https://servicewechat.com/wxec5bb43763e424a0/29/page-frame.html"

    }

    response = requests.post(f_url, headers=headers, json={}).json()
    msg.append(response['data']['serialNumber'])
    print(response['data']['serialNumber'])
    response = requests.post(c_url, headers=headers, json=data)
    chance = response.json()['data']['remainChance']

    if chance > 0:

        res = requests.post(d_url, headers=headers, json=data)
        res_data = res.json()
        if res_data["success"]:

            item_name = res_data["data"]["itemName"]

            print(item_name)
            msg.append(item_name)
        else:
            msg.append(res.text)
            print(res.text)

    else:

        print('暂无机会')
        msg.append('暂无机会')

if __name__ == "__main__":
    msg = []
    for x in ckArr:
        f(x)
    send('银联', '\n'.join(msg))
