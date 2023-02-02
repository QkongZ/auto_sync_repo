#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 觉得好用请点 *star*，作者仓库:https://github.com/rpgrpg/freenom-qinglong.git

'''
cron: 19 19 * * 5
new Env:('freenom域名自动续期');
'''
# 配置环境变量：export freenom_usr=""，""内为你自己的FREENOM的用户名
# 配置环境变量：export freenom_psd=""，""内为你自己的FREENOM密码
# V20228

import requests
import re,os
try:
    from notify import send
except:
    print("upload notify failed")
    exit(-1)
try:
    # 没有设置环境变量可以在此处直接填写freenom用户名，示例：username = '87654321@qq.com'
    username = os.environ["freenom_usr"]
    # 没有设置环境变量可以在此处直接填写freenom密码，示例：password = '12345678'
    password = os.environ["freenom_psd"]
except:
    print("请设置环境变量freenom_usr和freenom_psd.")
# 登录url
LOGIN_URL = 'https://my.freenom.com/dologin.php'
# 域名状态url
DOMAIN_STATUS_URL = 'https://my.freenom.com/domains.php?a=renewals'
# 续期url
RENEW_DOMAIN_URL = 'https://my.freenom.com/domains.php?submitrenewals=true'

# 登录匹配
token_ptn = re.compile('name="token" value="(.*?)"', re.I)
domain_info_ptn = re.compile(
    r'<tr><td>(.*?)</td><td>[^<]+</td><td>[^<]+<span class="[^<]+>(\d+?).Days</span>[^&]+&domain=(\d+?)">.*?</tr>',
    re.I)
login_status_ptn = re.compile('<a href="logout.php">Logout</a>', re.I)
sess = requests.Session()
sess.headers.update({
    'user-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/103.0.5060.134 Safari/537.36'
})
sess.headers.update({
    'content-type': 'application/x-www-form-urlencoded',
    'referer': 'https://my.freenom.com/clientarea.php'
})

try:  # 异常捕捉
    r = sess.post(LOGIN_URL, data={'username': username, 'password': password})

    if r.status_code != 200:
        print('Can not login. Pls check username&password.')
        exit(-1)

    # 查看域名状态
    sess.headers.update({'referer': 'https://my.freenom.com/clientarea.php'})
    r = sess.get(DOMAIN_STATUS_URL)
except:
    print('Network failed.')
    send(f'freenom域名自动续期','Network failed.')
    exit(-1)
# 确认登录状态
if not re.search(login_status_ptn, r.text):
    print('login failed, retry')
    exit(-1)

# 获取token
page_token = re.search(token_ptn, r.text)
if not page_token:
    print('page_token missed')
    exit(-1)
token = page_token.group(1)

# 获取域名列表
domains = re.findall(domain_info_ptn, r.text)
#print(domains)
domains_list = []
renew_domains_succeed = []
renew_domains_failed = []
message = ''
message_successed = ''
message_failed = ''
message += '账户' + username + '所有域名情况如下：\n'

# 域名续期
for domain, days, renewal_id in domains:
    days = int(days)
    domains_list.append(f'{domain} 还有 {days} 天到期')
    message = message + domain + ' 还有 ' + str(days) + ' 天到期\n'
    if days < 14:
        sess.headers.update({
            'referer':
            f'https://my.freenom.com/domains.php?a=renewdomain&domain={renewal_id}',
            'content-type': 'application/x-www-form-urlencoded'
        })
        try:
            r = sess.post(RENEW_DOMAIN_URL,
                          data={
                              'token': token,
                              'renewalid': renewal_id,
                              f'renewalperiod[{renewal_id}]': '12M',
                              'paymentmethod': 'credit'
                          })
        except:
            message_failed += 'Network failed.\n'
            message_failed += '请自行访问freenom官网查看\n'
            print('Network failed.')
            exit(-1)
        if r.text.find('Order Confirmation') != -1:
            message_successed = message_successed + domain + ' 续期成功\n'
            renew_domains_succeed.append(domain)
        else:
            message_failed = message_failed + domain + ' 续期失败\n'
            renew_domains_failed.append(domain)

# 输出结果并推送通知
#print(domains_list, renew_domains_succeed, renew_domains_failed)
if message_successed:
    message = message + '\n\n' + message_successed + '\n\n'
if message_failed:
    message = message + '\n\n' + message_failed + '\n\n'
message += '\nfreenom官网(https://my.freenom.com/domains.php?a=renewals)'
#print(message)
send(f'freenom域名自动续期',f'{message}')

'''
if renew_domains_failed:
    send('Caution! ', f'renew failed:{renew_domains_failed}')
else:
    send(f'{message}')
'''
