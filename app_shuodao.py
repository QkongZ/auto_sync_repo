
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
from tools.encrypt_symmetric import Crypt
from tools.send_msg import push
from tools.tool import get_environ, random_sleep
from sendNotify import send
from datetime import datetime

now = datetime.now()
"""读取环境变量"""
uids = environ.get("shuodao") if environ.get("shuodao") else ""


uidArr = uids.split('\n')
for phone in uidArr:
    if not phone:
        uidArr.remove(phone)  
    

"""主类"""


class ShuoDao:
    def __init__(self, uid):
        self.uid = uid.split('@')[0]
        self.userId = uid.split('@')[1]
        self.appType = uid.split("@")[2]
        self.userName = ''
        self.validPoint = ''
        self.salt = 'horace-allin'
        default_ua = f"Mozilla/5.0 (Linux; Android 7.1.2; BRQ-AN00 Build/N6F26Q; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 TengZhan/3"
        run_ua = get_environ(key="UNICOM_USERAGENT", default=default_ua, output=False)
        self.headers = {
            "Host": "dt-apigatewayv2.dt-pn1.com",
            "accept": "application/json, text/plain, */*",
            "user-agent": run_ua,
        }
        self.fail_num = 0

    def timestamp(self):
        return round(time() * 1000)

    def print_now(self, content):
        print(content)
        stdout.flush()

    def md5(self, str):
        m = md5Encode(str.encode(encoding='utf-8'))
        return m.hexdigest()

    def req(self, url, retry_num=5):
        while retry_num > 0:
            try:
                res = get(url, headers=self.headers)
                data = res.json()
                return data
            except Exception as e:
                self.print_now(f"😭本次请求失败, 正在重新发送请求 剩余次数{retry_num}")
                self.print_now(f"😭本次请求失败原因------{e}")
                retry_num -= 1
                sleep(5)
                return self.req(url, retry_num)

    def pet_play(self, toyType):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/play?userId={self.userId}&appType={self.appType}&toyType={toyType}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            self.print_now('任务完成成功')
        else:
            self.print_now(f'😭出错了：{data}')
            
    def pet_playPage(self):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/playPage?userId={self.userId}&appType={self.appType}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            self.print_now(f'今日play情况：{data["playLeftChance"]}/{data["playTotalchance"]}')
            toys = data['toys']
            playcishu = data["playLeftChance"]
            toys.reverse()
            #self.print_now(toys)
            if playcishu > 0:
                for toy in toys:
                    self.print_now(f'{toy["toyName"]}:{toy["toyNum"]}')
                    if toy["toyNum"] > 0:
                        toycishu = toy["toyNum"]
                        for t in range(toy["toyNum"]):
                            if toycishu > 0 and playcishu > 0:
                                self.pet_play(toy["toyType"])
                                playcishu -= 1
                                toycishu -= 1
                                sleep(5)
                            else:
                                break
        else:
            self.print_now(f'😭出错了：{data}')

    def pet_task_receiveReward(self, taskType, c):
        timestamp = self.timestamp()
        if taskType == 3:
            for visitPetId in [85737, 85719, 85730, 85799, 85763]:
                url = f"https://dt-apigatewayv2.dt-pn1.com/pet/task/receiveReward?userId={self.userId}&appType={self.appType}&taskType={taskType}&visitPetId={visitPetId}&timeStamp={timestamp}"
                data = self.req(url)
                if data['Result'] == 1:
                    self.print_now('任务完成成功')
                else:
                    self.print_now(f'😭出错了 {data}')
        else:
            for a in range(c):
                url = f"https://dt-apigatewayv2.dt-pn1.com/pet/task/receiveReward?userId={self.userId}&appType={self.appType}&taskType={taskType}&timeStamp={timestamp}"
                data = self.req(url)
                if data['Result'] == 1:
                    self.print_now(f'任务 {taskType} 完成成功')
                else:
                    self.print_now(f'😭任务 {taskType} 出错了 {data}')

    def pet_task_list(self):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/task/list?userId={self.userId}&appType={self.appType}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            #self.print_now(data)
            data = data["data"]['tasks']
            for x in data:
                self.print_now(f'任务：{x["taskName"]}（{x["taskCompletedNum"]}/{x["taskUpperLimit"]}）')
                if x['taskType'] == 4:
                    continue
                if x['taskStatus'] == 1:
                    self.print_now('-尚未完成，去完成。。')
                    self.pet_task_receiveReward(x['taskType'], x["taskUpperLimit"] - x["taskCompletedNum"])
        else:
            self.print_now(f'😭出错了 {data}')
                    
    def pet_doublePrize(self,prizeType,totalPrizeCount):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/doublePrize?userId={self.userId}&appType={self.appType}&prizeType={prizeType}&totalPrizeCount={totalPrizeCount}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            self.print_now('翻倍成功')
        else:
            self.print_now(f'😭出错了 {data}')
        return

    def pet_lottery(self, c):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/lottery?userId={self.userId}&appType={self.appType}&timeStamp={timestamp}"
        for x in range(c):
            data = self.req(url)
            #self.print_now(data)
            sleep(3)
            if data['Result'] == 1:
                data = data["data"]
                self.print_now(f"奖品类型 {data['prizeType']}，数量 {data['totalPrizeCount']}")
                if data['prizeType'] == 3 and data['totalPrizeCount'] == 1:
                    self.print_now(f'{data}')
                sleep(5)
                self.pet_doublePrize(data['prizeType'],data['totalPrizeCount'])
                #sleep(3)
            else:
                self.print_now(f'😭抽奖出错了 {data}')
        return

    def pet_lotteryPage(self):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/lotteryPage?userId={self.userId}&appType={self.appType}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            self.print_now(f'轮盘抽奖次数：{data["lotteryLeftChance"]}/{data["lotteryTotalchance"]}')
            if data["lotteryLeftChance"] > 0:
                self.print_now('-去抽奖。。。')
                self.pet_lottery(data["lotteryLeftChance"])
                #sleep(1)
        else:
            self.print_now(f'😭出错了 {data}')

    def pet_feed(self, x):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/feed?userId={self.userId}&appType={self.appType}&feeFishNum={x}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            self.print_now('喂食成功')
        else:
            self.print_now(f'😭喂食失败了 {data}')
        return

    def pet_treasureHunt(self):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/treasureHunt?userId={self.userId}&appType={self.appType}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            self.print_now('寻宝成功')
        else:
            self.print_now(f'😭寻宝失败了 {data}')
        return

    def pet_morePrize(self, prizeType):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/morePrize?userId={self.userId}&appType={self.appType}&prizeType={prizeType}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            print(data['data'])
        else:
            print(f'😭morePrize出错了 {data}')

    def pet_homePage(self):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/homePage?userId={self.userId}&appType={self.appType}&timeStamp={timestamp}"
        data = self.req(url)
        #print(url, data)
        if data['Result'] == 1:
            data = data["data"]
            self.print_now(f'{data["petName"]}：Lv{data["petLevel"]}({data["growthValue"]}/{data["growthValue"]+data["nextLevelRequiredGrowthValue"]}) \n鱼料：{data["fishNum"]}')
            if data["nextFeedRemainingTime"] == 0:
                for x in [50, 10, 5, 2]:
                    if data["fishNum"] > x:
                        self.print_now(f'-去喂食 {x} g。。。')
                        self.pet_feed(x)
                        break
            elif  data["nextFeedRemainingTime"] > 0:
                self.print_now(f'剩余喂食时间：{int(data["nextFeedRemainingTime"]/60)}分{data["nextFeedRemainingTime"]%60}秒')
            if data['treasureHuntStatus'] == 3:
                self.print_now(f'下次寻宝时间{int(data["nextTreasureHuntRemainingTime"]/60)}分{data["nextTreasureHuntRemainingTime"]%60}秒')
            elif data['treasureHuntStatus'] == 1:
                self.print_now(f'寻宝中，剩余时间{int(data["treasureHuntEndRemainingTime"]/60)}分{data["treasureHuntEndRemainingTime"]%60}秒')
            elif data['treasureHuntStatus'] == 0:
                self.print_now('-可寻宝，准备去。。。')
                self.pet_treasureHunt()
            elif data['treasureHuntStatus'] == 2:
                ty = 2
                if data['treasureHuntRewardCreditNum']:
                    self.print_now(f'⭕获得说到币：{data["treasureHuntRewardCreditNum"]}')
                if data["treasureHuntRewardFishNum"]:
                    self.print_now(f'⭕获得鱼饵：{data["treasureHuntRewardFishNum"]}')
                    ty = 1
                self.print_now('寻宝结束，领奖翻倍。。。')
                self.pet_morePrize(ty)
            else:
                self.print_now(data)
              
    def checkin_reward(self):
        url = f"https://dt-apigatewayv2.dt-pn1.com/point/checkin/reward?uid={self.uid}"
        data = self.req(url)
        #self.print_now(data)
        if data['Result'] == 1:
            data = data["data"]
            self.print_now(f'⭕获得 {data["prizeName"]}')
        else:
            self.print_now(f'😭checkin_reward出错 {data}')
        return

    def checkin_addtimes(self, c):
        url = f"https://dt-apigatewayv2.dt-pn1.com/point/checkin/addtimes?uid={self.uid}"
        for x in range(c):
            data = self.req(url)
            if data['Result'] == 1:
                self.print_now('⭕增加成功')
                self.checkin_reward()
            else:
                self.print_now('😭失败了呢')
        return
            
    def checkin_times(self):
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/point/checkin/times?uid={self.uid}"
        data = self.req(url)
        #self.print_now(data)
        if data['Result'] == 1:
            data = data["data"]
            self.print_now(f'可用次数：{data["validTimes"]}\n已获得/可获得次数：{data["addTimes"]}/{data["maxAddTimes"]}')
            if data["addTimes"] < data["maxAddTimes"]:
                self.print_now('-去获取次数。。。')
                self.checkin_addtimes(data["maxAddTimes"]-data["addTimes"])
            elif data["validTimes"] > 0:
                self.checkin_reward()  
            else:
                self.print_now('今日无次数了')
        else:
            self.print_now(f"😭签到次数查询失败：{data}")
            exit(0)

    def ad_roulette_reward(self, ad_roulette_times):
        url = f"https://dt-apigatewayv2.dt-pn1.com/web/ad/roulette/reward?userId={self.userId}&deviceId=And.8b0355c263713b5301559b2a0c222859.dttalk&timeZone=Asia%2FShanghai&isoCC=US"
        for ada in range(ad_roulette_times):
            data = self.req(url)
            if data['Result'] == 1:
                data = data["data"]
                self.print_now(f'⭕ad_roulette_reward获得 {data["prizeName"]}')
            else:
                self.print_now(f'😭ad_roulette_reward出错 {data["Reason"]}')
            sleep(1)
        return

    def ad_roulette_chance_add(self):
        url = f"https://dt-apigatewayv2.dt-pn1.com/web/ad/roulette/chance/add?userId={self.userId}&deviceId=And.8b0355c263713b5301559b2a0c222859.dttalk"
        for ad in range(2):
            data = self.req(url)
            if data['Result'] == 1:
                ad_roulette_times = data['data']
                print(f'当前抽奖次数 {ad_roulette_times}')
            else:
                print(f'😭获取抽奖次数出错， {data}')
                break
            sleep(1)
        if ad_roulette_times > 0:
            #print('去抽奖')
            self.ad_roulette_reward(ad_roulette_times)
        
    def pointstore(self):
        url = f'https://dt-apigatewayv2.dt-pn1.com/pointstore/entrance?uid={self.uid}&lang=cn&osType=2'
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            if data['products'] and len(data['products']) > 0:
                for product in data['products']:
                    self.print_now(f"{product['name']} 剩余 {product['stock']} 件，需要 {product['price']}")
                    if product['name'] != 'Credit Coupon' and product['stock'] > 0:
                        msg = f"用户 {self.userName} ，当前拥有 {self.validPoint} 积分\n{product['name']} 剩余 {product['stock']} 件，需要 {product['price']} 积分"
                        send('⭕说道/叮咚积分兑换提醒', msg)

    def userinfo(self):
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        url = f"https://dt-apigatewayv2.dt-pn1.com/point/userinfo?uid={self.uid}&zone=800"
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            self.userName = data["userName"]
            self.validPoint = data["validPoint"]
            self.print_now(f'用户：{data["userName"]} Lv{data["userGrade"]+1}\n可用/总积分：{data["validPoint"]}/{data["historyPoint"]}\n将在{data["expireTime"]}过期：{data["expirePoint"]}')
        else:
            self.print_now(f"😭获取基本信息失败, 日志为{data}")
            exit(0)

    def fruit_homepage(self):
        timestamp = self.timestamp()
        url = f'https://dt-apigatewayv2.dt-pn1.com/campaign/fruit/homepage?userId={self.userId}&appType={self.appType}&dingtoneId=196252944&campaignId=10094&zone=GMT%2B8&timeStamp={timestamp}'
        data =  self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            if len(data['plantFruitList'])  > 0:
                for fruit in data['plantFruitList']:
                    #print(fruit["completionRate"])
                    print(f'水果 {fruit["name"]}，进度 {round(fruit["completionRate"]*100, 1)}%')
                    if fruit["completionRate"] == 1:
                        send('说道种水果成熟通知', f'账户 {self.userName} 所种水果已经成熟')
            else:
                print('-未种植任何水果，尝试去种植。。。')
                self.fruit_plant()
        else:
            self.print_now(f"😭获取果园信息失败：{data}")
        self.fruit_task()
    def fruit_plant(self):
        timestamp = self.timestamp()
        fruitType = '1'#水果 1 apple; 2 mango
        url = f'https://dt-apigatewayv2.dt-pn1.com/campaign/fruit/plant?userId={self.userId}&dingtoneId=196252944&fruitType={fruitType}&campaignId=10094&appType={self.appType}&zone=GMT%2B8&timeStamp={timestamp}'
        data =  self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            print(f"👌种植 {data['name']}（{data['fruitId']}） 成功")
            self.fruit_homepage()
        else:
            print(f'😭种植水果失败：{data}')
    def fruit_task(self):
        timestamp = self.timestamp()
        url = f'https://dt-apigatewayv2.dt-pn1.com/campaign/fruit/task/list?userId={self.userId}&campaignId=10094&timeStamp={timestamp}'
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            for task in data['tasks']:
                if task['taskStatus'] == 0:
                    print(f"-准备去完成任务 {task['taskName']}：{task['taskCompletedNum']}/{task['taskUpperLimit']}")
                    for t in range(task['taskUpperLimit'] - task['taskCompletedNum']):
                        self.fruit_reward(task['taskType'])
                elif task['taskStatus'] == 1:
                    print(f"👌任务 {task['taskName']} 已完成：{task['taskCompletedNum']}/{task['taskUpperLimit']}")
                else:
                    print(task)
            u = f'https://dt-apigatewayv2.dt-pn1.com/campaign/fruit/homepage?userId={self.userId}&appType={self.appType}&dingtoneId=196252944&campaignId=10094&zone=GMT%2B8&timeStamp={timestamp}'
            data = self.req(u)
            if data['Result'] == 1:
                data = data["data"]
                if len(data['plantFruitList'])  > 0:
                    print(f'当前水滴 {data["nutritiveNumber"]}')
                    if data["nutritiveNumber"] > 0:
                        for fruit in data['plantFruitList']:
                            if fruit["completionRate"] < 1:
                                print(f"-去给 {fruit['name']}（{fruit['fruitId']}） 浇水")
                                self.fruit_water(fruit['fruitId'])
                                break
        else:
            print(f"😭获取果园任务失败：{data}")
    def fruit_reward(self, taskType):
        timestamp = self.timestamp()
        url = f'https://dt-apigatewayv2.dt-pn1.com/campaign/fruit/mission/reward?userId={self.userId}&campaignId=10094&appType={self.appType}&dingtoneId=196252944&taskType={taskType}&timeStamp={timestamp}'
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            print(f"⭕获得 {data['reward']} 水滴")
        else:
            print(f'😭完成任务失败：{data}')
    def fruit_water(self, fruitId):
        timestamp = self.timestamp()
        url = f'https://dt-apigatewayv2.dt-pn1.com/campaign/fruit/warter?userId={self.userId}&campaignId=10094&appType={self.appType}&dingtoneId=196252944&fruitId={fruitId}&timeStamp={timestamp}'
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            print(f"⭕浇水成功，当前进度 {round(data['completionRate']*100, 1)}% 水滴")
        elif data['ErrCode'] == 10004:
            print(f'😭{data["Reason"]}')
        elif data['ErrCode'] == 10005:
            print(f'😭{data["Reason"]}')
        else:
            print(f'😭浇水失败：{data}')

    def knife_homePage(self):
        timestamp = self.timestamp()
        url = f'https://dt-apigatewayv2.dt-pn1.com/knife/homePage?userId={self.userId}&appType={self.appType}&timeStamp={timestamp}'
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            print(f'当前剩余 {data["remainPlayTimes"]} 次游戏机会')
            
            print(f'当前剩余Juice {data["fruitJuiceAmount"]} 个')
            print(f'当前看广告获取游戏次数：{data["watchingGetPlayTimes"]}/{data["watchingGetPlayTimesLimit"]}')
            if data['treasureBoxOwned'] and data['treasureBoxOpenTime'] > timestamp:
                d = datetime.fromtimestamp(data['treasureBoxOpenTime'] / 1000).strftime("%m-%d %H:%M:%S")
                print(f'开宝箱时间：{d}')
            elif data['treasureBoxOwned'] and data['treasureBoxOpenTime'] <= timestamp:
                print('疑似可开宝箱')
                self.knife_openTreasureBox()
            t = 2
            if data["remainPlayTimes"] > 0:
                if data["remainPlayTimes"] <=  2:
                    t = data["remainPlayTimes"]
                for a in range(t):
                    self.knife_play()
            #self.knife_lotteryPage() #直接领奖（防止做过任务但领奖失败）
            if data["watchingGetPlayTimesLimit"] != data["watchingGetPlayTimes"]:
                self.knife_watchingForPlay()
        else:
            print(f'😭查询扎转盘任务失败：{data}')
    def knife_watchingForPlay(self):
        timestamp = self.timestamp()
        url = f'https://dt-apigatewayv2.dt-pn1.com/knife/watchingForPlay?userId={self.userId}&appType={self.appType}&timeStamp={timestamp}'
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            print(f'-当前看广告获取游戏次数：{data["watchingGetPlayTimes"]}/{data["watchingGetPlayTimesLimit"]}')
        else:
            print(f'😭看广告获取次数失败：{data}')
    def knife_openTreasureBox(self):
        timestamp = self.timestamp()
        url = f'https://dt-apigatewayv2.dt-pn1.com/knife/openTreasureBox?userId={self.userId}&appType={self.appType}&timeStamp={timestamp}'
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            print(data)
        else:
            print(f'😭玩游戏失败：{data}')
    def knife_play(self):
        timestamp = self.timestamp()
        url = f'https://dt-apigatewayv2.dt-pn1.com/knife/play?userId={self.userId}&appType={self.appType}&timeStamp={timestamp}'
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            print(f"⭕玩游戏成功，当前剩余 {data['remainPlayTimes']} 次")
            print(f"当前Juice {data['fruitJuiceAmount']} 个")
            sleep(5)
            self.knife_lotteryPage()
        else:
            print(f'😭玩游戏失败：{data}')
    def knife_lotteryPage(self):
        timestamp = self.timestamp()
        level = 10  #10等级转盘
        #print(f"{int(self.userId)}-{int(self.appType)}-{int(10)}-{int(timestamp)}-{self.salt}")
        jm = self.md5(f"{int(self.userId)}-{int(self.appType)}-{int(10)}-{int(timestamp)}-{self.salt}")
        #print(jm)
        url = f'https://dt-apigatewayv2.dt-pn1.com/knife/lotteryPage?userId={self.userId}&appType={self.appType}&level={level}&md5={jm}&timeStamp={timestamp}'
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            #print(data)
            if data['lotteryId']:
                sleep(1)
                self.knife_lottery(data['lotteryId'], data['lotteryPrizeList'])
        else:
            print(f'😭打开抽奖页失败：{data}')
    def knife_lottery(self, lotteryId, lotteryPrizeList):
        timestamp = self.timestamp()
        jm = self.md5(f'{self.userId}-{self.appType}-{lotteryId}-{timestamp}-{self.salt}')
        url = f'https://dt-apigatewayv2.dt-pn1.com/knife/lottery?userId={self.userId}&appType={self.appType}&lotteryId={lotteryId}&md5={jm}&timeStamp={timestamp}'
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            #print(data)
            for x in lotteryPrizeList:
                if x['prizeId'] == data['prizeId']:
                    print(f'⭕本次抽中 {x["prizeName"]}')
                '''
            if data['prizeType'] == 3:
                print(f'⭕抽中 {data["totalPrizeCount"]} Juice')
            elif data['prizeType'] == 1:
                print(f'⭕抽中 {data["totalPrizeCount"]} Credits')
            elif data['prizeType'] == 2:
                print(f'⭕抽中 {data["totalPrizeCount"]} 宝箱')
            else:
                print('暂时不知道抽中的啥')
                '''
            if data['doublePrize']:
                self.knife_doublePrize(data['prizeType'], data["totalPrizeCount"])
        elif data['ErrCode'] == 11018:
            print(data['Reason'])
        else:
            print(f'😭抽奖失败：{data}')
    def knife_doublePrize(self, prizeType, totalPrizeCount):
        timestamp = self.timestamp()
        md5 = md5({self.userId}-{self.appType}-{lotteryId}-{timestamp}-{self.salt})
        url = f'https://dt-apigatewayv2.dt-pn1.com/knife/doublePrize?userId={self.userId}&appType={self.appType}&prizeType={prizeType}&totalPrizeCount={totalPrizeCount}&timeStamp={timestamp}'
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            print(data)
        else:
            print('😭翻倍出错')

    def main(self):
        print(f'\n------用户信息------\n')
        self.userinfo()  #用户会员信息
        print(f'\n------兑换查询------\n')
        self.pointstore()
        print(f'\n------等级任务------\n')
        self.ad_roulette_chance_add() #广告抽奖
        self.checkin_times() #查询签到次数
        #self.checkin()
        print(f'\n------养猫------\n')
        self.pet_homePage() #宠物
        self.pet_lotteryPage() #宠物十次转盘
        self.pet_task_list() #宠物任务
        self.pet_playPage()  #宠物玩耍
        print(f'\n------种水果------\n')
        self.fruit_homepage()#种水果
        print(f'\n------扎转盘------\n')
        self.knife_homePage()
        #exit(0)

if __name__ == "__main__":
    print('共' + str(len(uidArr)) + '个账户')
    c = 0
    shuffle(uidArr)
    print(uidArr)
    u = []

    if int(now.strftime('%H')) < 24:
        for i in uidArr:
            c = c + 1
            print('\n\n============ ▷ 账户' + str(c) + '：' + str(i).split('@')[1] + '◁ ============\n\n')
            ShuoDao(i).main()
    else:
        for i in uidArr:
            u.append(
                threading.Thread(target=ShuoDao(i).main)
            ) 
        for thread in u:
            thread.start()
        for thread in u:
            thread.join()
            
    exit(0)
