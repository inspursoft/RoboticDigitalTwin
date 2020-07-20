#! /usr/bin/python3
# encoding: utf-8
import os
import re
import ArmController as controller
import LeConf
import LeActList
import threading

actdir = "./ActionGroups/"

class LeError(Exception):
    def __init__(self, data=(), msg="LeError"):
        self.data = data
        self.msg = msg

def cmd_i000(par):  #指令000 空指令
    pass

def cmd_i001(par):  # 指令001 舵机运动
    global Deviation
    if par[0] > 30000:
        par[0] = 30000
    if par[0] < 20:
        par[0] = 20
    if not par[1] * 2 + 2 == len(par) or not len(par) >= 4:
        raise LeError(tuple(par),"舵机运动指令长度错误")

    Servos = par[2:]
    for i in range(0, len(Servos),2) :
        if Servos[i] > 6 or Servos[i] < 1 or Servos[i+1] > 2500 or Servos[i+1] < 500:
            raise LeError((Servos[i],Servos[i+1]), "舵机运动参数错误")
        controller.setServo(Servos[i], Servos[i+1],par[0])

def cmd_i002(par):  # 指令002 停止运动
    controller.stopActionGroup()

def cmd_i003(sock, data =["",""]):  # 指令003 运行动作组
    if (not len(data) == 2) or (not data) or (not data[0]) or (not data[1]) :
        raise LeError(tuple(data), "运行动作组指令错误")
    par = None
    try:
        par = int(data[1])
    except:
        raise LeError((data[1],),"动作组运行次数错误")

    print(data[0])
    print(par)
    if not par is None:
        try:
            threading.Thread(target=controller.runActionGroup, args=(data[0],par)).start()
            #controller.runActionGroup(data[0], par)
        except Exception as e:
            print(e)
        #controller.runActionGroup(data[0], par)

def cmd_i004(sock, data = []):  #指令 004查询动作组
    actList = LeActList.listActions(actdir)
    actList.sort()
    if not len(actList) is 0:
        
        for i in range(0, len(actList), 10):
            str_head = "I004-" + str(len(actList))
            str_tial = "-" + str(i+1)  + "-"
            str_tial1 = ""
            t = 10
            for j in range(0, 10, 1):
                if i+j < len(actList):
                    str_tial1 += "-" +actList[i+j][:-4]
                else:
                    if t == 10:
                        t = j
            if str_tial1:
                str_head = str_head + str_tial + str(i+t) + str_tial1 + "\r\n"
                sock.sendall(str_head.encode())
    else:
        s = "I004-0-0-0\r\n"
        sock.sendall(s)

    print(len(actList))
    print(actList)

def cmd_i005(sock, data = []): #指令 005 删除一个动作组
    if data:
        for d in data:
            if d:
                os.remove(actdir + d + ".d6a")

def cmd_i006(sock, data = []):  #指令 006 删除所有动作组
    actList = LeActList.listActions(actdir)
    for d in actList:
        os.remove(actdir + d)

def cmd_i007(sock, data = []):
    try:
        time = int(data[0])
        servo_num = int(data[1])
        #print(time,servo_num)
        servo_data = []
        for i in range(servo_num):
            servo_id = int(data[2 + i * 2])
            servo_pos = int(data[3 + i * 2])
            servo_data.append((servo_id, servo_pos-10000))
        #print(servo_data)
    except:
        raise LeError(tuple(data),"canshucuowu")
    try:
        for d in servo_data:
            controller.setServo_CMP(d[0], d[1], time)
    except Exception as e:
        print(cuowu, e)

cmd_list = [cmd_i000, cmd_i001, cmd_i002, cmd_i003, cmd_i004, cmd_i005, cmd_i006, cmd_i007]

