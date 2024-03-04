'''
const $ = new Env("南航签到");

'''

import os, time
import requests
from datetime import datetime
from calendar import monthrange

# 假设你有一个sendNotify.py文件，其中包含了send函数
from sendNotify import send

token = os.environ.get('nanhan')
msg = []

def csairSign():
    if not token:
        print('请填写token')
        exit(0)

    # 签到
    now = time.time()
    createTime = int(now * 1000)

    url = "https://wxapi.csair.com/marketing-tools/activity/join"
    params = {"type": "APPTYPE", "chanel": "ss", "lang": "zh"}
    json_data = {"activityType": "sign", "channel": "app", "entrance": None}
    headers = {
        "Content-Type": "application/json",
        
    cookies = {
        "sign_user_token": token,
        "TOKEN": token,
        "cs1246643sso": token,
    }

    res = requests.post(url, params=params, json=json_data, headers=headers, cookies=cookies)

    if res.status_code == 200:
        try:
            info = res.json()
            if info.get("respCode") == "S00011":
                print('token可能失效')
                msg.append('token可能失效')

            if info.get("respCode") == "S2001":
                print('今天已签到！')
                msg.append('今天已签到！')
            else:
                print(info.get("respMsg"))
                msg.append(info.get("respMsg"))

            # 奖励列表
            url = "https://wxapi.csair.com/marketing-tools/award/awardList?envVersion=release"
            json_data = {"activityType": "sign", "awardStatus": "all", "pageNum": 1, "pageSize": 100}
            res = requests.post(url, json=json_data, headers=headers, cookies={"sign_user_token": token})
            if res.status_code == 200 and res.json():
                #print(res.json()["data"])
                for d in res.json()["data"]["list"]:
                    print(f'{d["activityName"]}：{d["awardName"]}')
                    msg.append(f'{d["activityName"]}：{d["awardName"]}')
            else:
                print(res.text)
                msg.append(res.text)

        except Exception as e:
            print(f'南航签到程序异常 {e}')
            msg.append(f'南航签到程序异常 {e}')

    # 签到日历
    month_start = datetime(datetime.now().year, datetime.now().month, 1).strftime("%Y%m%d")
    month_end = datetime(datetime.now().year, datetime.now().month,
                         monthrange(datetime.now().year, datetime.now().month)[1]).strftime("%Y%m%d")
    url= f"https://wxapi.csair.com/marketing-tools/sign/getSignCalendar?envVersion=release&startQueryDate={month_start}&endQueryDate={month_end}"

    res = requests.get(url, headers = headers, cookies = {"sign_user_token": token})
    if res:
        try:
            info = res.json()
            if info.get("respCode") == "0000":
                print(f'南航用户：{token} \n{info["data"]["dateList"]} 已签到\n{"".join(info["data"]["signProgressMsg"])}')
                msg.append(f'{info["data"]["dateList"]} 已签到 \n{"".join(info["data"]["signProgressMsg"])}')
            else:

                print(f'{token} {info.get("respMsg", "")}')
                msg.append(f'{token} {info.get("respMsg", "")}')
        except Exception as e:
            print(f'南航签到异常 {e}')
            msg.append(f'南航签到异常 {e}')
    else:
        print(res.text)

    send("南航签到", "\n".join(msg))

csairSign()
