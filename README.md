# goodnight_bot
## 一个在特定群组内，不止可以道晚安的bot

Telegram bot：@goodnight_prpr_bot

注意：请授予机器人admin的`delete message`权限，否则自动删除命令功能将无法使用！
当然，如果担心隐私问题，不赋予权限也是可以用的！

### 使用方法
搭建api环境
> pip3 install pytelegrambotapi

下载源代码
> git clone https://github.com/xhn16729/goodnight_bot.git

运行
> python3 main.py

### 进程守护
推荐使用systemd进行进程守护，详询Google

### bot的bug
1. 由于服务器性能和线路原因，bot的反应速度超级慢……暂无解决方法
2. ~~回复一个没有username的用户的话，机器人无法应答~~
3. ~~回复机器人自己，会自己给自己打招呼~~
4. ~~用户回复自己，会自己给自己打招呼~~
5. 其他的bug请tg告知 @LittleBear0729

### bot的feature
1. 可以按照时间自动改变问好内容
2. 可以自动删掉command（当然，这需要bot的管理员权限，这也意味着隐私问题。所以，不赋予权限也是可以用的！）
3. 可以给你的好朋友加上昵称
3. ~~bug也可以变成feature不是吗~~
