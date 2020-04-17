import json
import time
import stext as st

Prefix = "!!msg"
help_msg = '''------MCDR Message Manager插件------
§a命令帮助如下:§r
§6!!msg§r 显示这条信息
§6!!msg send <目标玩家> <信息>§r 向一位离线玩家留言信息，将在他上线时显示
§6!!msg list§r 显示由自己发送的所有留言
§6!!msg del <信息>§r 删除留言
--------------------------------'''
PluginName = "MessageMgr"
DataPath = "plugins/" + PluginName + '/'
data = []

def on_load(server, old_module):
    load_data()

def format_time():
	return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

def load_data():
    global data
    try:
        with open(DataPath + "message.json") as file:
            data = json.load(file, encoding='utf8')
    except:
        return

def save_data():
    global data
    try:
        with open(DataPath + "message.json", "w") as file:
            json.dump(data, file)
    except:
        return

def add_data(time, sender, target, message):
    global data

    load_data()
    
    length = len(data)
    data.append({"time" : time , "sender" : sender ,
                 "target" : target , "message" : message})
    
    save_data()

def delete_data(message):
    global data
    load_data()
    print(data)
    length = len(data)
    print(length)
    for i in range(0, length):
        print(i, data[i]["message"], message)
        if data[i]["message"] == message:
            del data[i]
            save_data()
            return 1
    return 0

def on_player_joined(server, player):
    load_data()
    for i in range(0, len(data)):
        if data[i]["target"] == player:

            server.tell(player, format_time())
            
            server.tell(player, "§6" + data[i]["sender"] + "§r于§a" +
                        data[i]["time"] + "§r给你留言 : " + "§6" + data[i]["message"] + "§r")


def on_info(server, info):
    content = info.content
    splited_content = content.split()
    player = info.player
    
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
        sender = player
        target = splited_content[2]
        message = splited_content[3]
        
        if sender == target:
            server.reply(info, "§c不能给自己留言！§r")
            return

        add_data(time, sender, target, message)
        server.reply(info, "§a成功向§6" + target + "§a留言 : §r" + message)
    if splited_content[1] == "list":
        global data
        load_data()
        flag = 1
        for i in range(0, len(data)):
            if data[i]["sender"] == player:
                time = data[i]["time"]
                target = data[i]["target"]
                message = data[i]["message"]
                if flag :
                    flag = 0
                    
                delete = st.SText("[x]", color=st.SColor.red)
                delete.styles = [st.SStyle.bold]
                delete.hover_text = st.SText("点击删除§6" + data[i]["message"])
                command = "!!msg del " + data[i]["message"]
                delete.set_click_command(command)
                st.show_to_player(server, player, delete)
                
                server.reply(info, "§a" + time + " §6To " +
                             target + "§r : " + message)
        if flag:
            server.reply(info, "§c你没有任何留言！")
    if splited_content[1] == "del":
        if len(splited_content) < 3:
            server.reply(info, "§c格式错误§r，请输入§6!!msg§r查看帮助信息")
            return
        if delete_data(splited_content[2]):
            server.reply(info, "§a成功删除§r : " + splited_content[2])
        else:
            server.reply(info, "§c未找到指定留言")
