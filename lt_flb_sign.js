/*
2 0,20 * * * 福利吧论坛签到
ck变量
export flbcookie=""
*/
const $ = new Env("福利吧签到");
//const jdCookieNode = $.isNode() ? require('./jdCookie.js') : '';
const notify = $.isNode() ? require('./sendNotify') : '';
let flbcookie = '', flbcookiesArr = [], cookie = '', message = '', formhash='', signdetail='',issign, username='',fl='',ax='',jf='',yhz='',fx='',jb='',xx='',newmessage,islogin,signsuc;
let ismessage
let Host = ''
if (process.env.flbcookie) {
  if (process.env.flbcookie.indexOf('&') > -1) {
    flbcookiesArr = process.env.flbcookie.split('&');
  } else if (process.env.flbcookie.indexOf('\n') > -1) {
    flbcookiesArr = process.env.flbcookie.split('\n');
  } else if (process.env.flbcookie.indexOf('@') > -1) {
    clcookiesArr = process.env.flbcookie.split('@');
  } else {
    flbcookiesArr = [process.env.flbcookie];
  }
}
let time = new Date()

!(async () => {
    if (!flbcookiesArr[0]) {
        $.msg($.name, '请先添加cookie，变量名 flbcookie');
        return;
    }
    console.log("共" + flbcookiesArr.length + "个账号")
    //await gethost()
    if (!Host) {
        Host = 'www.wnflb2023.com'
        console.log("未获取到host，使用固定host:" + Host)
        
    } else {
        console.log("获取到论坛最新地址："+ Host) 
    }
    ismessage = false
    await $.wait(600)
    console.log(new Date())
    for (let i = 0; i < flbcookiesArr.length; i++) {
        if (flbcookiesArr[i]) {
            cookie = flbcookiesArr[i]
            $.index = i + 1;
            $.nickName = '';
            islogin = true
            signsuc = true
            issign = false
            console.log(`\n******开始【账号${$.index}】*********\n`);
            console.log(new Date())
            await getformhash()
            if (!islogin) {
                console.log("cookie失效")
                await notify.sendNotify($.name,`用户${$.index} cookie已失效`);
                continue
            }            
            if (!issign) {
                
                console.log(`用户${$.index}: ${username}尚未签到，现在去签到`)
                await sign(formhash);
                if (!signsuc) {
                    //await $.wait(500)
                    await sign(formhash);
                }
            }
            
            if (time.getHours() != 0 && time.getHours() != 23) await home()

        }
    }
    if (process.env.JSRUN && (time.getHours() == 19 || time.getHours() == 10)) await jsrunsign()
    if (message !== '' && ismessage) {
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


function jsrunsign() {
    const options = {
        url: 'https://jsrun.net/uc/getTodayCash',
        headers: {

            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Connection": "keep-alive",
            "Cookie": process.env.JSRUN,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate",
        }
    };
    return new Promise(resolve => {
        $.get(options, (err, resp, data) => {
            try {
                if (err) {
                    $.logErr(err)
                } else {
                    if (data) {
                        console.log(data)
                         
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

async function home() {
    const options = {
        url: "https://" + Host + "/home.php?mod=spacecp&ac=credit&showcredit=1",
        headers: {
            "Host": Host,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://" + Host + "/plugin.php?id=fx_checkin:list",
            "Accept-Encoding": "gzip, deflate",
        }
    };
    return new Promise(resolve => {
        $.get(options, (err, resp, data) => {
            try {
                if (err) {
                    $.logErr(err)
                } else {
                    if (data) {
                        //console.log(data)                        
                        var reyhz = /showUpgradeinfo\)\"\>(.+?)\</
                        var rejf = /积分\: \<\/em\>(.+?) \</
                        var refl = /福利\: \<\/em\>(.+?) \</
                        var refx = /分享\: \<\/em\>(.+?) \</
                        var rejh = /精华\: \<\/em\>(.+?) \</
                        var reax = /爱心\: \<\/em\>(.+?) \</
                        var rejb = /金币\: \<\/em\>(.+?) \&/
                        yhz = data.match(reyhz)[1]
                        jf = data.match(rejf)[1]
                        fl = data.match(refl)[1]
                        fx = data.match(refx)[1]
                        jh = data.match(rejh)[1]
                        ax = data.match(reax)[1]
                        jb = data.match(rejb)[1]
                        console.log(yhz)
                        console.log('积分：'+jf)
                        console.log("福利："+fl)
                        console.log("分享："+fx)
                        console.log("精华："+jh)
                        console.log("爱心："+ax)
                        console.log("金币：" +jb)
                        //yhz=yhzmatch[1]
                        //console.log(yhz)
                        message += yhz + '\n积分：'+jf+"\n福利："+fl+"\n分享："+fx+"\n精华："+jh+"\n爱心："+ax+"\n金币：" +jb+'\n\n'
                        if (data.indexOf('class=\"new') != -1 || data.indexOf('提醒(') != -1) {
                            ismessage = true
                            message +=  `用户${$.index}：${username} 有新消息待处理\n\n`
                            console.log(`用户${$.index}：${username} 有新消息待处理\n`)
                        }
                        
                        
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


function getformhash() {
    const options = {
        url: "https://" + Host + "/plugin.php?id=fx_checkin:checkin",
        headers: {
            "Host": Host,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://" + Host + "/plugin.php",
            "Accept-Encoding": "gzip, deflate",
        }
    };
    return new Promise(resolve => {
        $.get(options, (err, resp, data) => {
            try {
                if (err) {
                    $.logErr(err)
                } else {
                    if (data) {
                        //console.log(data)
                        if (data.indexOf("您尚未登录") != -1) {
                            islogin = false
                            return
                        }
                        var reformhash = /formhash=(.+?)\"/
                        var reusername = /访问我的空间\"\>(.+?)\</
                        var resigndetail = /tip_c\"\>(.+?)\</
                        var formhashmatch = data.match(reformhash)
                        username = data.match(reusername)[1]
                        formhash = formhashmatch[1]
                        signdetail = data.match(resigndetail)[1]
                        //console.log('formhash是:'+formhash)
                        if (data.indexOf("已签到") != -1) {  
                            console.log("用户" + $.index +': '+ username + " 已签到\n签到详情：" + signdetail)   
                            message += "用户" + $.index +': '+ username + " 已签到\n签到详情："  + signdetail +'\n'                  
                            issign=true;
                        } else {
                            issign=false;
                        }                        
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

function sign(formhash) {
    const options = {
        url: `https://${Host}/plugin.php?id=fx_checkin:checkin&formhash=${formhash}&${formhash}&infloat=yes&handlekey=fx_checkin&inajax=1&ajaxtarget=fwin_content_fx_checkin`,
        headers: {
            "Host": Host,
            "Accept": "*/*",
            "Connection": "keep-alive",
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://" + Host + "/home.php",
            "Accept-Encoding": "gzip, deflate",
        }
    };
    //console.log(options.url)
    return new Promise(resolve => {
        $.get(options, (err, resp, data) => {
            try {
                if (err) {
                    $.logErr(err)
                } else {
                    if (data) {
                        //console.log(data)
                        var reresultmatch = /showDialog\(\'(.+?)\'/
                        var result = data.match(reresultmatch)[1]
                        console.log(result)
                        if (result.indexOf("签名出错") != -1) {
                            signsuc=false
                            return
                        }
                        ismessage = true
                        message += "用户" + $.index +': ' + username + ' ' + result + '\n'                                                                       
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


function gethost() {
    const options = {
        url: `http://fuliba2023-1256179406.file.myqcloud.com/`,
        headers: {
            "Host": "fuliba2023-1256179406.file.myqcloud.com",
            "Accept": "*/*",
            "Connection": "keep-alive",
            //"Cookie": cookie,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9",
            //"Referer": "https://www.wnflb99.com/home.php",
            "Accept-Encoding": "gzip, deflate, br",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
    };
    //console.log(options.url)
    return new Promise(resolve => {
        $.get(options, (err, resp, data) => {
            try {
                if (err) {
                    $.logErr(err)
                } else {
                    if (data) {
                       //console.log(data)    
                       var rehost = /福利吧最新地址\s+\<a href\=\"https\:\/\/(.+?)\"/
                       Host = data.match(rehost)[1]
                                                                                      
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
// prettier-ignore

function Env(t, e) { "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0); class s { constructor(t) { this.env = t } send(t, e = "GET") { t = "string" == typeof t ? { url: t } : t; let s = this.get; return "POST" === e && (s = this.post), new Promise((e, i) => { s.call(this, t, (t, s, r) => { t ? i(t) : e(s) }) }) } get(t) { return this.send.call(this.env, t) } post(t) { return this.send.call(this.env, t, "POST") } } return new class { constructor(t, e) { this.name = t, this.http = new s(this), this.data = null, this.dataFile = "box.dat", this.logs = [], this.isMute = !1, this.isNeedRewrite = !1, this.logSeparator = "\n", this.startTime = (new Date).getTime(), Object.assign(this, e), this.log("", `🔔${this.name}, 开始!`) } isNode() { return "undefined" != typeof module && !!module.exports } isQuanX() { return "undefined" != typeof $task } isSurge() { return "undefined" != typeof $httpClient && "undefined" == typeof $loon } isLoon() { return "undefined" != typeof $loon } toObj(t, e = null) { try { return JSON.parse(t) } catch { return e } } toStr(t, e = null) { try { return JSON.stringify(t) } catch { return e } } getjson(t, e) { let s = e; const i = this.getdata(t); if (i) try { s = JSON.parse(this.getdata(t)) } catch { } return s } setjson(t, e) { try { return this.setdata(JSON.stringify(t), e) } catch { return !1 } } getScript(t) { return new Promise(e => { this.get({ url: t }, (t, s, i) => e(i)) }) } runScript(t, e) { return new Promise(s => { let i = this.getdata("@chavy_boxjs_userCfgs.httpapi"); i = i ? i.replace(/\n/g, "").trim() : i; let r = this.getdata("@chavy_boxjs_userCfgs.httpapi_timeout"); r = r ? 1 * r : 20, r = e && e.timeout ? e.timeout : r; const [o, h] = i.split("@"), n = { url: `http://${h}/v1/scripting/evaluate`, body: { script_text: t, mock_type: "cron", timeout: r }, headers: { "X-Key": o, Accept: "*/*" } }; this.post(n, (t, e, i) => s(i)) }).catch(t => this.logErr(t)) } loaddata() { if (!this.isNode()) return {}; { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e); if (!s && !i) return {}; { const i = s ? t : e; try { return JSON.parse(this.fs.readFileSync(i)) } catch (t) { return {} } } } } writedata() { if (this.isNode()) { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e), r = JSON.stringify(this.data); s ? this.fs.writeFileSync(t, r) : i ? this.fs.writeFileSync(e, r) : this.fs.writeFileSync(t, r) } } lodash_get(t, e, s) { const i = e.replace(/\[(\d+)\]/g, ".$1").split("."); let r = t; for (const t of i) if (r = Object(r)[t], void 0 === r) return s; return r } lodash_set(t, e, s) { return Object(t) !== t ? t : (Array.isArray(e) || (e = e.toString().match(/[^.[\]]+/g) || []), e.slice(0, -1).reduce((t, s, i) => Object(t[s]) === t[s] ? t[s] : t[s] = Math.abs(e[i + 1]) >> 0 == +e[i + 1] ? [] : {}, t)[e[e.length - 1]] = s, t) } getdata(t) { let e = this.getval(t); if (/^@/.test(t)) { const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t), r = s ? this.getval(s) : ""; if (r) try { const t = JSON.parse(r); e = t ? this.lodash_get(t, i, "") : e } catch (t) { e = "" } } return e } setdata(t, e) { let s = !1; if (/^@/.test(e)) { const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e), o = this.getval(i), h = i ? "null" === o ? null : o || "{}" : "{}"; try { const e = JSON.parse(h); this.lodash_set(e, r, t), s = this.setval(JSON.stringify(e), i) } catch (e) { const o = {}; this.lodash_set(o, r, t), s = this.setval(JSON.stringify(o), i) } } else s = this.setval(t, e); return s } getval(t) { return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null } setval(t, e) { return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null } initGotEnv(t) { this.got = this.got ? this.got : require("got"), this.cktough = this.cktough ? this.cktough : require("tough-cookie"), this.ckjar = this.ckjar ? this.ckjar : new this.cktough.CookieJar, t && (t.headers = t.headers ? t.headers : {}, void 0 === t.headers.Cookie && void 0 === t.cookieJar && (t.cookieJar = this.ckjar)) } get(t, e = (() => { })) { t.headers && (delete t.headers["Content-Type"], delete t.headers["Content-Length"]), this.isSurge() || this.isLoon() ? (this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.get(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) })) : this.isQuanX() ? (this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t))) : this.isNode() && (this.initGotEnv(t), this.got(t).on("redirect", (t, e) => { try { if (t.headers["set-cookie"]) { const s = t.headers["set-cookie"].map(this.cktough.Cookie.parse).toString(); s && this.ckjar.setCookieSync(s, null), e.cookieJar = this.ckjar } } catch (t) { this.logErr(t) } }).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) })) } post(t, e = (() => { })) { if (t.body && t.headers && !t.headers["Content-Type"] && (t.headers["Content-Type"] = "application/x-www-form-urlencoded"), t.headers && delete t.headers["Content-Length"], this.isSurge() || this.isLoon()) this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.post(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) }); else if (this.isQuanX()) t.method = "POST", this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t)); else if (this.isNode()) { this.initGotEnv(t); const { url: s, ...i } = t; this.got.post(s, i).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) }) } } time(t, e = null) { const s = e ? new Date(e) : new Date; let i = { "M+": s.getMonth() + 1, "d+": s.getDate(), "H+": s.getHours(), "m+": s.getMinutes(), "s+": s.getSeconds(), "q+": Math.floor((s.getMonth() + 3) / 3), S: s.getMilliseconds() }; /(y+)/.test(t) && (t = t.replace(RegExp.$1, (s.getFullYear() + "").substr(4 - RegExp.$1.length))); for (let e in i) new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? i[e] : ("00" + i[e]).substr(("" + i[e]).length))); return t } msg(e = t, s = "", i = "", r) { const o = t => { if (!t) return t; if ("string" == typeof t) return this.isLoon() ? t : this.isQuanX() ? { "open-url": t } : this.isSurge() ? { url: t } : void 0; if ("object" == typeof t) { if (this.isLoon()) { let e = t.openUrl || t.url || t["open-url"], s = t.mediaUrl || t["media-url"]; return { openUrl: e, mediaUrl: s } } if (this.isQuanX()) { let e = t["open-url"] || t.url || t.openUrl, s = t["media-url"] || t.mediaUrl; return { "open-url": e, "media-url": s } } if (this.isSurge()) { let e = t.url || t.openUrl || t["open-url"]; return { url: e } } } }; if (this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r))), !this.isMuteLog) { let t = ["", "==============📣系统通知📣=============="]; t.push(e), s && t.push(s), i && t.push(i), console.log(t.join("\n")), this.logs = this.logs.concat(t) } } log(...t) { t.length > 0 && (this.logs = [...this.logs, ...t]), console.log(t.join(this.logSeparator)) } logErr(t, e) { const s = !this.isSurge() && !this.isQuanX() && !this.isLoon(); s ? this.log("", `❗️${this.name}, 错误!`, t.stack) : this.log("", `❗️${this.name}, 错误!`, t) } wait(t) { return new Promise(e => setTimeout(e, t)) } done(t = {}) { const e = (new Date).getTime(), s = (e - this.startTime) / 1e3; this.log("", `🔔${this.name}, 结束! 🕛 ${s} 秒`), this.log(), (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(t) } }(t, e) }
