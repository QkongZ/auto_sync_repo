'''
new Env('TGBot 签到')
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
from random import randint, uniform, choice, shuffle
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
CHANNEL_ID1 = environ.get('channel_id') if environ.get('channel_id') else ''
#session_name = API_ID[:]
if captcha_username and captcha_pwd:
    captcha_usernameArr = captcha_username.split('&')
    captcha_pwdArr = captcha_pwd.split('&')


if CHANNEL_ID1:
    CHANNEL_ID = CHANNEL_ID1.split('&')
else:
    CHANNEL_ID = ['@qweybgbot']  #, 
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
    c = random.randint(0, len(captcha_usernameArr) - 1)
    print_now('本次调用账号' + captcha_usernameArr[c])
    data = {
        "userid":captcha_usernameArr[c],
        "apikey":captcha_pwdArr[c],
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
        return str(sj(10000,99999))




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
        @client.on(events.MessageEdited(chats=channel_id))
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
                
                if '积分' in event.message.text or '总分' in event.message.text or "your point" in event.message.text:
                    msg.append('已签到:')
                    print_now(event.message.text)
                    msg.append(event.message.text)
                    await client.send_read_acknowledge(channel_id) #退出运行
                    await client.disconnect()
                else:
                    await client.send_message(channel_id, '/userinfo') #查询分数

                
                
            elif 'KeyboardButtonCallback' in str(event.message): #计算签到
                buttons = event.message.reply_markup.rows[0].buttons
                print_now( event.message.reply_markup.rows[0])
                sz = re.findall(r'\d+', event.message.message)
                print_now(sz)
                sz[0] = int(sz[0])
                sz[1] = int(sz[1])
                mespin = py.get_pinyin(event.message.message)
                if 'jian' in mespin or '－' in mespin:
                    print_now('本次执行减法')
                    res = sz[0] - sz[1]
                elif 'jia' in mespin or '+' in mespin:
                    print_now('本次执行加法')
                    res = sz[0] + sz[1]
                elif 'cheng' in mespin or '*' in mespin or '×' in mespin:
                    print_now('本次执行×法')
                    res = sz[0] * sz[1]
                elif 'chu' in mespin or '/' in mespin or '÷' in mespin:
                    print_now('本次执行÷法')
                    res = sz[0] / sz[1]
                else:
                    res = 0
                print_now('计算结果：' + str(res))
                if res:
                    for button in buttons:
                        if int(button.text) == res:
                            print_now('点击提交正确答案按钮')
                            #await event.message.click(button)
                            time.sleep(sj(1,3))
                            await event.message.click(buttons.index(button))
                    '''   
                    print_now('提交过正确答案，不清楚是否成功，终止')
                    msg.append('提交过正确答案，不清楚是否成功')
                    await client.send_read_acknowledge(channel_id)
                    await client.disconnect()
                    '''
                    
                else:
                    print_now('没匹配到算法，重新获取')
                    time.sleep(sj(5,30))
                    await client.send_message(event.message.chat_id, MSG)
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
                print_now(event.message.text)
                print_now('不知道咋回事，防止意外，退出')
                msg.append(event.message.text)
                #time.sleep(sj(5,10))
                await client.send_read_acknowledge(channel_id)	#将机器人回应设为已读
                await client.disconnect()
            #await client.send_read_acknowledge(channel_id)	#将机器人回应设为已读
            #await client.disconnect()
        await client.start()
        await client.run_until_disconnected()    

async def main2(api_id, api_hash, channel_id):

    MSG = '/start'

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
        @client.on(events.NewMessage(chats=channel_id))
        @client.on(events.MessageEdited(chats=channel_id))



        async def my_event_handler(event):
            global cishu
            cishu += 1


            print_now('当前第' + str(cishu) + '次尝试')
            print_now(event.message.text)
            time.sleep(sj(5,8))

            #尝试八次，失败退出
            if cishu > 30:
                print_now('尝试次数已达到30次仍未成功，退出')
                msg.append('尝试次数已达到30仍未签到成功')
                if channel_id == '@EmbyPublicBot':
                    await client.send_message(channel_id, '/cancel')
                await client.send_read_acknowledge(channel_id)
                #await asyncio.sleep(0)
                await client.disconnect()
            #print_now(event.message)

            # 区分消息类型
            if "已经签到过" in event.message.text or "距离下次可签到" in event.message.text or '当前积分' in event.message.text:
                # 结束运行
                if '积分' in event.message.text or '总分' in event.message.text:
                    print_now('已签到，终止')
                    msg.append('已签到:')
                    print_now(event.message.text)
                    msg.append(event.message.text)
                    await client.send_read_acknowledge(channel_id) #退出运行
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
                buttons = event.message.reply_markup.rows[0].buttons
                #print_now( event.message.reply_markup.rows[0])
                if '选择您要使用的功能' in event.message.text:  #orange
                    if channel_id == '@EmbyCc_bot' or channel_id == "@Orange_Emby_Bot":
                        await event.message.click(3)
                    else:
                        await event.message.click(2)  #签到按钮所在位置
                    time.sleep(3) 
                    
                    async for msgs in client.iter_messages(channel_id, 1):  #获取最新一条消息
                        if '已经签到过' in msgs.text:   #如果签到过，运行
                            print_now(msgs.text)
                            msg.append(msgs.text)
                            await client.send_read_acknowledge(channel_id)  
                            #await asyncio.sleep(0)
                            await client.disconnect()
                        
                else:  #卷毛
                    sz = re.findall(r'\d+', event.message.message)
                    print_now(sz)
                    sz[0] = int(sz[0])
                    sz[1] = int(sz[1])
                    mespin = py.get_pinyin(event.message.message)
                    if 'jian' in mespin or '－' in mespin:
                        print_now('本次执行减法')
                        res = sz[0] - sz[1]
                    elif 'jia' in mespin or '+' in mespin:
                        print_now('本次执行加法')
                        res = sz[0] + sz[1]
                    elif 'cheng' in mespin or '*' in mespin or '×' in mespin:
                        print_now('本次执行×法')
                        res = sz[0] * sz[1]
                    elif 'chu' in mespin or '/' in mespin or '÷' in mespin:
                        print_now('本次执行÷法')
                        res = sz[0] / sz[1]
                    else:
                        res = 0
                    print_now('计算结果：' + str(res))
                    if res:
                        for button in buttons:
                            if int(button.text) == res:
                                print_now('点击提交正确答案按钮')
                                #await event.message.click(button)
                                time.sleep(sj(2,7))
                                await event.message.click(buttons.index(button))
                                await client.set_receive_updates(channel_id) #获取更新消息？
                                
                        print_now('提交过正确答案，不清楚是否成功，终止')
                        msg.append('提交过正确答案，不清楚是否成功')
                        await client.send_read_acknowledge(channel_id)
                        #await asyncio.sleep(0)
                        await client.disconnect()
                    else:
                        print_now('没匹配到算法，重新获取')
                        time.sleep(sj(5,30))
                        await client.send_message(event.message.chat_id, MSG)           

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
        '''
        js = await iter_messages(client, channel_id, me)
        print_now(js)
        if js == 0:
            await client.disconnect()
            return
        print_now('ga')
        '''
        await client.run_until_disconnected()


async def main3(api_id, api_hash, channel_id):
    
    MSG1 = '🎲更多功能'
    MSG2 = '🛎每日签到'
    MSG3 = '🎟我的积分'
    
    async with TelegramClient("id_" + str(api_id), api_id, api_hash) as client:

        me = await client.get_me() #获取当前账号信息       
        if me.username not in ''.join(msg):
            print_now(me.first_name + ' @' + me.username)
            msg.append(me.first_name + ' @' + me.username + '\n')

        print_now('\n准备去签到:' + channel_id)
        msg.append('\n准备去签到:' + channel_id)
        await client.send_message(channel_id, MSG1)
        time.sleep(sj(5,10))

        @client.on(events.NewMessage(chats=channel_id))
        @client.on(events.MessageEdited(chats=channel_id))
        async def my_event_handler(event):
            global cishu
            global is_signed
            cishu += 1
            print_now('当前第' + str(cishu) + '次尝试')
            print_now(event.message.text)
            time.sleep(sj(5,8))
            await client.send_read_acknowledge(channel_id)
            #尝试八次，失败退出
            if cishu > 30:
                print_now('尝试次数已达到10次仍未成功，退出')
                msg.append('尝试次数已达到10仍未签到成功')

                await client.send_read_acknowledge(channel_id)
                #await asyncio.sleep(0)
                await client.disconnect()
            #print_now(event.message)

            # 区分消息类型
            if "已经签到过" in event.message.text or "距离上次签到" in event.message.text or '您的积分' in event.message.text:
                # 结束运行
                is_signed = True

                if '积分' in event.message.text or '总分' in event.message.text:
                    print_now('已签到，终止')
                    msg.append('已签到:')
                    print_now(event.message.text)
                    msg.append(event.message.text)
                    await client.send_read_acknowledge(channel_id) #退出运行
                    #await asyncio.sleep(0)
                    time.sleep(3)
                    await client.disconnect()
                else:
                    await client.send_message(channel_id, MSG1)  #查询积分
            elif "请输入验证码" in event.message.text:  # 获取图像验证码
                
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
            elif "验证码错误" in event.message.text or "选择您要使用的功能" in event.message.text: 
                print_now('重新开始。。。')
                await client.send_message(channel_id, MSG1)
            elif '签到成功' in event.message.text or '你回答正确' in event.message.text:
                msg.append(event.message.text)
                print_now(event.message.text)
                is_signed = True
                await client.send_read_acknowledge(channel_id)
                #await asyncio.sleep(0)
                await client.disconnect()
            elif "请选择功能" in event.message.text: 
                print_now(is_signed)
                if is_signed:
                    await client.send_message(channel_id, MSG3)
                else:

                    await client.send_message(channel_id, MSG2)
                await client.send_read_acknowledge(channel_id)

            # 是否成功签到
                '''

            else :
                print_now('不知道咋回事，防止意外，退出')
                msg.append('出现意外，未签到')
                #time.sleep(sj(5,10))
                await client.send_read_acknowledge(channel_id)	#将机器人回应设为已读
                #await asyncio.sleep(0)
                await client.disconnect()      
                '''     
        await client.start()

        await client.run_until_disconnected()




if __name__ == "__main__":
    msg = []
    print('共' + str(len(API_ID)) + '个账户：' + API_ID1.replace('&', '  '))
    print('签到bot：' + '  '.join(CHANNEL_ID))
    zh = 0
    for i in API_ID:       
        zh += 1 
        print_now('\n\n************开始执行账号' + str(zh) + '：' + str(i) + '：' '************\n')
        msg.append('\n*********账号' + str(zh) + '：' + str(i) + '：' '*********\n')
        yc = sj(3,10)
        #print_now('随机延迟' + str(yc) + '秒后开始执行')
        #time.sleep(yc)
        shuffle(CHANNEL_ID)
        for j in CHANNEL_ID:
            if i == API_ID[0] and j == CHANNEL_ID[1]:
                #continue
                a = 1
            cishu = 0     #每个账号尝试签到次数
            is_signed = False
            if j == '@Orange_Emby_Bot' or j == '@peach_emby_bot' or j == '@EmbyCc_bot':  
                asyncio.run(main2(i, API_HASH[API_ID.index(i)], j))
            elif j == '@EmbyMistyBot':
                asyncio.run(main3(i, API_HASH[API_ID.index(i)], j))
            else:
                asyncio.run(main1(i, API_HASH[API_ID.index(i)], j))
            #main(i, API_HASH[API_ID.index(i)], j)
            #break
    
    if int(now.strftime('%H')) > 12:
        print_now('当前小时为' + now.strftime('%H') + '发送通知。。。')
        send('TG签到', '\n'.join(msg))  
    else:
        print_now('当前小时为'+ now.strftime('%H') + '取消通知')
    exit(0)
