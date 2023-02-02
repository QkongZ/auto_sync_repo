/*
22 14 * * * caoliu论坛自动回帖
*/
const $ = new Env("小草自动回帖");
const notify = $.isNode() ? require('./sendNotify') : '';
let clcookie = '', clcookiesArr = [], cookie = '', message = '', username='',level='',ww='',ip='',lastlogintime='',money='',gx='',tz='',newmessagetitle='',newmessagecontent='',newmessageauthor='',newmessagetime='';
let hqck='',hqlx='',hqcktime='',dqck='',dqlx='',dqcktime='',dqdqtime='',allmoney='',isnewmessage,newmessageurl,newmessageurlold=''
let ismessage,UA='',urlarr=[],authorarr=[],urlarrs=[],authorarrs=[],blacklist=[],blacklists=[],isrun,titlearr=[],titlearrs=[]
let tidarrs=[],replycount='',reply_news='',reply_news_arr=[],myuid='',jrft=''
if (process.env.clcookie) {
  if (process.env.clcookie.indexOf('&') > -1) {
    clcookiesArr = process.env.clcookie.split('&');
  } else if (process.env.clcookie.indexOf('\n') > -1) {
    clcookiesArr = process.env.clcookie.split('\n');
  } else if (process.env.clcookie.indexOf('@') > -1) {
    clcookiesArr = process.env.clcookie.split('@');
  } else {
    clcookiesArr = [process.env.clcookie];
  }
}
let time = new Date()
if (process.env.clua) {
    UA = process.env.clua
}
reply_news_arr = ['1024','感谢分享','感谢你的分享','谢谢分享','多谢分享','感谢作者分享','谢谢坛友分享','感谢分享','支持分享','支持发帖','感谢发帖']
replycount = (process.env.clreplycount) ? process.env.clreplycount : 10
!(async () => {
    if (!clcookiesArr[0]) {
        $.msg($.name, '请先添加cookie');
        return;
    }
    if (!UA) {
        console.log('需手动抓取ua才可运行,且需保证cookie与ua对应,变量为：clua')
        return;
    }
    console.log("共" + clcookiesArr.length + "个账号")
    ismessage = false
    for (let i = 0; i < clcookiesArr.length; i++) {
        if (clcookiesArr[i]) {
            cookie = clcookiesArr[i]
            $.index = i + 1;
            $.nickName = '';
            islogin = true
            isnewmessage = true
            newmessageurl=''
            isrun = true
            jrft = ''
            console.log(`\n******开始【账号${$.index}】*********\n`);
            await getbaseinfo()
            await $.wait(1500)
            await getmyuid()
            if (!isrun) {
                //await 
                continue
            }
            if (!islogin) {               
                continue
            }
            await $.wait(1500)
            await gettodayurl() 

            if (isrun) {
                if (replycount > 60 - jrft) {
                    if (60 - jrft > 0) {
                        replycount = 60 - jrft
                    } else {
                        console.log('您今日回帖数量已超过60，停止回帖')
                        continue
                    }

                }                
                if (replycount > tidarrs.length) {
                    replycount = tidarrs.length

                } else {
                    
                }
                console.log(`本次将回复 ${replycount} 个帖子`)
                for (var j = 0; j < replycount; j++) {
                    var a = random(0,reply_news_arr.length - 1)
                    var reply_news = reply_news_arr[a]
                    var x = random(0,tidarrs.length - 1)
                    var y = random(1025000,1600000)
                    //console.log(a,reply_news_arr.length,reply_news,x,y)
                    console.log(`当前在第 ${j+1} 次回复，回复帖子为 ${authorarrs[x]} 的: ${titlearrs[x]} ,回复内容为: ${reply_news} `)
                    await reply(tidarrs[x],titlearrs[x],reply_news)
                    var z = tidarrs.length

                    authorarrs.splice(x,1)
                    titlearrs.splice(x,1)
                    tidarrs.splice(x,1)
                    if (!isrun || tidarrs.length != z - 1) {
                        break
                    }                    
                    console.log(`随机等待${y/1000}秒后回复下一个\n`)
                    await $.wait(y)
                }
                //await reply()
                 
            }          

                        
        }
    }
    if (message !== '' && (ismessage || time.getHours()  == 21)) {
        
        if ($.isNode()) {
            await notify.sendNotify($.name, message, '', `\n`);
        } else {
            $.msg($.name, '', message);
        }
    }
})()
    .catch((e) => {
        $.log('', `❌ ${$.name}, 失败! 原因: ${e}!`, '')
    })
    .finally(() => {
        $.done();
    })

function getmyuid() {
    return new Promise(resolve => {
        $.get(geturl('profile.php'),async (err, resp, data) => {
            try {
                if (err) {
                    $.logErr(err)
                } else {
                    if (data) {
                        //console.log(data)
                        myuid = /\（UID\:(\d+)\）/.exec(data)[1]
                        console.log('UID:' + myuid)
                        await gettodaysend()
                    }
                }
            } catch (e) {
                $.logErr(e)
            } finally {
                resolve();
            }
        })
            
    })  

}


async function gettodaysend() {
    return new Promise(resolve => {
        $.get(geturl('profile.php?action=show&uid='+myuid), (err, resp, data) => {
            try {
                if (err) {
                    $.logErr(err)
                } else {
                    if (data) {
                        //console.log(data)
                        var ft = /平均每日發帖\<\/th\>\<th\>(.+?)\</.exec(data)[1]
                        jrft = /今日(\d+)篇/.exec(ft)[1]
                        console.log(ft)
                        message += ft
                    }
                }
            } catch (e) {
                $.logErr(e)
            } finally {
                resolve();
            }
        })
            
    })  

}


async function reply(tid,title,reply) {
    title = 'Re:' + title
    return new Promise(resolve => {
        $.post(posturl("post.php?",tid,title,reply), (err, resp, data) => {
            try {
                if (err) {
                    $.logErr(err)
                } else {
                    if (data) {
                        //console.log(data)
                        
                        if (data.indexOf('發貼完畢點擊') != -1) {
                            console.log('回复成功')
                            isrun = true
                            return
                        } else if (data.indexOf('所屬的用戶組') != -1) {
                            console.log('所属用户组今日回帖已达上限，停止回复')
                            isrun = false
                            return
                        } else if (data.indexOf('灌水預防機制') != -1) {
                            console.log('新手1024秒限制中')
                            isrun = true
                            return;
                        }
                    } else {
                        isrun = false
                    }
                    
                }
            } catch (e) {
                $.logErr(e)
            } finally {
                resolve();
            }
        })
    })
}

async function gettodayurl() {
    return new Promise(resolve => {
        $.get(geturl('thread0806.php?fid=7&search=today'), (err, resp, data) => {
            try {
                if (err) {
                    $.logErr(err)
                } else {
                    if (data) {
                        //console.log(data)
                        var ptzt
                        if (data.indexOf('普通主題') != -1) {

                            ptzt = data.indexOf('普通主題')
                            //console.log(ptzt)
                        }
                        //data=JSON.stringify(data)
                        data=data.slice(ptzt)
                        //console.log(ptzt)
                        var retodayurl=/\<h3\>\<a href\=\"(.+?)\"/g
                        var retodayauthor=/href\=\".+?class=\"bl\"\>(.+?)\<\/a\>/g
                        var retodaytitle=/target\=\"\_blank\" id\=\"\"\>(.+?)\</g
                        urlarr=data.match(retodayurl)
                        //console.log(urlarr)
                        for (var i = 0; i < urlarr.length; i++) {
                            if (urlarr[i].indexOf('tid') != -1) {
                                tidarrs.push(urlarr[i].match(/tid\=(\d+)\"/)[1])
                            } else if (urlarr[i].indexOf('html') != -1) {
                                tidarrs.push(urlarr[i].match(/htm_data\/\d+\/\d+\/(\d+)\.html/)[1])
                            } else {
                                console.log('出错了，停止运行')
                                isrun = false
                                return
                            }
                            
                        }
                        authorarr=data.match(retodayauthor)
                        for (var i = 0; i < authorarr.length; i++) {
                            authorarrs.push(authorarr[i].match(/bl\"\>(.+?)\</)[1])
                        } 
                        titlearr=data.match(retodaytitle)  
                        for (var i = 0; i < titlearr.length; i++) {
                            titlearrs.push(titlearr[i].match(/\>(.+?)\</)[1])
                        }  
                        if(authorarrs.length != tidarrs.length || authorarrs.length != titlearrs.length) {
                            console.log('出错了，停止运行')
                            isrun = false
                            return
                        }                   
                        //console.log(tidarrs)
                        //console.log(authorarrs)
                        //console.log(titlearrs)
                        for (var i = authorarrs.length - 1; i > -1; i--) {
                            //console.log(i,tidarrs.length)
                            if (blacklists.indexOf(authorarrs[i]) != -1) {
                                console.log(`发现黑名单${authorarrs[i]}的帖子${titlearrs}:${tidarrs[i]},进行移除`)
                                tidarrs.splice(i,1)
                                titlearrs.splice(i,1)
                                authorarrs.splice(i,1)
                                if (tidarrs.indexOf(authorarrs[i]) == -1 && titlearrs.indexOf(authorarrs[i]) == -1) {
                                    console.log('移除成功,剩余列表长度' + tidarrs.length)
                                    
                                } else {
                                    console.log('移除黑名单帖子失败，停止运行')
                                    isrun = false
                                    return;
                                }

                            }
                        }
                        if(titlearrs.length != tidarrs.length) {
                            console.log('出错了，停止运行')
                            isrun = false
                            return
                        }    
                        //console.log(tidarrs)
                        console.log('获取帖子成功，开始回帖')
                        isrun = true
                    }
                }
            } catch (e) {
                $.logErr(e)
            } finally {
                resolve();
            }
        })
            
    })  

}

function random(b, a) {
    randomtime = Math.round(Math.random() * (a - b) + b)
    return randomtime
}

async function getbaseinfo() {
    return new Promise(resolve => {
        $.get(geturl('index.php'), async (err, resp, data) => {
            try {
                if (err) {
                    $.logErr(err)
                } else {
                    if (data) {
                        //console.log('基础信息'+data)
                        if (data.indexOf('您尚未') != -1) {
                           console.log(`账号${$.index}cookie已失效，请重新抓取`)
                           islogin = false 
                           message += `账号${$.index}cookie已失效，请重新抓取\n\n`
                           return
                        } else if (data.indexOf('禁止發言') != -1) {
                            username = /font-weight\:bold\"\>(.+?)\</.exec(data)[1]
                            console.log('您的账号被禁言，请去查看原因，退出运行')
                            await notify.sendNotify($.name,`用户${$.index}:${username}已被禁言，请去查看原因`)
                            isrun = false
                            return
                        }
                        
                       username = /font-weight\:bold\"\>(.+?)\</.exec(data)[1]
                       
                       level = /span class\=\"s3\"\>(.+?)\</.exec(data)[1]
                       lastlogintime = /上次登錄時間\:(.+?)\|/.exec(data)[1]
                       ip = /您的IP \:(.+?)\</.exec(data)[1]
                       ww = /威望\:(.+?)\|/.exec(data)[1]
                       money = /金錢\:(.+?)\|/.exec(data)[1]
                       gx = /貢獻\:(.+?)\|/.exec(data)[1]
                       tz = /共發表帖子\:(.+?)\|/.exec(data)[1]
                       console.log(`用户${$.index}：${username}\n等级：${level}\n上次登录时间：${lastlogintime}\n当前IP：${ip}\n威望：${ww}\n金钱：${money}\n贡献：${gx}\n共发表帖子：${tz}`)
                       message += `用户${$.index}：${username}\n等级：${level}\n上次登录时间：${lastlogintime}\n当前IP：${ip}\n威望：${ww}\n金钱：${money}\n贡献：${gx}\n共发表帖子：${tz}`
                        var reblacklist = /action=show&username\=(.+?)\"\>/g
                        //console.log(data)
                        blacklist = data.match(reblacklist)
                        for (var i = 0; i < blacklist.length; i ++) {
                            blacklists.push(/name\=(.+?)\"/.exec(blacklist[i])[1])
                        }
                        blacklists = blacklists.concat(['administrator','vonder','痴儿','lj413025','老地方见','大紅鷹','tsq456'])
                        //console.log(blacklists)
                    }
                }
            } catch (e) {
                $.logErr(e)
            } finally {
                resolve();
            }
        })
    })
}

async function getbankinfo() {
    return new Promise(resolve => {
        $.get(geturl("hack.php?H_name=bank"), (err, resp, data) => {
            try {
                if (err) {
                    $.logErr(err)
                } else {
                    if (data) {
                        //console.log(data)
                        hqck = /活期存款：(.+?)\</.exec(data)[1]
                        hqlx = /利息：(.+?)\</.exec(data)[1]
                        hqcktime = /\>存款时间(.+?)\</.exec(data)[1]
                        dqck = /定期存款：(.+?)\</.exec(data)[1]
                        dqlx = /定期存款：.+?　　利息：(.+?)\</.exec(data)[1]
                        dqcktime = /定期存款：.+?存款时间：(.+?)\</.exec(data)[1]
                        dqdqtime = /到期时间：(.+?)\</.exec(data)[1]
                        allmoney = /总资产：(.+?)USD/.exec(data)[1]
                        //dqck = /定期存款：(.+?)\</.exec(data)[1]
                        console.log(`活期存款：${hqck}\n活期利息：${hqlx}\n活期存款时间：${hqcktime}\n定期存款：${dqck}\n定期利息：${dqlx}\n定期存款时间：${dqcktime}\n定期到期时间：${dqdqtime}\n总资产：${allmoney}\n`)
                        message += `活期存款：${hqck}\n活期利息：${hqlx}\n活期存款时间：${hqcktime}\n定期存款：${dqck}\n定期利息：${dqlx}\n定期存款时间：${dqcktime}\n定期到期时间：${dqdqtime}\n总资产：${allmoney}\n\n`
                      
                    }
                }
            } catch (e) {
                $.logErr(e)
            } finally {
                resolve();
            }
        })
    })
}

function geturl(url) {
    const options = {
        url: "http://t66y.com/" + url,
        headers: {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': cookie,
            'DNT': '1',
            'Host': 't66y.com',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://t66y.com/index.php',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': UA,

        }
    };
    //console.log(cookie)
    return options

}
function posturl(url,tid,title,reply_news) {
    let opt = {
        url: "http://t66y.com/" + url,
        headers: {
            //'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',

            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie,
            'DNT': '1',
            'Host': 't66y.com',
            'Origin': 'null',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': UA,

            
        },
        
        body: `atc_usesign=1&atc_convert=1&atc_autourl=1&atc_title=${title}&atc_content=${reply_news}&step=2&action=reply&fid=7&tid=${tid}&atc_attachment=none&pid=&article=&touid=&verify=verify`

    }
    //console.log(opt)
    return opt
}


// prettier-ignore

function Env(t, e) { "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0); class s { constructor(t) { this.env = t } send(t, e = "GET") { t = "string" == typeof t ? { url: t } : t; let s = this.get; return "POST" === e && (s = this.post), new Promise((e, i) => { s.call(this, t, (t, s, r) => { t ? i(t) : e(s) }) }) } get(t) { return this.send.call(this.env, t) } post(t) { return this.send.call(this.env, t, "POST") } } return new class { constructor(t, e) { this.name = t, this.http = new s(this), this.data = null, this.dataFile = "box.dat", this.logs = [], this.isMute = !1, this.isNeedRewrite = !1, this.logSeparator = "\n", this.startTime = (new Date).getTime(), Object.assign(this, e), this.log("", `🔔${this.name}, 开始!`) } isNode() { return "undefined" != typeof module && !!module.exports } isQuanX() { return "undefined" != typeof $task } isSurge() { return "undefined" != typeof $httpClient && "undefined" == typeof $loon } isLoon() { return "undefined" != typeof $loon } toObj(t, e = null) { try { return JSON.parse(t) } catch { return e } } toStr(t, e = null) { try { return JSON.stringify(t) } catch { return e } } getjson(t, e) { let s = e; const i = this.getdata(t); if (i) try { s = JSON.parse(this.getdata(t)) } catch { } return s } setjson(t, e) { try { return this.setdata(JSON.stringify(t), e) } catch { return !1 } } getScript(t) { return new Promise(e => { this.get({ url: t }, (t, s, i) => e(i)) }) } runScript(t, e) { return new Promise(s => { let i = this.getdata("@chavy_boxjs_userCfgs.httpapi"); i = i ? i.replace(/\n/g, "").trim() : i; let r = this.getdata("@chavy_boxjs_userCfgs.httpapi_timeout"); r = r ? 1 * r : 20, r = e && e.timeout ? e.timeout : r; const [o, h] = i.split("@"), n = { url: `http://${h}/v1/scripting/evaluate`, body: { script_text: t, mock_type: "cron", timeout: r }, headers: { "X-Key": o, Accept: "*/*" } }; this.post(n, (t, e, i) => s(i)) }).catch(t => this.logErr(t)) } loaddata() { if (!this.isNode()) return {}; { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e); if (!s && !i) return {}; { const i = s ? t : e; try { return JSON.parse(this.fs.readFileSync(i)) } catch (t) { return {} } } } } writedata() { if (this.isNode()) { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e), r = JSON.stringify(this.data); s ? this.fs.writeFileSync(t, r) : i ? this.fs.writeFileSync(e, r) : this.fs.writeFileSync(t, r) } } lodash_get(t, e, s) { const i = e.replace(/\[(\d+)\]/g, ".$1").split("."); let r = t; for (const t of i) if (r = Object(r)[t], void 0 === r) return s; return r } lodash_set(t, e, s) { return Object(t) !== t ? t : (Array.isArray(e) || (e = e.toString().match(/[^.[\]]+/g) || []), e.slice(0, -1).reduce((t, s, i) => Object(t[s]) === t[s] ? t[s] : t[s] = Math.abs(e[i + 1]) >> 0 == +e[i + 1] ? [] : {}, t)[e[e.length - 1]] = s, t) } getdata(t) { let e = this.getval(t); if (/^@/.test(t)) { const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t), r = s ? this.getval(s) : ""; if (r) try { const t = JSON.parse(r); e = t ? this.lodash_get(t, i, "") : e } catch (t) { e = "" } } return e } setdata(t, e) { let s = !1; if (/^@/.test(e)) { const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e), o = this.getval(i), h = i ? "null" === o ? null : o || "{}" : "{}"; try { const e = JSON.parse(h); this.lodash_set(e, r, t), s = this.setval(JSON.stringify(e), i) } catch (e) { const o = {}; this.lodash_set(o, r, t), s = this.setval(JSON.stringify(o), i) } } else s = this.setval(t, e); return s } getval(t) { return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null } setval(t, e) { return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null } initGotEnv(t) { this.got = this.got ? this.got : require("got"), this.cktough = this.cktough ? this.cktough : require("tough-cookie"), this.ckjar = this.ckjar ? this.ckjar : new this.cktough.CookieJar, t && (t.headers = t.headers ? t.headers : {}, void 0 === t.headers.Cookie && void 0 === t.cookieJar && (t.cookieJar = this.ckjar)) } get(t, e = (() => { })) { t.headers && (delete t.headers["Content-Type"], delete t.headers["Content-Length"]), this.isSurge() || this.isLoon() ? (this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.get(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) })) : this.isQuanX() ? (this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t))) : this.isNode() && (this.initGotEnv(t), this.got(t).on("redirect", (t, e) => { try { if (t.headers["set-cookie"]) { const s = t.headers["set-cookie"].map(this.cktough.Cookie.parse).toString(); s && this.ckjar.setCookieSync(s, null), e.cookieJar = this.ckjar } } catch (t) { this.logErr(t) } }).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) })) } post(t, e = (() => { })) { if (t.body && t.headers && !t.headers["Content-Type"] && (t.headers["Content-Type"] = "application/x-www-form-urlencoded"), t.headers && delete t.headers["Content-Length"], this.isSurge() || this.isLoon()) this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.post(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) }); else if (this.isQuanX()) t.method = "POST", this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t)); else if (this.isNode()) { this.initGotEnv(t); const { url: s, ...i } = t; this.got.post(s, i).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) }) } } time(t, e = null) { const s = e ? new Date(e) : new Date; let i = { "M+": s.getMonth() + 1, "d+": s.getDate(), "H+": s.getHours(), "m+": s.getMinutes(), "s+": s.getSeconds(), "q+": Math.floor((s.getMonth() + 3) / 3), S: s.getMilliseconds() }; /(y+)/.test(t) && (t = t.replace(RegExp.$1, (s.getFullYear() + "").substr(4 - RegExp.$1.length))); for (let e in i) new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? i[e] : ("00" + i[e]).substr(("" + i[e]).length))); return t } msg(e = t, s = "", i = "", r) { const o = t => { if (!t) return t; if ("string" == typeof t) return this.isLoon() ? t : this.isQuanX() ? { "open-url": t } : this.isSurge() ? { url: t } : void 0; if ("object" == typeof t) { if (this.isLoon()) { let e = t.openUrl || t.url || t["open-url"], s = t.mediaUrl || t["media-url"]; return { openUrl: e, mediaUrl: s } } if (this.isQuanX()) { let e = t["open-url"] || t.url || t.openUrl, s = t["media-url"] || t.mediaUrl; return { "open-url": e, "media-url": s } } if (this.isSurge()) { let e = t.url || t.openUrl || t["open-url"]; return { url: e } } } }; if (this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r))), !this.isMuteLog) { let t = ["", "==============📣系统通知📣=============="]; t.push(e), s && t.push(s), i && t.push(i), console.log(t.join("\n")), this.logs = this.logs.concat(t) } } log(...t) { t.length > 0 && (this.logs = [...this.logs, ...t]), console.log(t.join(this.logSeparator)) } logErr(t, e) { const s = !this.isSurge() && !this.isQuanX() && !this.isLoon(); s ? this.log("", `❗️${this.name}, 错误!`, t.stack) : this.log("", `❗️${this.name}, 错误!`, t) } wait(t) { return new Promise(e => setTimeout(e, t)) } done(t = {}) { const e = (new Date).getTime(), s = (e - this.startTime) / 1e3; this.log("", `🔔${this.name}, 结束! 🕛 ${s} 秒`), this.log(), (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(t) } }(t, e) }
