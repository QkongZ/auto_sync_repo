import requests
import re
import os
from sendNotify import send
cookie=os.environ.get('laravel_session')
class qndxx:
    def __init__(self, cookie):
        headers_post = {
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
        headers_get = {
            "Host": "service.jiangsugqt.org",
            "Connection": "keep-alive",
            #"Content-Length": "21",
            "withCredential": "true",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2012K11AC Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/107.0.5304.141 Mobile Safari/537.36 XWEB/5023 MMWEBSDK/20221206 MMWEBID/4883 MicroMessenger/8.0.32.2300(0x2800205D) WeChat/arm64 Weixin NetType/5G Language/zh_CN ABI/arm64",
            "Content-Type": "application/json",
            "Accept": "*/*",
            #"Origin": "https://service.jiangsugqt.org",
            "X-Requested-With": "com.tencent.mm",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://service.jiangsugqt.org/youth-h5/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7",
            "Cookie": cookie
        }
        self.headers_post=headers_post
        self.headers_get=headers_get
    def my(self):

        url = "https://service.jiangsugqt.org/api/my"
        res =requests.get(url=url, headers=self.headers_get)

        if res.json() and res.json()['status'] == 1:
            print(res.json()['data']['username'], res.json()['data']['orga'])
        else:
            print(res.text)
    
    def todayJob(self):
        url = "https://service.jiangsugqt.org/api/todayJob"
        res =requests.get(url=url, headers=self.headers_get)
        if res.json() and res.json()['status'] == 1:
            print(f"剩余分数：{res.json()['data']['rest_score']}")
            print(f"今日分数：{res.json()['data']['today_score']}")
            resu = res.json()['data']['list']
            for x in resu:

                if x['is_finish'] == 1:
                    print(f"{x['title']} 已完成")
                else:
                    print(f"{x['title']} 未完成")
                    if '阅读' in x['title']:
                        self.news(1)
                    elif '观看' in x['title']:
                        self.news(2)
        else:
            print(res.text)

    def lesson(self):
        infor_url = "https://service.jiangsugqt.org/api/lessons"
        data = {'page':1,'limit':5}
        response = requests.post(url=infor_url, headers=self.headers_post,json=data)
        #response.encoding = response.apparent_encoding
        #print(response.json())
        #token = re.findall(r'var token = "(.*?)";', response.text)[0]
        i = 0
        for x in response.json()['data']:
            i+=1

            if i > 4:
                break
            lesson_id = x['id']
            commit_url = "https://service.jiangsugqt.org/api/doLesson"
            params = {

                "lesson_id": lesson_id
            }
            response = requests.post(url=commit_url, headers=self.headers_post, json=params)
            #response.encoding = response.apparent_encoding
            print(response.json()['message'],response.json()['data']['title'])


    def news(self, category): 
        url = "https://service.jiangsugqt.org/api/newsList"
        json = {'page':1,'limit':10, 'category':category}
        res =requests.post(url=url, headers=self.headers_post, json=json)
        if res.json() and res.json()['status'] == 1:
            data = res.json()['data']
            for x in data:
                print(f"去完成：{x['title']}")
                url_read = "https://service.jiangsugqt.org/api/news"
                json_read = {'id':x['id']}
                res_read= requests.post(url=url_read, headers=self.headers_post, json=json_read)
                print(res_read.json()['message'])
        else:
            print(res.text)
    
    def giftList(self): 
        url = "https://service.jiangsugqt.org/api/giftList"
        json = {'page':1,'limit':10}
        res =requests.post(url=url, headers=self.headers_post, json=json)
        if res.json() and res.json()['status'] == 1:
            data = res.json()['data']
            print(data)
            if data:
                send('青年大学习', str(data))

        else:
            print(res.text)
    def main(self):
        
        self.my()

        self.lesson()
        self.todayJob()
        print('\n\n')
        self.todayJob()
        self.giftList()
if __name__ == "__main__":
    dxx = qndxx(cookie)
    dxx.main()
