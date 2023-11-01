/*
https://github.com/mrabit/aliyundriveDailyCheck/blob/master/autoSignin.js
cron "0 9 * * *" autoSignin.js, tag=阿里云盘签到
refreshToken	阿里云盘 refresh_token, 添加多个可支持多账户签到
CLIENT_ID	可选项, 用于青龙面板 API 更新 refreshToken 字段
CLIENT_SECRET	可选项, 用于青龙面板 API 更新 refreshToken 字段
QL_PATH	可选项, 青龙面板path
*/

const axios = require('axios')
const {
    initInstance,
    getEnv,
    updateCkEnv
} = require('./qlApi.js')
const notify = require('./sendNotify')

const updateAccesssTokenURL = 'https://auth.aliyundrive.com/v2/account/token'
const signinURL = 'https://member.aliyundrive.com/v1/activity/sign_in_list?_rx-s=mobile'
const rewardURL = 'https://member.aliyundrive.com/v1/activity/sign_in_reward?_rx-s=mobile'

// 使用 refresh_token 更新 access_token
function updateAccesssToken(queryBody, remarks) {
    const errorMessage = [remarks, '更新 access_token 失败']
    return axios(updateAccesssTokenURL, {
            method: 'POST',
            data: queryBody,
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(d => d.data)
        .then(d => {
            const {
                code,
                message,
                nick_name,
                refresh_token,
                access_token
            } = d
            if (code) {
                if (
                    code === 'RefreshTokenExpired' ||
                    code === 'InvalidParameter.RefreshToken'
                )
                    errorMessage.push('refresh_token 已过期或无效')
                else errorMessage.push(message)
                return Promise.reject(errorMessage.join(', '))
            }
            return {
                nick_name,
                refresh_token,
                access_token
            }
        })
        .catch(e => {
            errorMessage.push(e.message)
            return Promise.reject(errorMessage.join(', '))
        })
}

function today_is_last() {
    // 创建一个Date对象
    var today = new Date();

    // 获取当前日期和月份
    var currentDate = today.getDate();
    var currentMonth = today.getMonth() + 1; // 月份是从0开始的，所以要加1

    // 获取本月最后一天的日期
    var lastDayOfMonth = new Date(today.getFullYear(), currentMonth, 0).getDate();

    // 判断是否是本月最后一天
    if (currentDate === lastDayOfMonth) {
        console.log("今天是本月最后一天");
        return true 
    } else {
        console.log("今天不是本月最后一天");
        return false
    }
}
//签到列表
function sign_in(access_token, remarks) {
    const sendMessage = [remarks]
    return axios(signinURL, {
            method: 'POST',
            data: {
                isReward: false
            },
            headers: {
                Authorization: access_token,
                'Content-Type': 'application/json'
            }
        })
        .then(d => d.data)
        .then(async json => {
            if (!json.success) {
                sendMessage.push('签到失败', json.message)
                return Promise.reject(sendMessage.join('\n'))
            }

            sendMessage.push('签到成功')

            const {
                signInLogs,
                signInCount
            } = json.result
            const currentSignInfo = signInLogs[signInCount - 1] // 当天签到信息

            sendMessage.push(`本月累计签到 ${signInCount} 天`)

            // 未领取奖励列表
            const rewards = signInLogs.filter(
                v => v.status === 'normal' && !v.isReward
            )
            //console.log(rewards)
            if (rewards.length) {
                var toady_is = today_is_last()
                for await (reward of rewards) {
                    
                    if (reward.type == 'svip8t' && !toady_is) {
                        console.log('SVIP,需要时自行领取')
                        sendMessage.push('SVIP,需要时自行领取')
                        continue
                    }
                    if (reward.type == 'svipVideo' && !toady_is) {
                        console.log('影音播放特权,需要时自行领取')
                        sendMessage.push('影音播放特权,需要时自行领取')
                        continue
                    }
                    console.log(reward)
                    const signInDay = reward.day
                    try {
                        const rewardInfo = await getReward(access_token, signInDay)
                        sendMessage.push(
                            `第${signInDay}天奖励领取成功: 获得${rewardInfo.name || ''}${rewardInfo.description || ''}`
                        )
                    } catch (e) {
                        sendMessage.push(`第${signInDay}天奖励领取失败:`, e)
                    }
                }
            } else if (currentSignInfo.isReward) {
                sendMessage.push(
                    `今日签到获得${currentSignInfo.reward.name || ''}${currentSignInfo.reward.description || ''}`
                )
            }

            return sendMessage.join('\n')
        })
        .catch(e => {
            sendMessage.push('签到失败')
            sendMessage.push(e.message)
            return Promise.reject(sendMessage.join('\n'))
        })
}

// 领取奖励
function getReward(access_token, signInDay) {
    return axios(rewardURL, {
            method: 'POST',
            data: {
                signInDay
            },
            headers: {
                authorization: access_token,
                'Content-Type': 'application/json'
            }
        })
        .then(d => d.data)
        .then(json => {
            if (!json.success) {
                return Promise.reject(json.message)
            }

            return json.result
        })
}

// 获取环境变量
async function getRefreshToken() {
    let instance = null
    try {
        instance = await initInstance()
    } catch (e) {}
    
    let refreshToken = process.env.refreshToken || []
    
    try {
        if (instance) refreshToken = await getEnv(instance, 'refreshToken')
    } catch (e) {}
    
    //console.log(refreshToken)
    let refreshTokenArray = []

    if (Array.isArray(refreshToken)) refreshTokenArray = refreshToken
    else if (refreshToken.indexOf('&') > -1)
        refreshTokenArray = refreshToken.split('&')
    else if (refreshToken.indexOf('\n') > -1)
        refreshTokenArray = refreshToken.split('\n')
    else refreshTokenArray = [refreshToken]

    if (!refreshTokenArray.length) {
        console.log('未获取到refreshToken, 程序终止')
        process.exit(1)
    }

    return {
        instance,
        refreshTokenArray
    }
}

!(async() => {
    const {
        instance,
        refreshTokenArray
    } = await getRefreshToken()

    const message = []
    let index = 1
    for await (refreshToken of refreshTokenArray) {
        let remarks = refreshToken.remarks || `账号${index}`
        const queryBody = {
            grant_type: 'refresh_token',
            refresh_token: refreshToken.value || refreshToken
        }

        try {
            const {
                nick_name,
                refresh_token,
                access_token
            } = await updateAccesssToken(queryBody, remarks)

            if (nick_name && nick_name !== remarks)
                remarks = `${nick_name}(${remarks})`

            // 更新环境变量
            if (instance) {
                let params = {
                    name: refreshToken.name,
                    value: refresh_token,
                    remarks: refreshToken.remarks || nick_name // 优先存储原有备注信息
                }
                // 新版青龙api
                if (refreshToken.id) {
                    params.id = refreshToken.id
                }
                // 旧版青龙api
                if (refreshToken._id) {
                    params._id = refreshToken._id
                }
                await updateCkEnv(instance, params)
            }

            const sendMessage = await sign_in(access_token, remarks)
            console.log(sendMessage)
            console.log('\n')
            message.push(sendMessage)
        } catch (e) {
            console.log(e)
            console.log('\n')
            message.push(e)
        }
        index++
    }
    await notify.sendNotify(`阿里云盘签到`, message.join('\n\n'))
})()
