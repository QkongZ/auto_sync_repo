# scripts-repo
## 复刻各个🐉 🦿📖整合到一起

### GitHub工作流 workflows.yml 文件拉取变量

#### 2.11旧版本版本🐉拉库命令(按实际更改) 多个关键词用"|"分割 ~ 2.13之后新版🐉复制拉库链接可一键导入或手动按需填写
    ql repo https://github.com/作者名/仓库名.git "白名单关键词" "黑名单关键词" "依赖文件关键词" "拉库分支名称"

#### 示例 拉本仓库 mian分支 ~ (①白名单词一般可不设置②黑名单可以填写不能用或过期文件③依赖文件④分支名称)
    ql repo https://github.com/QkongZ/scripts-repo.git "identical|ql_log_scan" "README|workflows" "" "mian"
