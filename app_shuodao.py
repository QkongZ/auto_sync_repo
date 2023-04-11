
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

now = datetime.now()
"""读取环境变量"""
uids = environ.get("shuodao") if environ.get("shuodao") else ""


uidArr = uids.split('&')
for phone in uidArr:
    if not phone:
        uidArr.remove(phone)  
    

"""主类"""


class ShuoDao:
    def __init__(self, uid):
        self.uid = uid.split('@')[0]
        self.userId = uid.split('@')[1]
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
                self.print_now(f"本次请求失败, 正在重新发送请求 剩余次数{retry_num}")
                self.print_now(f"本次请求失败原因------{e}")
                retry_num -= 1
                sleep(5)
                return self.req(url, retry_num)

    def pet_play(self, toyType):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/play?userId={self.userId}&appType=3&toyType={toyType}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            self.print_now('任务完成成功')
        else:
            self.print_now(f'出错了 {data}')
            

    def pet_playPage(self):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/playPage?userId={self.userId}&appType=3&timeStamp={timestamp}"
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
            self.print_now(f'出错了 {data}')

    def pet_task_receiveReward(self, taskType, c):
        timestamp = self.timestamp()

        if taskType == 3:
            for visitPetId in [85737, 85719, 85730, 85799, 85763]:
                url = f"https://dt-apigatewayv2.dt-pn1.com/pet/task/receiveReward?userId={self.userId}&appType=3&taskType={taskType}&visitPetId={visitPetId}&timeStamp={timestamp}"
                data = self.req(url)
                if data['Result'] == 1:
                    self.print_now('任务完成成功')
                else:
                    self.print_now(f'出错了 {data}')
        else:
            for a in range(c):
                url = f"https://dt-apigatewayv2.dt-pn1.com/pet/task/receiveReward?userId={self.userId}&appType=3&taskType={taskType}&timeStamp={timestamp}"
                data = self.req(url)
                if data['Result'] == 1:
                    self.print_now(f'任务{taskType}完成成功')
                else:
                    self.print_now(f'任务{taskType}出错了 {data}')

    def pet_task_list(self):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/task/list?userId={self.userId}&appType=3&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            #self.print_now(data)
            data = data["data"]['tasks']
            for x in data:
                self.print_now(f'任务：{x["taskName"]}（{x["taskCompletedNum"]}/{x["taskUpperLimit"]}）')
                if x['taskType'] == 4:
                    continue
                if x['taskStatus'] == 1:
                    self.print_now('尚未完成，去完成。。')
                    self.pet_task_receiveReward(x['taskType'], x["taskUpperLimit"] - x["taskCompletedNum"])
        else:
            self.print_now(f'出错了 {data}')
                    

    def pet_doublePrize(self,prizeType,totalPrizeCount):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/doublePrize?userId={self.userId}&appType=3&prizeType={prizeType}&totalPrizeCount={totalPrizeCount}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            self.print_now('翻倍成功')
        else:
            self.print_now(f'出错了 {data}')
        return

    def pet_lottery(self, c):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/lottery?userId={self.userId}&appType=3&timeStamp={timestamp}"
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
                sleep(3)
            else:
                self.print_now(f'抽奖出错了 {data}')
            
        
        return

    def pet_lotteryPage(self):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/lotteryPage?userId={self.userId}&appType=3&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            self.print_now(f'轮盘抽奖次数：{data["lotteryLeftChance"]}/{data["lotteryTotalchance"]}')
            if data["lotteryLeftChance"] > 0:
                self.print_now('去抽奖。。。')
                self.pet_lottery(data["lotteryLeftChance"])
                #sleep(1)
        else:
            self.print_now(f'出错了 {data}')

    def pet_feed(self, x):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/feed?userId={self.userId}&appType=3&feeFishNum={x}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            self.print_now('喂食成功')
        else:
            self.print_now(f'喂食失败了 {data}')
        return
    def pet_treasureHunt(self):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/treasureHunt?userId={self.userId}&appType=3&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            self.print_now('寻宝成功')
        else:
            self.print_now(f'寻宝失败了 {data}')
        return

    def pet_morePrize(self, prizeType):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/morePrize?userId={self.userId}&appType=3&prizeType={prizeType}&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            print(data['data'])
        else:
            print(f'morePrize出错了 {data}')

    def pet_homePage(self):
        timestamp = self.timestamp()
        url = f"https://dt-apigatewayv2.dt-pn1.com/pet/homePage?userId={self.userId}&appType=3&timeStamp={timestamp}"
        data = self.req(url)
        if data['Result'] == 1:
            data = data["data"]
            self.print_now(f'{data["petName"]}：Lv{data["petLevel"]}({data["growthValue"]}/{data["growthValue"]+data["nextLevelRequiredGrowthValue"]}) \n鱼料：{data["fishNum"]}')
            if data["nextFeedRemainingTime"] == 0:
                
                for x in [50, 10, 5, 2]:
                    if data["fishNum"] > x:
                        self.print_now(f'去喂食 {x} g。。。')
                        self.pet_feed(x)
                        break
            elif  data["nextFeedRemainingTime"] > 0:
                self.print_now(f'剩余喂食时间：{int(data["nextFeedRemainingTime"]/60)}分{data["nextFeedRemainingTime"]%60}秒')

            if data['treasureHuntStatus'] == 3:
                self.print_now(f'下次寻宝时间{int(data["nextTreasureHuntRemainingTime"]/60)}分{data["nextTreasureHuntRemainingTime"]%60}秒')
            elif data['treasureHuntStatus'] == 1:
                self.print_now(f'寻宝中，剩余时间{int(data["treasureHuntEndRemainingTime"]/60)}分{data["treasureHuntEndRemainingTime"]%60}秒')
            elif data['treasureHuntStatus'] == 0:
                
                self.print_now('可寻宝，准备去。。。')
                self.pet_treasureHunt()
            elif data['treasureHuntStatus'] == 2:
                ty = 2
                if data['treasureHuntRewardCreditNum']:
                    self.print_now(f'获得说到币：{data["treasureHuntRewardCreditNum"]}')
                if data["treasureHuntRewardFishNum"]:
                    self.print_now(f'获得鱼饵：{data["treasureHuntRewardFishNum"]}')
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
            self.print_now(f'获得 {data["prizeName"]}')
        else:
            self.print_now(f'checkin_reward出错 {data}')
        return



    def checkin_addtimes(self, c):
        url = f"https://dt-apigatewayv2.dt-pn1.com/point/checkin/addtimes?uid={self.uid}"
        for x in range(c):
            data = self.req(url)
            if data['Result'] == 1:
                self.print_now('增加成功')
                self.checkin_reward()
            else:
                self.print_now('失败了呢')
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
                self.print_now('去获取次数。。。')
                self.checkin_addtimes(data["maxAddTimes"]-data["addTimes"])
            elif data["validTimes"] > 0:
                self.checkin_reward()  
            else:
                self.print_now('今日无次数了')
        else:
            self.print_now(f"签到次数查询失败,日志为{data}")
            exit(0)

    def ad_roulette_reward(self, ad_roulette_times):

        url = f"https://dt-apigatewayv2.dt-pn1.com/web/ad/roulette/reward?userId={self.userId}&deviceId=And.8b0355c263713b5301559b2a0c222859.dttalk&timeZone=Asia%2FShanghai&isoCC=US"
        for ada in range(ad_roulette_times):
            data = self.req(url)
            if data['Result'] == 1:
                data = data["data"]
                self.print_now(f'ad_roulette_reward获得 {data["prizeName"]}')
            else:
                self.print_now(f'ad_roulette_reward出错 {data["Reason"]}')
            sleep(1)
        return
    def ad_roulette_chance_add(self):
        url = f"https://dt-apigatewayv2.dt-pn1.com/web/ad/roulette/chance/add?userId={self.userId}&deviceId=And.8b0355c263713b5301559b2a0c222859.dttalk"
        
        for ad in range(10):
            data = self.req(url)
            if data['Result'] == 1:
                
                ad_roulette_times = data['data']
                print(f'当前抽奖次数 {ad_roulette_times}')
            else:
                print(f'获取抽奖次数出错， {data}')
                break
            sleep(1)
        if ad_roulette_times > 0:
            #print('去抽奖')
            self.ad_roulette_reward(ad_roulette_times)
        


    def userinfo(self):
        date = datetime.today().__format__("%Y%m%d%H%M%S")
        url = f"https://dt-apigatewayv2.dt-pn1.com/point/userinfo?uid={self.uid}&zone=800"
        data = self.req(url)

        if data['Result'] == 1:
            data = data["data"]
            self.print_now(f'用户：{data["userName"]} Lv{data["userGrade"]+1}\n可用/总积分：{data["validPoint"]}/{data["historyPoint"]}\n将在{data["expireTime"]}过期：{data["expirePoint"]}')
        else:
            self.print_now(f"获取基本信息失败, 日志为{data}")
            exit(0)


    def main(self):
        self.userinfo()  #用户会员信息
        self.ad_roulette_chance_add() #广告抽奖
        self.checkin_times() #查询签到次数
        #self.checkin()
        self.pet_homePage() #宠物
        self.pet_lotteryPage() #宠物十次转盘
        self.pet_task_list() #宠物任务
        self.pet_playPage()  #宠物玩耍
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
            print('\n\n账户' + str(c) + '：' + str(i) + '\n\n')
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
