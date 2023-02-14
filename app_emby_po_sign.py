'''
new Env('Pornbot 签到')
https://apitruecaptcha.org/api.html
'''
import asyncio
import base64
import json
import re
import time
import random
import requests
import os
from datetime import datetime
from os import environ
from sendNotify import send
from sys import stdout, exit
from xpinyin import Pinyin
from telethon import TelegramClient, events

py = Pinyin() #转拼音
now = datetime.now()

API_ID1 = environ.get('api_id')	if environ.get('api_id') else '' #输入api_id，一个账号一项
API_HASH1 = environ.get('api_hash')	if environ.get('api_hash') else ''   #输入api_hash，一个账号一项
captcha_username = environ.get('captcha_username') if environ.get('captcha_username') else ''
captcha_pwd = environ.get('captcha_pwd') if environ.get('captcha_pwd') else ''

#session_name = API_ID[:]
CHANNEL_ID = ['https://t.me/PronembyTGBot2_bot']#, '@EmbyPublicBot','@blueseamusic_bot', '@Orange_Emby_Bot','@EmbyMistyBot']  #, 
if len(API_HASH1) == 0 or len(API_ID1) == 0:
    print('未填api_id或api_hash，退出')
    exit(0)
else:
    API_ID = API_ID1.split('&')
    API_HASH = API_HASH1.split('&')



def sj(a, b):
    return random.randint(a, b)

async def captcha_solver(dealcap):
    with open('./captcha.jpg', 'rb') as tp:
        base64data = base64.b64encode(tp.read())
        #print_now(base64data)
    captcha_url = 'https://api.apitruecaptcha.org/one/gettext'
    data = {
        "userid":captcha_username,
        "apikey":captcha_pwd,
        'case':'lower',
        "data":str(base64data.decode('utf-8'))
    }
    #print_now(str(base64data.decode('utf-8'))) #'data:image/jpeg;base64,' +  
    try:
        response = requests.post(url=captcha_url, json=data)
        print_now(response.json())

        if response.json()["result"]:
            solved_result = response.json()["result"]
        else:
            solved_result = '2b'
            print_now('识别图片验证码失败，输入2b尝试')
        if len(solved_result) != 2 and dealcap:
            print_now('识别结果过长，取最后两位尝试')
            solved_result = solved_result[-2:]
        return solved_result
        #return base64data
    except:
        print_now('验证码识别平台无回应，随便返回一个结果')
        return dg341




def print_now(content):
    print(content)
    stdout.flush()


async def main1(api_id, api_hash, channel_id):
    MSG = '/checkin'
    async with TelegramClient("id_" + str(api_id), api_id, api_hash) as client:
        me = await client.get_me() #获取当前账号信息       
        if me.username not in ''.join(msg):
            print_now(me.first_name + ' @' + me.username)
            msg.append(me.first_name + ' @' + me.username + '\n')

        print_now('\n准备去签到:' + channel_id)
        msg.append('\n准备去签到:' + channel_id)
        await client.send_message(channel_id, MSG)
        @client.on(events.NewMessage(chats=channel_id))

        async def my_event_handler(event):
            global cishu
            cishu += 1
            print_now('当前第' + str(cishu) + '次尝试')
            print_now(event.message.text)
            time.sleep(sj(3,8))
            if cishu > 10:
                print_now('尝试次数已达到10次仍未成功，退出')
                msg.append('尝试次数已达到10次仍未签到成功')
                if channel_id == '@EmbyPublicBot':
                    await client.send_message(channel_id, '/cancel')
                await client.send_read_acknowledge(channel_id)
                await client.disconnect()
            # 根据button count 区分消息类型
            if "已经签到过" in event.message.text or "距离下次可签到" in event.message.text or '当前积分' in event.message.text or "已签过到" in event.message.text or "You have checkined today" in event.message.text:
                # 结束循环
                print_now('已签到，终止')
                
                if '积分' in event.message.text or '余额总计' in event.message.text or "your point" in event.message.text:
                    msg.append('已签到:')
                    print_now(event.message.text)
                    msg.append(event.message.text)
                    await client.send_read_acknowledge(channel_id) #退出运行
                    await client.disconnect()
                else:
                    await client.send_message(channel_id, '/userinfo') #查询分数

                
                
            elif 'KeyboardButtonCallback' in str(event.message): #计算签到

                await event.message.click(0)

            elif "会话超时已取消" in event.message.text or "验证码错误" in event.message.text or "Wrong captcha code" in event.message.text or "Session canceled due to timeout" in event.message.text:
                await client.send_message(channel_id, MSG)
                        
            elif "输入签到验证码" in event.message.text or "输入错误或超时" in event.message.text or "输入验证码" in event.message.text or "Please input the captcha code" in event.message.text:  # 获取图像验证码
                if len(captcha_pwd) < 2 or len(captcha_username) < 2:
                    print_now('未填验证码识别账号信息，退出')
                    await client.send_read_acknowledge(channel_id)
                    await client.disconnect()
                await client.download_media(event.message.photo, "captcha.jpg")
                # 使用 TRUECAPTCHA 模块解析验证码
                if "输入验证码" in event.message.text or "Please input the captcha code" in event.message.text:
                    print_now('非两位验证码')
                    solved_result = await captcha_solver(0)  
                else:
                    print_now('两位验证码')
                    solved_result = await captcha_solver(1)
                time.sleep(sj(4,10))
                print_now('输入验证码为：' + solved_result)
                await client.send_message(event.message.chat_id, solved_result)
                
                # 删除临时文件
                os.remove("captcha.jpg")
            # 是否成功签到
            elif '签到成功' in event.message.text or '你回答正确' in event.message.text or "Checkin successful" in event.message.text:
                msg.append(event.message.text)
                print_now(event.message.text)
                await client.send_read_acknowledge(channel_id)
                await client.disconnect()
            else :
                print_now('不知道咋回事，防止意外，退出')
                msg.append('出现意外，未签到')
                #time.sleep(sj(5,10))
                await client.send_read_acknowledge(channel_id)	#将机器人回应设为已读
                await client.disconnect()
            #await client.send_read_acknowledge(channel_id)	#将机器人回应设为已读
            #await client.disconnect()
        await client.start()
        await client.run_until_disconnected()    

        
        
async def main2(api_id, api_hash, channel_id):

    MSG = '/checkin'

    async with TelegramClient("id_" + str(api_id), api_id, api_hash) as client:
        
        me = await client.get_me() #获取当前账号信息       
        if me.username not in ''.join(msg):
            print_now(me.first_name + ' @' + me.username)
            msg.append(me.first_name + ' @' + me.username + '\n')

        print_now('\n准备去签到:' + channel_id)
        msg.append('\n准备去签到:' + channel_id)
        await client.send_message(channel_id, MSG)
        time.sleep(sj(5,10))
        '''
        first_msg = client.iter_messages(channel_id, 1) #首次发送签到命令后等待7秒打印第一条信息
        print_now(first_msg)

        if me.first_name == first_msg.sender.first_name:  #如果发送人为账号本身，退出
            print_now('当前账号无反应，可能被禁用或' + channel_id + '卡住了，退出')
            msg.append('当前账号无反应，可能被禁用或' + channel_id + '卡住了')
            await client.disconnect()
        '''
        @client.on(events.NewMessage(chats=channel_id))#
        #@client.on(events.MessageEdited(chats=channel_id))


        async def my_event_handler(event):
            global cishu
            cishu += 1


            print_now('当前第' + str(cishu) + '次尝试')
            print_now(event.message.text)
            time.sleep(sj(5,8))

            #尝试八次，失败退出
            if cishu > 10:
                print_now('尝试次数已达到10次仍未成功，退出')
                msg.append('尝试次数已达到10仍未签到成功')
                if channel_id == '@EmbyPublicBot':
                    await client.send_message(channel_id, '/cancel')
                await client.send_read_acknowledge(channel_id)
                #await asyncio.sleep(0)
                await client.disconnect()
            #print_now(event.message)

            # 区分消息类型
            if "已经签到过" in event.message.text or "距离下次可签到" in event.message.text or '当前积分' in event.message.text:
                # 结束运行
                if '积分' in event.message.text or '总分' in event.message.text or '余额总计' in event.message.text:
                    print_now('已签到，终止')
                    msg.append('已签到:')
                    print_now(event.message.text)
                    msg.append(event.message.text)
                    
                    await client.send_read_acknowledge(channel_id) #退出运行
                    #return
                    #await asyncio.sleep(0)
                    time.sleep(5)
                    await client.disconnect()
                else:
                    await client.send_message(channel_id, '/userinfo') #卷毛查询分数
            elif "输入签到验证码" in event.message.text or "输入错误或超时" in event.message.text or "请输入验证码" in event.message.stringify():  # 获取图像验证码
                if len(captcha_pwd) < 2 or len(captcha_username) < 2:  #无验证码识别信息
                    print_now('未填验证码识别账号信息，退出')
                    await client.send_read_acknowledge(channel_id)
                    #await asyncio.sleep(0)
                    await client.disconnect()
                print_now('开始下载验证码')
                #print_now(event.message)
                await client.download_media(event.message.photo, "captcha.jpg")
                #print_now(aaa)
                print_now('开始识别验证码')
                # 使用 TRUECAPTCHA 模块解析验证码
                
                if "输入验证码" in event.message.text:
                    print_now('非两位验证码')
                    solved_result = await captcha_solver(0)  
                else:
                    print_now('两位验证码')
                    solved_result = await captcha_solver(1)
                

                time.sleep(sj(3,6))
                print_now('输入验证码为：' + solved_result)
                await client.send_message(event.message.chat_id, solved_result)
                
                # 删除临时文件
                os.remove("captcha.jpg")
            elif 'KeyboardButtonCallback' in str(event.message): #按钮
                #print(event.message)
                buttons = event.message.reply_markup.rows[0].buttons
                #print_now( event.message.reply_markup.rows[0])
                await event.message.click(0)  #签到按钮所在位置
                '''
                print('12')
                time.sleep(sj(5,7))
                await client.send_read_acknowledge(channel_id)
                async for msgs in client.iter_messages(channel_id, 1):  #获取最新一条消息
                    print(msgs)
                    if '已经签到过' in msgs.text or '签到成功' in msgs.text:   #如果签到过，运行
                        print_now(msgs.text)
                        msg.append(msgs.text)
                        await client.send_read_acknowledge(channel_id)  
                        #await asyncio.sleep(0)
                        await client.disconnect()
                        '''
                        
                            

            # 是否成功签到
            elif '签到成功' in event.message.text or '你回答正确' in event.message.text:
                msg.append(event.message.text)
                print_now(event.message.text)
                await client.send_read_acknowledge(channel_id)
                #await asyncio.sleep(0)
                await client.disconnect()
            elif '验证码错误' in event.message.text: #orange验证码错误，重新获取
                print_now(event.message.text)
                await client.send_message(channel_id, MSG)
            else :
                print_now('不知道咋回事，防止意外，退出')
                msg.append('出现意外，未签到')
                #time.sleep(sj(5,10))
                await client.send_read_acknowledge(channel_id)	#将机器人回应设为已读
                #await asyncio.sleep(0)
                await client.disconnect()           
        await client.start()
        await client.run_until_disconnected()   
        '''
        js = await iter_messages(client, channel_id, me)
        print_now(js)
        if js == 0:
            await client.disconnect()
            return
        print_now('ga')
        '''
        #await client.run_until_disconnected()






if __name__ == "__main__":
    msg = []
    print('共' + str(len(API_ID)) + '个账户：' + API_ID1.replace('&', '  '))
    print('签到bot：' + '  '.join(CHANNEL_ID))
    zh = 0
    for i in API_ID:       
        zh += 1 
        print_now('\n\n************开始执行账号' + str(zh) + '：' + str(i) + '：' '************\n')
        msg.append('\n*********账号' + str(zh) + '：' + str(i) + '：' '*********\n')
        yc = sj(30,100)
        print_now('随机延迟' + str(yc) + '秒后开始执行')
        #time.sleep(yc)

        cishu = 0
        #if i == '9421323' or i == '4524860':

        asyncio.run(main2(i, API_HASH[API_ID.index(i)], 'https://t.me/PronembyTGBot2_bot')) #签到

            #break
    
    if int(now.strftime('%H')) > 12:
        print_now('当前小时为' + now.strftime('%H') + '发送通知。。。')
        send('Pornbot 签到', '\n'.join(msg))  
    else:
        print_now('当前小时为'+ now.strftime('%H') + '取消通知')
    exit(0)
