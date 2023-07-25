# 慈善家

全量自用工具本，使用方法详解脚本内注释，反馈脚本问题请在社区内联系作者，随缘更新~

接口验参全部调用函数模块并且开源，脚本内容全部加密无任何调用个人接口，我很忙没空研究如何偷你ck，喜欢🐕叫的别用谢谢

> 官方线报频道：[来薅线报通知](https://t.me/LH_notify)  
> 官方解析BOT：[宇宙无敌万能解析机器人](https://t.me/ParseJDBot)（加入 [Arcadia 官方频道](https://t.me/ArcadiaPanel) 和社区群组后才可以使用）

Tips：仓库内全部都是工具本没有常规本不需要默认设置定时任务，部分情况下运行脚本会报错例如不设置环境变量、变量无效等

## 拉库

- ### Arcadia 面板（推荐使用）

    ```bash
    arcadia repo 慈善家 https://gitlab.com/SuperManito/cishanjia.git main --whiteList '^jd_'
    ```
    详见官方文档：https://arcadia.cool

- ### 青龙面板

    ```bash
    ql repo https://gitlab.com/SuperManito/cishanjia.git "jd_|jdCookie" "" "^jd[^_]|USER|function|sendNotify" "main"
    ```

## 功能配置

- ### 自定义签名API

  ```bash
  export JD_SIGN_API="" # 杂货铺格式
  ```

- ### 自动登记实物收货地址

  ```bash
  export WX_ADDRESS="" # 变量格式：收件人@手机号@省份@城市@区县@详细地址@6位行政区划代码@邮编，需按照顺序依次填写，多个用管道符分开（6位行政区划代码自己查地图，也可用身份证号前六位）
  export WX_ADDRESS_BLOCK="" # 多个关键词用@分开
  ```

- ### 辅助工具脚本

  敬请期待

__未经授权请勿搬运，脚本仅供用于学习交流，切勿用于商业用途！__
