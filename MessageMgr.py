import json
import time

Prefix = "!!msg"
help_msg = '''------MCDR Message Manager插件------
§a命令帮助如下:§r
§6!!msg§r 显示这条信息
§6!!msg send <目标玩家> <信息>§r 向一位离线玩家留言信息，将在他上线时显示
--------------------------------'''
PluginName = "MessageMgr"
DataPath = "plugins/" + PluginName + '/'
data = []


def format_time():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def load_data():
    global data
    try:
        with open(DataPath + "message.json") as file:
            data = json.load(file, encoding='utf8')
    except:
        return

def add_data(time, sender, target, message):
    global data

    load_data()
    
    length = len(data)
    data.append({"time" : time , "sender" : sender ,
                 "target" : target , "message" : message})
    
    try:
        with open(DataPath + "message.json", "w") as file:
            json.dump(data, file)
    except:
        return

def on_player_joined(server, player):
    load_data()
    for i in range(0, len(data)):
        if data[i]["target"] == player:

            server.tell(player, format_time())
            
            server.tell(player, "§a" + data[i]["sender"] + "§r于§a" +
                        data[i]["time"] + "§r给你留言：" + "§6" + data[i]["message"] + "§r")


def on_info(server, info):
    content = info.content
    splited_content = content.split()
    
    if splited_content[0] != Prefix:
        return
    
    if len(splited_content) == 1: 
        server.reply(info, help_msg)
        return
    
    if splited_content[1] == "send":
        if len(splited_content) < 4:
            server.reply(info, "§c格式错误§r，请输入§6!!msg§r查看帮助信息")
            return

        time = format_time()
        sender = info.player
        target = splited_content[2]
        message = splited_content[3]
        
        if sender == target:
            server.reply(info, "§c不能给自己留言！§r")
            return

        add_data(time, sender, target, message)
        server.reply(info, "§a成功向§6" + target + "§a留言：§r" + message)
