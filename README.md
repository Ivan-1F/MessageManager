# MessageManager
[English](https://github.com/wyf0762/MessageManager/blob/master/doc/README_en.md)

一个 [MCDReforged](https://github.com/Fallen-Breath/MCDReforged)的留言插件，需要[stext](https://github.com/TISUnion/stext)作为前置。

向一位离线玩家留言信息，并在他下次上线时显示给他。

# 安装

1. 将`MessageMgr.py`和`stext.py`拖入`/plugins`文件夹，并创建`/plugins/MessageMgr/message.json`文件
2. 使用`!!MCDR reload plugin`重载MCDR 

# 使用

- `!!msg`获取帮助信息
- `!!msg send <目标玩家> <信息>`向一位离线玩家留言信息，将在他上线时显示
- `!!msg list`显示由自己发送的所有留言
- `!!msg del <信息>`删除留言

# 注意事项

- 目前留言的消息不能带有空格