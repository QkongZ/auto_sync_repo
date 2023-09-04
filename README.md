# auto_sync_repo
## 定时复刻各作者仓库青龙脚本代码整合到本仓库目标分支中

### GitHub工作流调用py脚本定时执行config.json中自定义仓库源推送并合并到目标分支中

#### 2.11旧版本版本🐉拉库命令(按实际更改) 多个关键词用"|"分割 ~ 2.13之后新版🐉复制拉库链接可一键导入或手动按需填写
    ql repo https://github.com/作者名/仓库名.git "白名单关键词" "黑名单关键词" "依赖文件关键词" "拉库分支名称"

#### 示例 拉本仓库 main分支 ~ (①白名单词一般可不设置②黑名单可以填写不能用或过期文件③依赖文件④分支名称)
    ql repo https://github.com/QkongZ/scripts-repo.git "identical|ql_log_scan" "README|workflows" "" "mian"
#### 拉取其他分支中的单个文件
    ql raw https://raw.githubusercontent.com/作者名/仓库名/分支名/文件名
#### 示例 拉取本仓库 main分支的workflows.yml文件
    ql raw https://raw.githubusercontent.com/QkongZ/scripts-repo/main/workflows.yml



## 使用说明
```
1、直接fork本项目到你自己的仓库。

2、点击自己的github设置--settings（右上角头像小三角点开下拉菜单就看到了）

3、点击developer setings

4、点击Personal access tokens

5、点击generate new token

6、note随便起个好记的名字，给“repo”和“workflow”打勾

7、拉倒页面最下，点generate token

8、复制得到的token

9、回到fork得到的仓库，点仓库名字下面一行按钮中的“settings”

10、点击secrets---再点击new repository secrets

11、上面填写 PAT 三个字母

12、下面粘贴复制得到的token

13、保存即可

14、点击仓库名字下面一行按钮中的action

15、点击右上角的star，添加一课星星

16、手动运行一次这个页面的各个sync项目。方法是点击一个项目，然后点击run workflow。

17、回到fork到的仓库的首页，编辑readme.md文件，删掉开头的^_^，再保存一次。

18、完事了

19、自动同步我的Autosync项目的方法：


在github安装pull，会自动帮你检测上游仓库，并帮助你更新代码

地址在这: https://github.com/apps/pull

配置后，fork走的仓库也会跟着我的更新而更新代码，然后再自动拉取新增的仓库，属于无限套娃

```
