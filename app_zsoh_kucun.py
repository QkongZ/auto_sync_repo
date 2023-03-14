from requests import get

from sendNotify import send
import time
def main():

    u="http://lwintegral.wznbw.com/addons/leescore/index/ajaxGoodlist?appid=2"

    res=get(u).json()

    res=res["data"]

    msg=""
    jk = ['枕头', '吹风机','茶具','锅']
    for item in res:

        if item["stock"] > 0:
            
            timeArr=time.localtime(item["updatetime"])
            other=time.strftime("%Y-%m-%d %H:%M:%S",timeArr)
            msg += f'{item["name"]} 还有 {item["stock"]} 件库存\n需要积分 {item["scoreprice"]} \n更新时间 {other}\nhttp://lwintegral.wznbw.com{item["thumb"]}\n\n'

    print(msg)
    for a in jk:
        if a in msg:
            send("掌上瓯海库存", msg)

main()
