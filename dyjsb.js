/**
 作者：临渊
 日期：7-1
 软件：抖音极速版
 抓包：进入活动后，抓 api5-normal-c-hl.amemv.com 域名请求体里cookie 或者别的域名也有可能，反正是活动里面的cookie
 变量格式：export dyjsAPP='xxx' 
 Cron： 13,43 8-18,23 * * *

 不支持多账号！不支持多账号！不支持多账号！多账号跑会有错误

 [task_local]
 #抖音极速版
 10,40 8-18 * * * https://raw.githubusercontent.com/LinYuanovo/scripts/main/dyjsb.js, tag=抖音极速版, enabled=true
 [rewrite_local]
 https://api5-normal-c-hl.amemv.com/luckycat/aweme/v1/task url script-request-header https://raw.githubusercontent.com/LinYuanovo/scripts/main/dyjsb.js
 [MITM]
 hostname = api5-normal-c-hl.amemv.com
 */

 const $ = new Env('抖音极速');
 const notify = $.isNode() ? require('./sendNotify') : '';
 const {log} = console;
 const Notify = 2; //0为关闭通知，1为完成任务进行通知，2为23.40之后推送一次余额，默认为2
 const debug = 0; //0为关闭调试，1为打开调试，默认为0
 //////////////////////

 const _0x2695=['test','name','completed','】：未填写变量\x20dyjsAPP','constructor','error','/page?aid=2329&device_platform=android&update_version_code=21040000','score_amount','\x0a\x20【','getdata','excitation_ad_info','ad_id','replace','./sendNotify','\x22}\x22,\x22ad_alias_position\x22:\x22box\x22,\x22timeout\x22:4000}','^([^\x20]+(\x20+[^\x20]+)+)+[^\x20]}','\x0a【领取开宝箱视频奖励】','\x0a【debug】===============\x20这是\x20领取视频奖励\x20请求\x20url\x20===============','，现金余额：','/ql/data/config/config.sh','dyjsAPP','明日再来','wait','已达到上限','info','\x0a【debug】===============\x20这是\x20签到\x20请求\x20url\x20===============','isNode','daily_times','/walk/step_submit?aid=2329&device_platform=android&update_version_code=21040000','【领取开宝箱视频奖励】','v1/task/page','split','stringify','getTimezoneOffset','\x20个账号】=========\x0a','\x0a【debug】===============\x20这是\x20领取签到视频奖励\x20请求\x20url\x20===============','/done/excitation_ad_treasure_box?aid=2329&device_platform=android&update_version_code=21040000','push','match','【领取搜索奖励】','setdata','https://api5-normal-c-hl.amemv.com/luckycat/aweme/v1/task','\x22,\x22amount\x22:\x22888\x22,\x22ad_rit\x22:\x22','QWERTYUIOPASDFGHJKLZXCVBNM1234567890','times_every_day','\x0a【领取视频奖励】今日已达上限','getMinutes','{\x22task_key\x22:\x22','【领取签到视频奖励】','author','/done/search_excitation?aid=2329&device_platform=android&update_version_code=21040000','\x0a【领取签到视频奖励】','\x0a\x0a【debug】===============这是\x20获取签到详情\x20返回data==============','/sign_in/detail?aid=2329&device_platform=android&update_version_code=21040000','\x0a\x0a【debug】===============这是\x20上传步数\x20返回data==============','action_desc','\x0a\x0a【debug】===============这是\x20领取看小说奖励\x20返回data==============','env','步数】','\x0a\x0a【debug】===============这是\x20获取任务列表\x20返回data==============','\x0a============\x20当前版本：','\x0a【debug】===============\x20这是\x20开宝箱\x20请求\x20url\x20===============','\x0a【领取第','round','【获取签到详情】','{\x22step\x22:','\x0a【debug】===============\x20这是\x20领取看小说奖励\x20请求\x20url\x20===============','floor','today_step','\x0a【debug】===============\x20这是\x20获取签到详情\x20请求\x20url\x20===============','\x22}\x22,\x22ad_alias_position\x22:\x22check_in\x22,\x22timeout\x22:4000}','\x0a\x0a【debug】===============这是\x20领取步数奖励\x20返回data==============','today_times','warn','req_id','length','/walk/receive_step_reward?aid=2329&device_platform=android&update_version_code=21040000','\x0a【开宝箱】','toLocaleString','/done/treasure_task?aid=2329&device_platform=android&update_version_code=21040000','1.0.0','trace','logErr','log','err_no','个\x20ck\x20成功:\x20','【领取视频奖励】今日已达上限','\x0a\x0a【debug】===============这是\x20开宝箱\x20返回data==============','origin','readFile','parse','url','【签到】','\x0a【debug】===============\x20这是\x20领取步数奖励\x20请求\x20url\x20===============','return\x20/\x22\x20+\x20this\x20+\x20\x22/','\x20\x20最新版本：','task_key','msg','utf8','\x0a【领取搜索奖励】','reward_amount','\x0a=========\x20开始【第\x20','getTime','，获得：','done_time','\x0a【debug】===============\x20这是\x20获取任务列表\x20请求\x20url\x20===============','\x0a金币余额：','content','{}.constructor(\x22return\x20this\x22)(\x20)',',\x22submit_time\x22:','catch','profit_desc','console','\x0a【debug】===============\x20这是\x20上传步数\x20请求\x20url\x20===============','\x20============','/done/excitation_ad?aid=2329&device_platform=android&update_version_code=21040000','income_data','【debug】\x20这是你的全部账号数组:\x0a\x20','/done/read_novel?aid=2329&device_platform=android&update_version_code=21040000','\x22,\x22ad_inspire\x22:\x22{\x22score_amount\x22:\x22888\x22,\x22amount\x22:\x22\x22,\x22req_id\x22:\x22','status_extra','post','err_tips','api5-normal-c-hl.amemv.com','headers','amount1','get','table','data','forEach','amount','hasOwnProperty','indexOf','return\x20(function()\x20','【开宝箱】','sendNotify','，退出','\x20获取\x20ck\x20成功:\x20','exception','task_list','\x20,不用请自行关闭重写!','【领取视频奖励】','random','application/json','【领取看小说奖励】','【上传','次看小说奖励】','\x0a\x0a=============================================\x20\x20\x20\x20\x0a脚本执行\x20-\x20北京时间(UTC+8)：','debug','\x0a\x20【debug】\x20这是你第\x20','搜索赚金币','compile','key','【获取任务列表】失败，原因是：','undefined','\x0a【debug】===============\x20这是\x20领取开宝箱视频奖励\x20请求\x20url\x20===============','【领取步数奖励】'];(function(_0x20f3e6,_0x269534){const _0x4ca941=function(_0x51df64){while(--_0x51df64){_0x20f3e6['push'](_0x20f3e6['shift']());}};const _0x43f389=function(){const _0x582073={'data':{'key':'cookie','value':'timeout'},'setCookie':function(_0x3686c4,_0x4fe0c7,_0x8fad2c,_0x28f616){_0x28f616=_0x28f616||{};let _0x40db3f=_0x4fe0c7+'='+_0x8fad2c;let _0x334285=0x0;for(let _0x2db013=0x0,_0x55c2c7=_0x3686c4['length'];_0x2db013<_0x55c2c7;_0x2db013++){const _0x3174ca=_0x3686c4[_0x2db013];_0x40db3f+=';\x20'+_0x3174ca;const _0x37432c=_0x3686c4[_0x3174ca];_0x3686c4['push'](_0x37432c);_0x55c2c7=_0x3686c4['length'];if(_0x37432c!==!![]){_0x40db3f+='='+_0x37432c;}}_0x28f616['cookie']=_0x40db3f;},'removeCookie':function(){return'dev';},'getCookie':function(_0x1c9201,_0x30b557){_0x1c9201=_0x1c9201||function(_0x293c3c){return _0x293c3c;};const _0x553e0b=_0x1c9201(new RegExp('(?:^|;\x20)'+_0x30b557['replace'](/([.$?*|{}()[]\/+^])/g,'$1')+'=([^;]*)'));const _0x261507=function(_0x4c6d9e,_0x1d0387){_0x4c6d9e(++_0x1d0387);};_0x261507(_0x4ca941,_0x269534);return _0x553e0b?decodeURIComponent(_0x553e0b[0x1]):undefined;}};const _0x59bf59=function(){const _0x2bd6e4=new RegExp('\x5cw+\x20*\x5c(\x5c)\x20*{\x5cw+\x20*[\x27|\x22].+[\x27|\x22];?\x20*}');return _0x2bd6e4['test'](_0x582073['removeCookie']['toString']());};_0x582073['updateCookie']=_0x59bf59;let _0x578a1a='';const _0x4c3aaa=_0x582073['updateCookie']();if(!_0x4c3aaa){_0x582073['setCookie'](['*'],'counter',0x1);}else if(_0x4c3aaa){_0x578a1a=_0x582073['getCookie'](null,'counter');}else{_0x582073['removeCookie']();}};_0x43f389();}(_0x2695,0xee));const _0x4ca9=function(_0x20f3e6,_0x269534){_0x20f3e6=_0x20f3e6-0x0;let _0x4ca941=_0x2695[_0x20f3e6];return _0x4ca941;};const _0x3686c4=function(){let _0x3349bc=!![];return function(_0x369806,_0x3acbd0){const _0x46b94d=_0x3349bc?function(){if(_0x3acbd0){const _0x353cae=_0x3acbd0['apply'](_0x369806,arguments);_0x3acbd0=null;return _0x353cae;}}:function(){};_0x3349bc=![];return _0x46b94d;};}();const _0x4c3aaa=_0x3686c4(this,function(){const _0x329ab8=function(){const _0x49c8fb=_0x329ab8[_0x4ca9('0x50')](_0x4ca9('0xd'))()[_0x4ca9('0x46')](_0x4ca9('0x5b'));return!_0x49c8fb[_0x4ca9('0x4c')](_0x4c3aaa);};return _0x329ab8();});_0x4c3aaa();const _0x582073=function(){let _0x514249=!![];return function(_0xc91cd8,_0x473374){const _0x27a050=_0x514249?function(){if(_0x473374){const _0x171103=_0x473374['apply'](_0xc91cd8,arguments);_0x473374=null;return _0x171103;}}:function(){};_0x514249=![];return _0x27a050;};}();const _0x51df64=_0x582073(this,function(){const _0xbc461c=function(){};const _0x40d302=function(){let _0x3ba627;try{_0x3ba627=Function(_0x4ca9('0x34')+_0x4ca9('0x1b')+');')();}catch(_0x3eab0a){_0x3ba627=window;}return _0x3ba627;};const _0x587d2e=_0x40d302();if(!_0x587d2e[_0x4ca9('0x1f')]){_0x587d2e[_0x4ca9('0x1f')]=function(_0xa52f47){const _0x15e77c={};_0x15e77c[_0x4ca9('0x2')]=_0xa52f47;_0x15e77c[_0x4ca9('0x95')]=_0xa52f47;_0x15e77c[_0x4ca9('0x43')]=_0xa52f47;_0x15e77c['info']=_0xa52f47;_0x15e77c[_0x4ca9('0x51')]=_0xa52f47;_0x15e77c[_0x4ca9('0x39')]=_0xa52f47;_0x15e77c['table']=_0xa52f47;_0x15e77c[_0x4ca9('0x0')]=_0xa52f47;return _0x15e77c;}(_0xbc461c);}else{_0x587d2e[_0x4ca9('0x1f')][_0x4ca9('0x2')]=_0xbc461c;_0x587d2e['console']['warn']=_0xbc461c;_0x587d2e['console']['debug']=_0xbc461c;_0x587d2e[_0x4ca9('0x1f')][_0x4ca9('0x64')]=_0xbc461c;_0x587d2e[_0x4ca9('0x1f')][_0x4ca9('0x51')]=_0xbc461c;_0x587d2e['console'][_0x4ca9('0x39')]=_0xbc461c;_0x587d2e['console'][_0x4ca9('0x2e')]=_0xbc461c;_0x587d2e[_0x4ca9('0x1f')][_0x4ca9('0x0')]=_0xbc461c;}});_0x51df64();let scriptVersion=_0x4ca9('0x9c');let scriptVersionLatest='';let dyjsAPP=($[_0x4ca9('0x66')]()?process[_0x4ca9('0x85')]['dyjsAPP']:$[_0x4ca9('0x55')](_0x4ca9('0x60')))||'';let dyjsAPPArr=[];let dyjs='';let data='';let msg1='';let msg2='';let activityUrl=_0x4ca9('0x75');let task_key='';let ad_rit='';let req_id='';let loginBack=0x0;let excitation_adBack=0x0;let search_excitationBack=0x0;let searchTimes=0x0;let read_novelBack=0x0;let read_novelNum=0x0;let signinBack=0x0;let signinVideoBack=0x0;let boxVideoBack=0x0;let submitStepBack=0x0;let coin=0x0;let cash=0x0;!(async()=>{if(typeof $request!==_0x4ca9('0x49')){await GetRewrite();}else{if(!await Envs())return;else{log(_0x4ca9('0x42')+new Date(new Date()[_0x4ca9('0x15')]()+new Date()[_0x4ca9('0x6d')]()*0x3c*0x3e8+0x8*0x3c*0x3c*0x3e8)[_0x4ca9('0x9a')]()+'\x20\x0a=============================================\x0a');await poem();await getVersion();log(_0x4ca9('0x88')+scriptVersion+_0x4ca9('0xe')+scriptVersionLatest+_0x4ca9('0x21'));log('\x0a===================\x20共找到\x20'+dyjsAPPArr[_0x4ca9('0x97')]+'\x20个账号\x20===================');if(debug){log(_0x4ca9('0x24')+dyjsAPPArr);}for(let _0x373a68=0x0;_0x373a68<dyjsAPPArr[_0x4ca9('0x97')];_0x373a68++){let _0x2accdb=_0x373a68+0x1;log(_0x4ca9('0x14')+_0x2accdb+_0x4ca9('0x6e'));dyjs=dyjsAPPArr[_0x373a68];if(debug){log(_0x4ca9('0x44')+_0x2accdb+'\x20账号信息:\x0a\x20'+data+'\x0a');}await submitStep();await $[_0x4ca9('0x62')](randomInt(0xbb8,0x1770));if(submitStepBack){await getStepReward();await $[_0x4ca9('0x62')](randomInt(0xbb8,0x1770));}await getTaskList();if(loginBack){if(signinBack){await $['wait'](randomInt(0xbb8,0x1770));await getSigninInfo();await $[_0x4ca9('0x62')](randomInt(0xbb8,0x1770));await getSigninVideoReward();await $[_0x4ca9('0x62')](randomInt(0xbb8,0x1770));}if(excitation_adBack){await getWatchVideoReward();await $[_0x4ca9('0x62')](randomInt(0xbb8,0x1770));}if(search_excitationBack){await getSearchReward();await $[_0x4ca9('0x62')](randomInt(0xbb8,0x1770));while(searchTimes!=0x0){await getSearchReward();await $[_0x4ca9('0x62')](randomInt(0xbb8,0x1770));}}if(read_novelBack){await getReadNovelReward();await $['wait'](randomInt(0xbb8,0x1770));while(read_novelNum){await getReadNovelReward();await $[_0x4ca9('0x62')](randomInt(0xbb8,0x1770));}}}log('金币余额：'+coin+_0x4ca9('0x5e')+cash);if(msg1!=''){msg1+=_0x4ca9('0x19')+coin+_0x4ca9('0x5e')+cash;}msg2+='\x0a金币余额：'+coin+_0x4ca9('0x5e')+cash;}if(Notify==0x1){await SendMsg(msg1);}else if(Notify==0x2&&new Date()['getHours']()>=0x17&&new Date()[_0x4ca9('0x7a')]()>=0x28){await SendMsg(msg2);}}}})()[_0x4ca9('0x1d')](_0x589861=>log(_0x589861))['finally'](()=>$['done']());function getTaskList(_0x2e32a5=0x3*0x3e8){return new Promise(_0xb4efd1=>{let _0x2adf63={'url':activityUrl+_0x4ca9('0x52'),'headers':{'Host':'api5-normal-c-hl.amemv.com','cookie':''+dyjs}};if(debug){log(_0x4ca9('0x18'));log(JSON[_0x4ca9('0x6c')](_0x2adf63));}$['get'](_0x2adf63,async(_0x5b02a7,_0x10bb35,_0x3e0226)=>{try{if(debug){log(_0x4ca9('0x87'));log(_0x3e0226);}let _0x2e590a=JSON[_0x4ca9('0x9')](_0x3e0226);if(_0x2e590a[_0x4ca9('0x3')]==0x0){coin=_0x2e590a[_0x4ca9('0x2f')][_0x4ca9('0x23')][_0x4ca9('0x2c')];cash=_0x2e590a[_0x4ca9('0x2f')][_0x4ca9('0x23')]['amount2'];cash=cash/0x64;loginBack=0x1;for(let _0x16db84 in _0x2e590a[_0x4ca9('0x2f')][_0x4ca9('0x3a')]){if(_0x2e590a['data']['task_list'][_0x16db84][_0x4ca9('0x1e')][_0x4ca9('0x33')]('签到')>-0x1){let _0x3e8f99=JSON[_0x4ca9('0x9')](_0x2e590a['data'][_0x4ca9('0x3a')][_0x16db84][_0x4ca9('0x4e')]);if(!_0x3e8f99){signinBack=0x1;}else signinBack=0x0;}if(_0x2e590a['data'][_0x4ca9('0x3a')][_0x16db84][_0x4ca9('0x4d')][_0x4ca9('0x33')]('看广告赚金币')>-0x1){let _0x16a12e=JSON[_0x4ca9('0x9')](_0x2e590a[_0x4ca9('0x2f')]['task_list'][_0x16db84][_0x4ca9('0x27')]);if(!_0x16a12e[_0x4ca9('0x4e')]){excitation_adBack=0x1;task_key=_0x2e590a[_0x4ca9('0x2f')]['task_list'][_0x16db84][_0x4ca9('0x47')];ad_rit=_0x16a12e[_0x4ca9('0x57')];req_id=_0x16a12e['req_id'];}else excitation_adBack=0x0;if(_0x2e590a[_0x4ca9('0x2f')][_0x4ca9('0x3a')][_0x16db84][_0x4ca9('0x83')][_0x4ca9('0x33')](_0x4ca9('0x61'))>-0x1){excitation_adBack=0x0;log(_0x4ca9('0x5'));}}if(_0x2e590a[_0x4ca9('0x2f')][_0x4ca9('0x3a')][_0x16db84][_0x4ca9('0x4d')]['indexOf'](_0x4ca9('0x45'))>-0x1){let _0x18619f=JSON[_0x4ca9('0x9')](_0x2e590a[_0x4ca9('0x2f')][_0x4ca9('0x3a')][_0x16db84][_0x4ca9('0x27')]);if(_0x18619f[_0x4ca9('0x94')]!=_0x18619f[_0x4ca9('0x78')]){search_excitationBack=0x1;}else search_excitationBack=0x0;}if(_0x2e590a['data']['task_list'][_0x16db84][_0x4ca9('0x4d')]['indexOf']('看小说赚金币')>-0x1){let _0x100067=JSON[_0x4ca9('0x9')](_0x2e590a['data'][_0x4ca9('0x3a')][_0x16db84][_0x4ca9('0x4e')]);if(!_0x100067){read_novelBack=0x1;}else read_novelBack=0x0;}}}else{log(_0x4ca9('0x48')+_0x2e590a[_0x4ca9('0x29')]+_0x4ca9('0x37'));}}catch(_0x3dd8f5){log(_0x3dd8f5);}finally{_0xb4efd1();}},_0x2e32a5);});}function getWatchVideoReward(_0x43e365=0x3*0x3e8){return new Promise(_0x5994fd=>{let _0x2e431d={'url':activityUrl+_0x4ca9('0x22'),'headers':{'Host':_0x4ca9('0x2a'),'Cookie':''+dyjs},'body':_0x4ca9('0x7b')+task_key+_0x4ca9('0x76')+ad_rit+'\x22,\x22ad_inspire\x22:\x22{\x22score_amount\x22:\x22888\x5c\x22,\x22req_id\x22:\x22'+req_id+'\x22}\x22,\x22ad_alias_position\x22:\x22task\x22,\x22timeout\x22:4000}'};if(debug){log(_0x4ca9('0x5d'));log(JSON[_0x4ca9('0x6c')](_0x2e431d));}$[_0x4ca9('0x28')](_0x2e431d,async(_0x472afe,_0x44b914,_0x125231)=>{try{if(debug){log('\x0a\x0a【debug】===============这是\x20领取视频奖励\x20返回data==============');log(_0x125231);}let _0x137c90=JSON['parse'](_0x125231);if(_0x137c90[_0x4ca9('0x3')]===0x0&&_0x137c90[_0x4ca9('0x2f')]['hasOwnProperty'](_0x4ca9('0x31'))){log(_0x4ca9('0x3c')+_0x137c90[_0x4ca9('0x29')]+'，获得：'+_0x137c90[_0x4ca9('0x2f')][_0x4ca9('0x31')]+'金币');msg1+='\x0a【领取视频奖励】'+_0x137c90[_0x4ca9('0x29')]+_0x4ca9('0x16')+_0x137c90['data'][_0x4ca9('0x31')]+'金币';}else if(_0x137c90['err_no']===0x2716&&_0x137c90[_0x4ca9('0x29')][_0x4ca9('0x33')](_0x4ca9('0x63'))>-0x1){log(_0x4ca9('0x5'));msg1+=_0x4ca9('0x79');}else log(_0x4ca9('0x3c')+_0x137c90['err_tips']);}catch(_0x49f1f2){log(_0x49f1f2);}finally{_0x5994fd();}},_0x43e365);});}function getSearchReward(_0x48dfb3=0x3*0x3e8){return new Promise(_0x6ad6f9=>{let _0x2b51a1={'url':activityUrl+_0x4ca9('0x7e'),'headers':{'Host':_0x4ca9('0x2a'),'Cookie':''+dyjs},'body':''};if(debug){log('\x0a【debug】===============\x20这是\x20领取搜索奖励\x20请求\x20url\x20===============');log(JSON[_0x4ca9('0x6c')](_0x2b51a1));}$[_0x4ca9('0x28')](_0x2b51a1,async(_0x30b479,_0x52968c,_0xa66b20)=>{try{if(debug){log('\x0a\x0a【debug】===============这是\x20领取搜索奖励\x20返回data==============');log(_0xa66b20);}let _0x36aee9=JSON[_0x4ca9('0x9')](_0xa66b20);if(_0x36aee9[_0x4ca9('0x3')]===0x0&&_0x36aee9[_0x4ca9('0x2f')]['hasOwnProperty'](_0x4ca9('0x31'))){searchTimes=_0x36aee9[_0x4ca9('0x2f')][_0x4ca9('0x67')];log('【领取搜索奖励】'+_0x36aee9[_0x4ca9('0x29')]+_0x4ca9('0x16')+_0x36aee9[_0x4ca9('0x2f')][_0x4ca9('0x31')]+'金币');msg1+=_0x4ca9('0x12')+_0x36aee9[_0x4ca9('0x29')]+'，获得：'+_0x36aee9['data'][_0x4ca9('0x31')]+'金币';}else log(_0x4ca9('0x73')+_0x36aee9[_0x4ca9('0x29')]);}catch(_0xa9d0a4){log(_0xa9d0a4);}finally{_0x6ad6f9();}},_0x48dfb3);});}function getReadNovelReward(_0x92a0f3=0x3*0x3e8){return new Promise(_0xda99c3=>{let _0x444f45={'url':activityUrl+_0x4ca9('0x25'),'headers':{'Host':_0x4ca9('0x2a'),'Cookie':''+dyjs},'body':''};if(debug){log(_0x4ca9('0x8e'));log(JSON[_0x4ca9('0x6c')](_0x444f45));}$[_0x4ca9('0x28')](_0x444f45,async(_0x397f6b,_0x3dd653,_0x434db8)=>{try{if(debug){log(_0x4ca9('0x84'));log(_0x434db8);}let _0x4600c9=JSON[_0x4ca9('0x9')](_0x434db8);if(_0x4600c9[_0x4ca9('0x3')]===0x0&&_0x4600c9['data'][_0x4ca9('0x32')]('score_amount')){if(_0x4600c9['data'][_0x4ca9('0x17')]!=_0x4600c9[_0x4ca9('0x2f')]['done_limit']){read_novelNum=0x1;}else read_novelNum=0x0;log('【领取第'+_0x4600c9[_0x4ca9('0x2f')][_0x4ca9('0x17')]+'次看小说奖励】'+_0x4600c9[_0x4ca9('0x29')]+'，获得：'+_0x4600c9['data']['score_amount']+'金币');msg1+=_0x4ca9('0x8a')+_0x4600c9['data'][_0x4ca9('0x17')]+_0x4ca9('0x41')+_0x4600c9[_0x4ca9('0x29')]+_0x4ca9('0x16')+_0x4600c9[_0x4ca9('0x2f')][_0x4ca9('0x53')]+'金币';}else log(_0x4ca9('0x3f')+_0x4600c9[_0x4ca9('0x29')]);}catch(_0xc33038){log(_0xc33038);}finally{_0xda99c3();}},_0x92a0f3);});}function submitStep(_0x5bac1a=0x3*0x3e8){return new Promise(_0x6350a0=>{let _0x15594a={'url':activityUrl+_0x4ca9('0x68'),'headers':{'Accept':'*/*','Host':_0x4ca9('0x2a'),'cookie':''+dyjs,'Content-Type':_0x4ca9('0x3e')},'body':_0x4ca9('0x8d')+randomInt(0x2ee0,0x32c8)+_0x4ca9('0x1c')+(timestampS()-0x14)+'}'};if(debug){log(_0x4ca9('0x20'));log(JSON[_0x4ca9('0x6c')](_0x15594a));}$[_0x4ca9('0x28')](_0x15594a,async(_0x3d3f5e,_0x8774bb,_0x470902)=>{try{if(debug){log(_0x4ca9('0x82'));log(_0x470902);}let _0x31a9aa=JSON[_0x4ca9('0x9')](_0x470902);if(_0x31a9aa['err_no']===0x0&&_0x31a9aa[_0x4ca9('0x2f')][_0x4ca9('0x32')](_0x4ca9('0x90'))){submitStepBack=0x1;log(_0x4ca9('0x40')+_0x31a9aa['data'][_0x4ca9('0x90')]+_0x4ca9('0x86')+_0x31a9aa[_0x4ca9('0x29')]);}else{submitStepBack=0x0;log('【上传步数】'+_0x31a9aa['err_tips']);}}catch(_0x10a9ec){log(_0x10a9ec);}finally{_0x6350a0();}},_0x5bac1a);});}function getStepReward(_0x318cde=0x3*0x3e8){return new Promise(_0x4d0cbb=>{let _0x2c9c06={'url':activityUrl+_0x4ca9('0x98'),'headers':{'Host':_0x4ca9('0x2a'),'Cookie':''+dyjs},'body':''};if(debug){log(_0x4ca9('0xc'));log(JSON[_0x4ca9('0x6c')](_0x2c9c06));}$['post'](_0x2c9c06,async(_0x4ebf65,_0x51088d,_0x4384f4)=>{try{if(debug){log(_0x4ca9('0x93'));log(_0x4384f4);}let _0x3540cc=JSON[_0x4ca9('0x9')](_0x4384f4);if(_0x3540cc[_0x4ca9('0x3')]===0x0&&_0x3540cc[_0x4ca9('0x2f')][_0x4ca9('0x32')](_0x4ca9('0x13'))){log(_0x4ca9('0x4b')+_0x3540cc['err_tips']+_0x4ca9('0x16')+_0x3540cc[_0x4ca9('0x2f')]['reward_amount']+'金币');}else log('【领取步数奖励】'+_0x3540cc['err_tips']);}catch(_0x22974e){log(_0x22974e);}finally{_0x4d0cbb();}},_0x318cde);});}function signin(_0x861c8e=0x3*0x3e8){return new Promise(_0x380684=>{let _0x128656={'url':activityUrl+'/done/sign_in?aid=2329&device_platform=android&update_version_code=21040000','headers':{'Host':_0x4ca9('0x2a'),'Cookie':''+dyjs},'body':'{}'};if(debug){log(_0x4ca9('0x65'));log(JSON[_0x4ca9('0x6c')](_0x128656));}$[_0x4ca9('0x28')](_0x128656,async(_0x12d85e,_0x1110e4,_0x3e2f12)=>{try{if(debug){log('\x0a\x0a【debug】===============这是\x20签到\x20返回data==============');log(_0x3e2f12);}let _0x39fc2f=JSON[_0x4ca9('0x9')](_0x3e2f12);if(_0x39fc2f[_0x4ca9('0x3')]===0x0&&_0x39fc2f[_0x4ca9('0x2f')][_0x4ca9('0x32')]('amount')){log(_0x4ca9('0xb')+_0x39fc2f[_0x4ca9('0x29')]+_0x4ca9('0x16')+_0x39fc2f['data']['amount']+'金币');msg1+='\x0a【签到】'+_0x39fc2f[_0x4ca9('0x29')]+_0x4ca9('0x16')+_0x39fc2f[_0x4ca9('0x2f')][_0x4ca9('0x31')]+'金币';}else log(_0x4ca9('0xb')+_0x39fc2f['err_tips']);}catch(_0x59f3e5){log(_0x59f3e5);}finally{_0x380684();}},_0x861c8e);});}function getSigninInfo(_0x4b0a4d=0x3*0x3e8){return new Promise(_0x4d6afb=>{let _0x5f1c0f={'url':activityUrl+_0x4ca9('0x81'),'headers':{'Host':_0x4ca9('0x2a'),'Cookie':''+dyjs}};if(debug){log(_0x4ca9('0x91'));log(JSON['stringify'](_0x5f1c0f));}$[_0x4ca9('0x2d')](_0x5f1c0f,async(_0x1340c7,_0x2fdce5,_0x3b0a0d)=>{try{if(debug){log(_0x4ca9('0x80'));log(_0x3b0a0d);}let _0x1b3c40=JSON[_0x4ca9('0x9')](_0x3b0a0d);if(_0x1b3c40[_0x4ca9('0x3')]===0x0&&_0x1b3c40[_0x4ca9('0x2f')][_0x4ca9('0x32')](_0x4ca9('0x56'))){signinVideoBack=0x1;task_key=_0x1b3c40['data'][_0x4ca9('0x56')][_0x4ca9('0xf')];ad_rit=_0x1b3c40['data'][_0x4ca9('0x56')][_0x4ca9('0x57')];req_id=_0x1b3c40[_0x4ca9('0x2f')]['excitation_ad_info']['req_id'];}else{signinVideoBack=0x0;log(_0x4ca9('0x8c')+_0x1b3c40[_0x4ca9('0x29')]);}}catch(_0x4ad42c){log(_0x4ad42c);}finally{_0x4d6afb();}},_0x4b0a4d);});}function getSigninVideoReward(_0x196175=0x3*0x3e8){return new Promise(_0x44af89=>{let _0xc16d31={'url':activityUrl+'/done/excitation_ad_signin?aid=2329&device_platform=android&update_version_code=21040000','headers':{'Host':_0x4ca9('0x2a'),'Cookie':''+dyjs},'body':_0x4ca9('0x7b')+task_key+_0x4ca9('0x76')+ad_rit+'\x22,\x22ad_inspire\x22:\x22{\x22score_amount\x22:\x22888\x22,\x22amount\x22:\x22\x22,\x22req_id\x22:\x22'+req_id+_0x4ca9('0x92')};if(debug){log(_0x4ca9('0x6f'));log(JSON['stringify'](_0xc16d31));}$[_0x4ca9('0x28')](_0xc16d31,async(_0x211e29,_0x59086f,_0x179d67)=>{try{if(debug){log('\x0a\x0a【debug】===============这是\x20领取签到视频奖励\x20返回data==============');log(_0x179d67);}let _0x59fca8=JSON['parse'](_0x179d67);if(_0x59fca8[_0x4ca9('0x3')]===0x0&&_0x59fca8[_0x4ca9('0x2f')][_0x4ca9('0x32')](_0x4ca9('0x31'))){log(_0x4ca9('0x7c')+_0x59fca8[_0x4ca9('0x29')]+_0x4ca9('0x16')+_0x59fca8[_0x4ca9('0x2f')][_0x4ca9('0x31')]+'金币');msg1+=_0x4ca9('0x7f')+_0x59fca8['err_tips']+_0x4ca9('0x16')+_0x59fca8[_0x4ca9('0x2f')][_0x4ca9('0x31')]+'金币';}else log(_0x4ca9('0x7c')+_0x59fca8[_0x4ca9('0x29')]);}catch(_0x5758e5){log(_0x5758e5);}finally{_0x44af89();}},_0x196175);});}function openBox(_0x5be1d6=0x3*0x3e8){return new Promise(_0x84d2a6=>{let _0x3830c5={'url':activityUrl+_0x4ca9('0x9b'),'headers':{'Host':'api5-normal-c-hl.amemv.com','Cookie':''+dyjs},'body':'{}'};if(debug){log(_0x4ca9('0x89'));log(JSON[_0x4ca9('0x6c')](_0x3830c5));}$['post'](_0x3830c5,async(_0x1e79cc,_0xc1cd0d,_0x158943)=>{try{if(debug){log(_0x4ca9('0x6'));log(_0x158943);}let _0x4b9c8e=JSON['parse'](_0x158943);if(_0x4b9c8e[_0x4ca9('0x3')]===0x0&&_0x4b9c8e[_0x4ca9('0x2f')][_0x4ca9('0x32')]('amount')){boxVideoBack=0x1;task_key=_0x4b9c8e[_0x4ca9('0x2f')][_0x4ca9('0x56')]['task_key'];ad_rit=_0x4b9c8e['data']['excitation_ad_info'][_0x4ca9('0x57')];req_id=_0x4b9c8e[_0x4ca9('0x2f')]['excitation_ad_info'][_0x4ca9('0x96')];log(_0x4ca9('0x35')+_0x4b9c8e[_0x4ca9('0x29')]+_0x4ca9('0x16')+_0x4b9c8e['data']['amount']+'金币');msg1+=_0x4ca9('0x99')+_0x4b9c8e[_0x4ca9('0x29')]+'，获得：'+_0x4b9c8e[_0x4ca9('0x2f')]['amount']+'金币';}else{log('【开宝箱】'+_0x4b9c8e['err_tips']);boxVideoBack=0x0;}}catch(_0x3a5780){log(_0x3a5780);}finally{_0x84d2a6();}},_0x5be1d6);});}function getBoxVideoReward(_0x381f3a=0x3*0x3e8){return new Promise(_0x3f3e45=>{let _0x110fab={'url':activityUrl+_0x4ca9('0x70'),'headers':{'Host':'api5-normal-c-hl.amemv.com','Cookie':''+dyjs},'body':_0x4ca9('0x7b')+task_key+_0x4ca9('0x76')+ad_rit+_0x4ca9('0x26')+req_id+_0x4ca9('0x5a')};if(debug){log(_0x4ca9('0x4a'));log(JSON[_0x4ca9('0x6c')](_0x110fab));}$['post'](_0x110fab,async(_0x55da65,_0x3e0e62,_0x4e44ea)=>{try{if(debug){log('\x0a\x0a【debug】===============这是\x20领取开宝箱视频奖励\x20返回data==============');log(_0x4e44ea);}let _0x333c94=JSON[_0x4ca9('0x9')](_0x4e44ea);if(_0x333c94[_0x4ca9('0x3')]===0x0&&_0x333c94['data'][_0x4ca9('0x32')](_0x4ca9('0x31'))){log('【领取开宝箱视频奖励】'+_0x333c94['err_tips']+'，获得：'+_0x333c94['data'][_0x4ca9('0x31')]+'金币');msg1+=_0x4ca9('0x5c')+_0x333c94[_0x4ca9('0x29')]+_0x4ca9('0x16')+_0x333c94[_0x4ca9('0x2f')][_0x4ca9('0x31')]+'金币';}else log(_0x4ca9('0x69')+_0x333c94[_0x4ca9('0x29')]);}catch(_0x35416f){log(_0x35416f);}finally{_0x3f3e45();}},_0x381f3a);});}async function GetRewrite(){if($request[_0x4ca9('0xa')][_0x4ca9('0x33')](_0x4ca9('0x6a'))>-0x1){const _0x3ab661=$request[_0x4ca9('0x2b')]['cookie'];if(dyjsAPP){if(dyjsAPP['indexOf'](_0x3ab661)==-0x1){dyjsAPP=dyjsAPP+'@'+_0x3ab661;$[_0x4ca9('0x74')](dyjsAPP,_0x4ca9('0x60'));let _0x125c2a=dyjsAPP['split']('@');$[_0x4ca9('0x10')]('【'+$[_0x4ca9('0x4d')]+'】'+('\x20获取第'+_0x125c2a[_0x4ca9('0x97')]+_0x4ca9('0x4')+_0x3ab661+_0x4ca9('0x3b')));}}else{$[_0x4ca9('0x74')](_0x3ab661,_0x4ca9('0x60'));$[_0x4ca9('0x10')]('【'+$[_0x4ca9('0x4d')]+'】'+(_0x4ca9('0x38')+_0x3ab661+_0x4ca9('0x3b')));}}}async function Envs(){if(dyjsAPP){if(dyjsAPP[_0x4ca9('0x33')]('@')!=-0x1){dyjsAPP['split']('@')[_0x4ca9('0x30')](_0x401d30=>{dyjsAPPArr[_0x4ca9('0x71')](_0x401d30);});}else if(dyjsAPP[_0x4ca9('0x33')]('\x0a')!=-0x1){dyjsAPP[_0x4ca9('0x6b')]('\x0a')['forEach'](_0x23d301=>{dyjsAPPArr[_0x4ca9('0x71')](_0x23d301);});}else{dyjsAPPArr['push'](dyjsAPP);}}else{log(_0x4ca9('0x54')+$[_0x4ca9('0x4d')]+_0x4ca9('0x4f'));return;}return!![];}async function SendMsg(_0x5b8baa){if(!_0x5b8baa)return;if(Notify>0x0){if($[_0x4ca9('0x66')]()){var _0x57faa5=require(_0x4ca9('0x59'));await _0x57faa5[_0x4ca9('0x36')]($[_0x4ca9('0x4d')],_0x5b8baa);}else{$[_0x4ca9('0x10')](_0x5b8baa);}}else{log(_0x5b8baa);}}function randomString(_0x656d97){_0x656d97=_0x656d97||0x20;var _0x9d152=_0x4ca9('0x77'),_0x1a8c16=_0x9d152[_0x4ca9('0x97')],_0xa092f8='';for(i=0x0;i<_0x656d97;i++)_0xa092f8+=_0x9d152['charAt'](Math[_0x4ca9('0x8f')](Math[_0x4ca9('0x3d')]()*_0x1a8c16));return _0xa092f8;}function randomInt(_0x131862,_0x304d90){return Math[_0x4ca9('0x8b')](Math[_0x4ca9('0x3d')]()*(_0x304d90-_0x131862)+_0x131862);}function timestampMs(){return new Date()[_0x4ca9('0x15')]();}function timestampS(){return Date[_0x4ca9('0x9')](new Date())/0x3e8;}function poem(_0x557db5=0x3*0x3e8){return new Promise(_0x10df8c=>{let _0x54ce26={'url':'https://v1.jinrishici.com/all.json'};$[_0x4ca9('0x2d')](_0x54ce26,async(_0x548c57,_0xcfb5c3,_0x23e03f)=>{try{_0x23e03f=JSON[_0x4ca9('0x9')](_0x23e03f);log(_0x23e03f[_0x4ca9('0x1a')]+'\x20\x20\x0a————《'+_0x23e03f[_0x4ca9('0x7')]+'》'+_0x23e03f[_0x4ca9('0x7d')]);}catch(_0x4f44bd){log(_0x4f44bd,_0xcfb5c3);}finally{_0x10df8c();}},_0x557db5);});}function modify(){fs[_0x4ca9('0x8')](_0x4ca9('0x5f'),_0x4ca9('0x11'),function(_0x5869c3,_0x397713){if(_0x5869c3){return log('读取文件失败！'+_0x5869c3);}else{var _0x1fd282=_0x397713[_0x4ca9('0x58')](/regular/g,string);fs['writeFile']('/ql/data/config/config.sh',_0x1fd282,_0x4ca9('0x11'),function(_0x379821){if(_0x379821){return log(_0x379821);}});}});}function getVersion(_0x1d3d2b=0x3*0x3e8){return new Promise(_0x297f62=>{let _0x1a79d2={'url':'https://raw.gh.fakev.cn/LinYuanovo/scripts/main/dyjsb.js'};$['get'](_0x1a79d2,async(_0x5f407c,_0x1b2188,_0x42e4ab)=>{try{scriptVersionLatest=_0x42e4ab[_0x4ca9('0x72')](/scriptVersion = "([\d\.]+)"/)[0x1];}catch(_0x778679){$[_0x4ca9('0x1')](_0x778679,_0x1b2188);}finally{_0x297f62();}},_0x1d3d2b);});}

 function Env(t, e) { "undefined" != typeof process && JSON.stringify(process.env).indexOf("GITHUB") > -1 && process.exit(0); class s { constructor(t) { this.env = t } send(t, e = "GET") { t = "string" == typeof t ? { url: t } : t; let s = this.get; return "POST" === e && (s = this.post), new Promise((e, i) => { s.call(this, t, (t, s, r) => { t ? i(t) : e(s) }) }) } get(t) { return this.send.call(this.env, t) } post(t) { return this.send.call(this.env, t, "POST") } } return new class { constructor(t, e) { this.name = t, this.http = new s(this), this.data = null, this.dataFile = "box.dat", this.logs = [], this.isMute = !1, this.isNeedRewrite = !1, this.logSeparator = "\n", this.startTime = (new Date).getTime(), Object.assign(this, e), this.log("", `🔔${this.name}, 开始!`) } isNode() { return "undefined" != typeof module && !!module.exports } isQuanX() { return "undefined" != typeof $task } isSurge() { return "undefined" != typeof $httpClient && "undefined" == typeof $loon } isLoon() { return "undefined" != typeof $loon } toObj(t, e = null) { try { return JSON.parse(t) } catch { return e } } toStr(t, e = null) { try { return JSON.stringify(t) } catch { return e } } getjson(t, e) { let s = e; const i = this.getdata(t); if (i) try { s = JSON.parse(this.getdata(t)) } catch { } return s } setjson(t, e) { try { return this.setdata(JSON.stringify(t), e) } catch { return !1 } } getScript(t) { return new Promise(e => { this.get({ url: t }, (t, s, i) => e(i)) }) } runScript(t, e) { return new Promise(s => { let i = this.getdata("@chavy_boxjs_userCfgs.httpapi"); i = i ? i.replace(/\n/g, "").trim() : i; let r = this.getdata("@chavy_boxjs_userCfgs.httpapi_timeout"); r = r ? 1 * r : 20, r = e && e.timeout ? e.timeout : r; const [o, h] = i.split("@"), n = { url: `http://${h}/v1/scripting/evaluate`, body: { script_text: t, mock_type: "cron", timeout: r }, headers: { "X-Key": o, Accept: "*/*" } }; this.post(n, (t, e, i) => s(i)) }).catch(t => this.logErr(t)) } loaddata() { if (!this.isNode()) return {}; { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e); if (!s && !i) return {}; { const i = s ? t : e; try { return JSON.parse(this.fs.readFileSync(i)) } catch (t) { return {} } } } } writedata() { if (this.isNode()) { this.fs = this.fs ? this.fs : require("fs"), this.path = this.path ? this.path : require("path"); const t = this.path.resolve(this.dataFile), e = this.path.resolve(process.cwd(), this.dataFile), s = this.fs.existsSync(t), i = !s && this.fs.existsSync(e), r = JSON.stringify(this.data); s ? this.fs.writeFileSync(t, r) : i ? this.fs.writeFileSync(e, r) : this.fs.writeFileSync(t, r) } } lodash_get(t, e, s) { const i = e.replace(/\[(\d+)\]/g, ".$1").split("."); let r = t; for (const t of i) if (r = Object(r)[t], void 0 === r) return s; return r } lodash_set(t, e, s) { return Object(t) !== t ? t : (Array.isArray(e) || (e = e.toString().match(/[^.[\]]+/g) || []), e.slice(0, -1).reduce((t, s, i) => Object(t[s]) === t[s] ? t[s] : t[s] = Math.abs(e[i + 1]) >> 0 == +e[i + 1] ? [] : {}, t)[e[e.length - 1]] = s, t) } getdata(t) { let e = this.getval(t); if (/^@/.test(t)) { const [, s, i] = /^@(.*?)\.(.*?)$/.exec(t), r = s ? this.getval(s) : ""; if (r) try { const t = JSON.parse(r); e = t ? this.lodash_get(t, i, "") : e } catch (t) { e = "" } } return e } setdata(t, e) { let s = !1; if (/^@/.test(e)) { const [, i, r] = /^@(.*?)\.(.*?)$/.exec(e), o = this.getval(i), h = i ? "null" === o ? null : o || "{}" : "{}"; try { const e = JSON.parse(h); this.lodash_set(e, r, t), s = this.setval(JSON.stringify(e), i) } catch (e) { const o = {}; this.lodash_set(o, r, t), s = this.setval(JSON.stringify(o), i) } } else s = this.setval(t, e); return s } getval(t) { return this.isSurge() || this.isLoon() ? $persistentStore.read(t) : this.isQuanX() ? $prefs.valueForKey(t) : this.isNode() ? (this.data = this.loaddata(), this.data[t]) : this.data && this.data[t] || null } setval(t, e) { return this.isSurge() || this.isLoon() ? $persistentStore.write(t, e) : this.isQuanX() ? $prefs.setValueForKey(t, e) : this.isNode() ? (this.data = this.loaddata(), this.data[e] = t, this.writedata(), !0) : this.data && this.data[e] || null } initGotEnv(t) { this.got = this.got ? this.got : require("got"), this.cktough = this.cktough ? this.cktough : require("tough-cookie"), this.ckjar = this.ckjar ? this.ckjar : new this.cktough.CookieJar, t && (t.headers = t.headers ? t.headers : {}, void 0 === t.headers.Cookie && void 0 === t.cookieJar && (t.cookieJar = this.ckjar)) } get(t, e = (() => { })) { t.headers && (delete t.headers["Content-Type"], delete t.headers["Content-Length"]), this.isSurge() || this.isLoon() ? (this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.get(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) })) : this.isQuanX() ? (this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t))) : this.isNode() && (this.initGotEnv(t), this.got(t).on("redirect", (t, e) => { try { if (t.headers["set-cookie"]) { const s = t.headers["set-cookie"].map(this.cktough.Cookie.parse).toString(); s && this.ckjar.setCookieSync(s, null), e.cookieJar = this.ckjar } } catch (t) { this.logErr(t) } }).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) })) } post(t, e = (() => { })) { if (t.body && t.headers && !t.headers["Content-Type"] && (t.headers["Content-Type"] = "application/x-www-form-urlencoded"), t.headers && delete t.headers["Content-Length"], this.isSurge() || this.isLoon()) this.isSurge() && this.isNeedRewrite && (t.headers = t.headers || {}, Object.assign(t.headers, { "X-Surge-Skip-Scripting": !1 })), $httpClient.post(t, (t, s, i) => { !t && s && (s.body = i, s.statusCode = s.status), e(t, s, i) }); else if (this.isQuanX()) t.method = "POST", this.isNeedRewrite && (t.opts = t.opts || {}, Object.assign(t.opts, { hints: !1 })), $task.fetch(t).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => e(t)); else if (this.isNode()) { this.initGotEnv(t); const { url: s, ...i } = t; this.got.post(s, i).then(t => { const { statusCode: s, statusCode: i, headers: r, body: o } = t; e(null, { status: s, statusCode: i, headers: r, body: o }, o) }, t => { const { message: s, response: i } = t; e(s, i, i && i.body) }) } } time(t, e = null) { const s = e ? new Date(e) : new Date; let i = { "M+": s.getMonth() + 1, "d+": s.getDate(), "H+": s.getHours(), "m+": s.getMinutes(), "s+": s.getSeconds(), "q+": Math.floor((s.getMonth() + 3) / 3), S: s.getMilliseconds() }; /(y+)/.test(t) && (t = t.replace(RegExp.$1, (s.getFullYear() + "").substr(4 - RegExp.$1.length))); for (let e in i) new RegExp("(" + e + ")").test(t) && (t = t.replace(RegExp.$1, 1 == RegExp.$1.length ? i[e] : ("00" + i[e]).substr(("" + i[e]).length))); return t } msg(e = t, s = "", i = "", r) { const o = t => { if (!t) return t; if ("string" == typeof t) return this.isLoon() ? t : this.isQuanX() ? { "open-url": t } : this.isSurge() ? { url: t } : void 0; if ("object" == typeof t) { if (this.isLoon()) { let e = t.openUrl || t.url || t["open-url"], s = t.mediaUrl || t["media-url"]; return { openUrl: e, mediaUrl: s } } if (this.isQuanX()) { let e = t["open-url"] || t.url || t.openUrl, s = t["media-url"] || t.mediaUrl; return { "open-url": e, "media-url": s } } if (this.isSurge()) { let e = t.url || t.openUrl || t["open-url"]; return { url: e } } } }; if (this.isMute || (this.isSurge() || this.isLoon() ? $notification.post(e, s, i, o(r)) : this.isQuanX() && $notify(e, s, i, o(r))), !this.isMuteLog) { let t = ["", "==============📣系统通知📣=============="]; t.push(e), s && t.push(s), i && t.push(i), console.log(t.join("\n")), this.logs = this.logs.concat(t) } } log(...t) { t.length > 0 && (this.logs = [...this.logs, ...t]), console.log(t.join(this.logSeparator)) } logErr(t, e) { const s = !this.isSurge() && !this.isQuanX() && !this.isLoon(); s ? this.log("", `❗️${this.name}, 错误!`, t.stack) : this.log("", `❗️${this.name}, 错误!`, t) } wait(t) { return new Promise(e => setTimeout(e, t)) } done(t = {}) { const e = (new Date).getTime(), s = (e - this.startTime) / 1e3; this.log("", `🔔${this.name}, 结束! 🕛 ${s} 秒`), this.log(), (this.isSurge() || this.isQuanX() || this.isLoon()) && $done(t) } }(t, e) }
