<h1 align="center">
  和东哥做兄弟
  <br>
  Author: chiupam
</h1>

## 目录
- [目录](#目录)
- [版权](#版权)
- [声明](#声明)
- [特别感谢](#特别感谢)
- [简介](#简介)
- [已有功能](#已有功能)
  - [bot.py功能](#botpy功能)
  - [bot.py可拓展功能](#botpy可拓展功能)
  - [user.py功能](#userpy功能)
- [使用方式](#使用方式)
  - [部署bot.py](#部署botpy)
  - [V4BOT用户部署user.py](#v4bot用户部署userpy)
  - [青龙用户部署user.py](#青龙用户部署userpy)
# 版权
- 未经本人同意，仓库内所有资源文件，禁止任何公众号、自媒体、开发者进行任何形式的转载、发布、搬运。
# 声明
- 这不是一个开源项目，只是把 GitHub 当作一个代码的存储空间，本项目不接受任何开源要求。
- 仅用于学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。
- 本人对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害。
- 间接使用脚本的任何用户，包括但不限于建立VPS或在某些行为违反国家/地区法律或相关法规的情况下进行传播, 本人对于由此引起的任何隐私泄漏或其他后果概不负责。
- 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明、所有权证明，我将在收到认证文件后删除相关脚本。
- 任何以任何方式查看此项目的人或者以直接或间接的方式使用该项目的任何脚本的使用者都应仔细阅读此声明。 本人保留随时更改或补充此免责声明的权利。一旦使用并复制或使用了任何相关脚本，则视为您已接受此免责声明。
- 您必须在下载后的24小时内从计算机或手机中完全删除以上内容。
# 特别感谢
- 脚本的写作参考了 [SuMaiKaDe](https://github.com/SuMaiKaDe) 的 [jddockerbot](https://github.com/SuMaiKaDe/bot) 仓库
- 模块的写作参考了 lxk0301 的 jd_sctipts 仓库
## 简介
随着 v4-bot 启动而启动的自定义机器人，其中大部分功能亦支持青龙用户。
## 已有功能
### bot.py功能
- [x] 发送 `/start` 指令可开启自定义机器人
- [x] 发送 `/restart` 指令可重启机器人
- [x] 发送 `/help` 指令可获取快捷命令
- [x] 发送 `/install` 指令可拓展功能
- [x] 发送 `/uninstall` 指令可卸载功能
- [x] 发送 `/list` 指令列出已有功能
### bot.py可拓展功能
- [x] 发送 `/upbot` 升级机器人
- [x] 发送 `/checkcookie` 检测过期情况
- [x] 发送`/export` 修改环境变量
- [x] 下载 `.js` `.py` `.sh` 的 `raw` 文件
- [x] 添加以 `.git` 结尾的仓库链接可添加仓库（暂不支持青龙用户）
- [x] 发送 `变量名="变量值"` 的格式消息可快捷添加环境变量
### user.py功能
- [x] 监控布道场，关注店铺有礼
- [x] 监控我的脚本频道，自动更新最新的脚本
- [x] 监控组队瓜分ID频道，自动替换环境变量
## 使用方法
### 部署[bot.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/bot.py)
#### 方法一、 在容器中使用命令
```
rm -rf diybot.sh
wget https://ghproxy.com/https://raw.githubusercontent.com/chiupam/JD_Diy/master/config/diybot.sh
bash diybot.sh
```
#### 方法二、 给机器人发消息
```
/cmd rm -rf diybot.sh && wget https://ghproxy.com/https://raw.githubusercontent.com/chiupam/JD_Diy/master/config/diybot.sh && bash diybot.sh
```
### V4BOT用户部署[user.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/user.py)
1. 把文件存储在路径 `/jbot/diy/` 下
2. 进入容器，使用命令 `docker exec -it jd bash`
3. 先手动停止机器人，输入命令：`pm2 stop jbot`
4. 为了避免不必要的麻烦，输入命令：`rm -rf user.session`
5. 手动前台开启机器人，输入命令：`python3 -m jbot`
6. 输入手机号和 `telegram` 验证码进行登录后按 `Ctrl`+`C` 退出前台运行
7. 后台挂起机器人，输入命令 `pm2 start jbot` 
### 青龙用户部署[user.py](https://github.com/chiupam/JD_Diy/blob/main/jbot/user.py)
1. 把文件存储在路径 `/jbot/diy/` 下
2. 进入容器，使用命令 `docker exec -it qinglong bash`
3. 先手动停止机器人，输入命令：`pm2 stop jbot`
4. 为了避免不必要的麻烦，输入命令：`rm -rf user.session`
5. 手动前台开启机器人，输入命令：`python3 -m jbot`
6. 输入手机号和 `telegram` 验证码进行登录后按 `Ctrl`+`C` 退出前台运行
7. 重启机器人，输入命令 `ql bot`
