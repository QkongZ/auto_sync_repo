import requests
import re
import os
# 以下参数需自行抓取
cookie=os.environ.get('laravel_session')

info_headers = {
    "Host": "service.jiangsugqt.org",
    "Connection": "keep-alive",
    "Content-Length": "21",
    "withCredential": "true",
    "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5023 MMWEBSDK/20221206 MMWEBID/4883 MicroMessenger/8.0.32.2300(0x2800205D) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64",
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://service.jiangsugqt.org",
    "X-Requested-With": "com.tencent.mm",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://service.jiangsugqt.org/youth-h5/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7",
    "Cookie": cookie
  }
infor_url = "https://service.jiangsugqt.org/api/lessons"
data = {'page':1,'limit':5}
response = requests.post(url=infor_url, headers=info_headers,json=data)
#response.encoding = response.apparent_encoding
print(response.json())
#token = re.findall(r'var token = "(.*?)";', response.text)[0]
lesson_id = response.json()['data'][0]['id']
commit_url = "https://service.jiangsugqt.org/api/doLesson"
params = {

    "lesson_id": lesson_id
}
response = requests.post(url=commit_url, headers=info_headers, json=params)
#response.encoding = response.apparent_encoding
print(response.json())
