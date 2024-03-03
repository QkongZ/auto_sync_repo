import requests
import json
from sendNotify import send
msg= []
url = "https://vtravel.link2shops.com/vfuliApi/api/client/ypJyActivity/goodsList"

payload = json.dumps({
  "activityTag": "ccbyyg",
  "catagoryId": ""
})

headers = {
  'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6309092b) XWEB/8555 Flue",
  'Accept': "application/json, text/plain, */*",
  'Content-Type': "application/json",
  'token': "[object Object]",
  'Origin': "https://vtravel.link2shops.com",
  'Sec-Fetch-Site': "same-origin",
  'Sec-Fetch-Mode': "cors",
  'Sec-Fetch-Dest': "empty",
  'Accept-Language': "zh-CN,zh;q=0.9",
}

response = requests.post(url, data=payload, headers=headers)
try:
    #print(response.json()['code'])
    if response.json()['code'] == 0:
        res = response.json()['data']['goodsList']
        for x in res:
            
            print(f"{x['name']}状态：{x['stockStatus']}")
            if ('京东' in x['name'] or '微信立减金' in x['name']) and x['stockStatus'] == '0':
                msg.append(f"{x['name']} 疑似有库存")
        
    else:
        print(response.text)
        msg.append(response.text)
except:
    print('出错了')
    print(response.text)
    msg.append('出错了')
    msg.append(response.text)
if msg:
    send('建行信用卡一元购查询', '\n'.join(msg))
