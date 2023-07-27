### 注意注意

1.自用，勿拉取（后果自负）

2.本项目仅用于学习使用，请下载后24小时内删除

### 自动填地址

#### 无线类：
`export WX_ADDRESS="" # 变量格式：收件人@手机号@省份@城市@区县@详细地址@6位行政区划代码@邮编，需按照顺序依次填写，多个用管道符分开（6位行政区划代码自己查地图，也可用身份证号前六位）`

`export WX_ADDRESS_BLOCK="" # 多个关键词用@分开  黑名单`

### 拉取(js py ts)青龙 config.sh 文件中修改

ql repo命令拉取脚本时需要拉取的文件后缀，直接写文件后缀名即可

`RepoFileExtensions="js py ts"`

### 神秘代码

`ql repo https://github.com/KingRan/KR.git "jd_|jx_|jdCookie" "activity|backUp" "^jd[^_]|USER|utils|function|sign|sendNotify|ql|JDJR"`

拉库失败或者拉不到更新的解决方案：

`rm -rf /ql/repo/KingRan_KR && ql repo https://github.com/KingRan/KR.git "jd_|jx_|jdCookie" "activity|backUp" "^jd[^_]|USER|utils|function|sendNotify|ql|JDJR"`


