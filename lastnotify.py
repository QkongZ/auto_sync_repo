
#!/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author : https://github.com/qingshanh/ymp
# @Time : 2022/8/10 13:23
# const $ = new Env("本月最后一天通知");



from requests import post, get
from time import sleep, time
from datetime import datetime
from os import environ
from datetime import datetime, timedelta
from sendNotify import send
import re

now = datetime.now()
"""读取环境变量"""
lastday = environ.get("lastday") if environ.get("lastday") else True

def is_last_day_of_month():
    """
    判断今天是否为本月最后一天。
    
    返回:
    - True: 如果今天是本月最后一天。
    - False: 如果今天不是本月最后一天。
    """
    # 获取当前日期
    today = datetime.now()
    
    # 计算明天的日期
    tomorrow = today + timedelta(days=1)
    # 判断今天是否为本月最后一天：如果明天是下个月的第一天，则今天是本月最后一天
    return today.month != tomorrow.month

# 测试函数
x = is_last_day_of_month()
if x and lastday:
    nt = '当前为本月最后一天，请及时领取：\n'
    print(nt)
    send('本月最后一天', nt + lastday)
else:
    print(f"当前为本月 {now.day} 号")
