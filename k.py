# -*- coding: utf-8 -*-
from Linephu.linepy import *
import codecs, json
from humanfriendly import format_timespan
import time, threading
import datetime
ts = time.time()
botStart = time.time()
cl = LINE()
cl.log(cl.authToken)

oepoll = OEPoll(cl)
settingsOpen = codecs.open("temp.json","r","utf-8")
settings = json.load(settingsOpen)
lineSettings = cl.getSettings()
clProfile = cl.getProfile()
clMID = cl.profile.mid
admin = [clMID, "uec56bb5a959005526b8b96e6907014e8",'uf5cea65de5804929ce44c168cb26addd','u9ca695057d9f61bf34b54a6b1343f39c','ua66ce0e2921ecd068760eda436c56746']
bots = [cl]
print("登入成功\n全体登入時間: {} s\n重複登入的次數 {}".format(time.time()-ts, len(bots)))
klist = []
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True     
    except Exception as error:
        logError(error)
        return False
def logError(text):
    cl.log("[ 錯誤 ] " + str(text))
    time = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def Kick(n, to, mid):
    while 1:
        bots[n].kickoutFromGroup(to, mid)
        break
def bot(op):
    try:
        if op.type == 0:
            return
        if op.type == 13: cl.acceptGroupInvitation(op.param1)
        if op.type == 17:
            if op.param2 not in admin:
                if settings["joinkick"] == True:
                    threading.Thread(target=cl.kickoutFromGroup, args=(op.param1,[op.param2],)).start()
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            elif msg.toType == 2:
                to = receiver
            if text.lower() is None:
                return
            if msg.contentType == 0:
                if text is None:
                    return
            if sender in settings["Owner"] or sender in admin:
                if op.message.text.lower().startswith(".t ") and "MENTION" in op.message.contentMetadata:
                    if settings["kick"] == True:
                        key = eval(op.message.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        n = 0
                        for x in key["MENTIONEES"]:
                            if n == len(bots):
                                n = 0
                            threading.Thread(target=Kick, args=(n, op.message.to, [x["M"]],)).start()
                            n += 1
                        return
                    else:
                        cl.sendMessage(op.message.to, "你的專武已關閉,機器不會踢人")
                elif op.message.text.lower().startswith(".k ") and "MENTION" in op.message.contentMetadata:
                    if settings["kick"] == True:
                        key = eval(op.message.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        n = 0
                        for x in key["MENTIONEES"]:
                            if n == len(bots):
                                n = 0
                            threading.Thread(target=Kick, args=(n, op.message.to, [x["M"]],)).start()
                            n += 1
                        return
                    else:
                        cl.sendMessage(op.message.to, "你的專武已關閉,機器不會踢人")
                elif "sp" == op.message.text.lower():
                    t1 = time.time()
                    threading.Thread(target=cl.sendMessage, args=(op.message.to, "速度測試",)).start()
                    t2 = time.time() - t1
                    time.sleep(1)
                    return cl.sendMessage(op.message.to, "速度偵測為\n%s 秒" %t2)
                elif op.message.text.lower().startswith("加入 ") and "MENTION" in op.message.contentMetadata:
                    key = eval(op.message.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    for x in key["MENTIONEES"]:
                        klist.append(x["M"])
                    return cl.sendMessage(op.message.to, "完成")
                elif "列表踢" == op.message.text.lower():
                    if settings["kick"] == True:
                        n = 0
                        for x in klist:
                            if n == len(bots):
                                n = 0
                            threading.Thread(target=Kick, args=(n, op.message.to, [x],)).start()
                            n += 1
                        return
                    else:
                        cl.sendMessage(op.message.to, "你的專武已關閉,機器不會踢人")
                elif op.message.text.lower().startswith("刪除 "):
                    input1 = op.message.text.replace("刪除 ","")
                    sep = input1.split(" ")
                    for x in sep:
                        try:
                            kill = klist[(int(x)-1)]
                            klist.remove(kill)
                            cl.sendMessage(op.message.to, "完成")
                        except:
                            cl.sendMessage(op.message.to, "無效範圍刪除失敗")
                elif op.message.text.lower().startswith("op ") and "MENTION" in op.message.contentMetadata:
                    key = eval(op.message.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            try:
                                settings["Owner"][target] = True
                                backupData()
                                cl.sendMessage(op.message.to, "已加入權限")
                            except:
                                pass
                elif op.message.text.lower().startswith("del ") and "MENTION" in op.message.contentMetadata:
                    key = eval(op.message.contentMetadata["MENTION"])
                    key["MENTIONEES"][0]["M"]
                    targets = []
                    for x in key["MENTIONEES"]:
                        targets.append(x["M"])
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            try:
                                del settings["Owner"][target]
                                backupData()
                                cl.sendMessage(op.message.to, "已刪除權限")
                            except:
                                pass
                elif "權限列表" == op.message.text:
                    if settings["Owner"] == {}:
                        cl.sendMessage(to=op.message.to, text="列表沒人")
                    else:
                        no = 1
                        rlist = "╭───「 admin List 」"
                        for x in settings["Owner"]:
                            rlist += "\n├≽{}. {}".format(str(no), cl.getContact(x).displayName)
                            no += 1
                        rlist += "\n╰───「 admin {} Members 」".format(len(settings["Owner"]))
                        cl.sendMessage(to=op.message.to, text=str(rlist))
                elif op.message.text.lower().startswith("刪除權限 "):
                    input1 = op.message.text.replace("刪除權限 ","")
                    sep = input1.split(" ")
                    for x in sep:
                        try:
                            a = settings["Owner"]
                            kill = settings["Owner"][(int(x)-1)]
                            a.remove(kill)
                            cl.sendMessage(op.message.to, "完成")
                        except:
                            cl.sendMessage(op.message.to, "無效範圍刪除失敗")
                elif "踢人列表" == op.message.text:
                    if klist == []:
                        cl.sendMessage(to=op.message.to, text="列表沒人")
                    else:
                        no = 1
                        rlist = "╭───「 kill List 」"
                        for x in klist:
                            rlist += "\n├≽{}. {}".format(str(no), cl.getContact(x).displayName)
                            no += 1
                        rlist += "\n╰───「 kill {} Members 」".format(len(klist))
                        cl.sendMessage(to=op.message.to, text=str(rlist))
                elif "runtime" == op.message.text:
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    cl.sendMessage(op.message.to, "機器運行時間 {}".format(str(runtime)))
                elif "進群踢人開" == op.message.text:
                    settings["joinkick"] = True
                    with open('temp.json', 'w') as fp:
                        json.dump(settings, fp, sort_keys=True, indent=4)
                    cl.sendMessage(to=op.message.to, text="已開啟")
                elif "進群踢人關" == op.message.text:
                    settings["joinkick"] = False
                    with open('temp.json', 'w') as fp:
                        json.dump(settings, fp, sort_keys=True, indent=4)
                    cl.sendMessage(to=op.message.to, text="已關閉")
                elif "專武開" == op.message.text:
                    settings["kick"] = True
                    with open('temp.json', 'w') as fp:
                        json.dump(settings, fp, sort_keys=True, indent=4)
                    cl.sendMessage(to=op.message.to, text="已開啟")
                elif "專武關" == op.message.text:
                    settings["kick"] = False
                    with open('temp.json', 'w') as fp:
                        json.dump(settings, fp, sort_keys=True, indent=4)
                    cl.sendMessage(to=op.message.to, text="已關閉")
                elif "清空列表" == op.message.text:
                    klist.clear()
                    cl.sendMessage(to=op.message.to, text="清除快取完成")
                elif op.message.text.lower() == ".set":
                    t0 = time.time() 
                    t1 = time.time() - t0
                    t2 = time.time() 
                    t3 = time.time() - t2
                    time.sleep(0.5)
                    ret_ = "偵測訊息\n"
                    if settings["kick"] == 0: ret_ +="專武已關閉\n"
                    else: ret_ += "專武已開啟\n"
                    if settings["joinkick"] == True: ret_ +="進群踢已開啟\n"
                    else: ret_ += "進群踢已關閉\n"
                    ret_ += "終端登入的次數 {}\n".format(len(bots))
                    ret_ += "登入版本 測試版專武"
                    cl.sendMessage(op.message.to, str(ret_))
                    return
    except Exception as e:
        print(e)
def RunBot():
    while True:
        try:
            ops = oepoll.singleTrace(count=50)
            if ops is not None:
                for op in ops:
                    oepoll.setRevision(op.revision)
                    bot(op)
        except Exception as e: print(e)
def Run():
    RunBot()
if __name__ == "__main__":
    Run()
