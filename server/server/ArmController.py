#!/usr/bin/python3
# encoding: utf-8
import time
import sqlite3 as sql    # 给予sqlite3一个别名sql
import pigpio
from LeServo import PWM_Servo   # 调用LeServo中的PWM_Servo
import os

Servos = ()     # 创建一个空元组，创建时可不指定元素的个数，相当于不定长的数组，但一旦创建就不能修改元组的长度。
runningAction = False   # 初始化运动标识
pi = None
stopRunning = False     # 初始化停止标识


# ####判断+赋值
def setServo(servoId, pos, time):     # 舵机转动函数
    global runningAction
    
    if servoId < 1 or servoId > 6:
        return
    if pos > 2500:
        pos = 2500
    elif pos < 500:
        pos = 500
    else:
        pass    # 什么也不做
    if time > 30000:
        time = 30000
    elif time < 20:
        time = 20
    else:
        pass    
    if runningAction is False:  # 如果没有动作组在运行
        Servos[servoId - 1].setPosition(pos, time)
        # -1是因为数组是从0开始的，在Python的解释器内部，当我们调用Servos[servoId - 1].setPosition(pos, time)时,
        # 实际上Python解释成PWM_Servo.setPosition(Servos[servoId - 1], pos, time)，也就是说把self替换成类的实例。


# #####获取当前舵机位置
def setServo_CMP(servoId, pos, time):
    # print(servoId, pos, time)
    if servoId < 1 or servoId > 6:
        return
    # print(Servos[servoId-1].getPosition())
    setServo(servoId, Servos[servoId - 1].getPosition() + pos, time);


# ######偏差加载
def setDeviation(servoId, d):
    global runningAction
    if servoId < 1 or servoId > 6:
        return
    if d < -300 or d > 300:
        return
    if runningAction is False:
        Servos[servoId -1].setDeviation(d)  # 偏差载入


def stopActionGroup():   # 动作组停止运行
    global stopRunning
    stopRunning = True


def runActionGroup(actNum, times):
    global runningAction
    global stopRunning
    actNum = "./ActionGroups/" + actNum + ".d6a"
    # print(actNum)
    if os.path.exists(actNum) is True:  # 如果存在该动作组
        ag = sql.connect(actNum)    # 打开数据库actNum
        cu = ag.cursor()    # 定义了一个游标
        cu.execute("select * from ActionGroup")     # 查询
        if runningAction is False:  # 没有动作组在运行
            runningAction = True    # 运行该动作组
            while True:
                if stopRunning is True:     #
                    stopRunning = False
                    runningAction = False
                    cu.close()  # 关闭一个数据库链接
                    ag.close()  # 游标关闭
                    break
                act = cu.fetchone()     # 返回列表中的第一项，再次使用,则返回第二项,依次下去
                if act is not None:
                    # print(act)
                    for i in range(0, 6, 1):
                        Servos[i].setPosition(act[2+i], act[1])
                    time.sleep(float(act[1]*1.2)/1000.0)    # 运行时间
                else:
                    runningAction = False
                    cu.close()
                    ag.close()
                    break
    else:
        runningAction = False
        print("未能找到动作组文件")


def initLeArm(d):
    global Servos
    global pi
    pi = pigpio.pi()    # 实例化
    # host = os.popen("ip route | awk 'NR==1 {print $3}'|xargs echo -n").read() # 获取路由 IP 以连接到宿主机上的 pigpiod 服务
    # pi = pigpio.pi(host)    # 实例化
    servo1 = PWM_Servo(pi, 12, deviation=d[0], control_speed = True) #初始化各舵机
    servo2 = PWM_Servo(pi, 16, deviation=d[1], control_speed = True)
    servo3 = PWM_Servo(pi, 20, deviation=d[2], control_speed = True)
    servo4 = PWM_Servo(pi, 21, deviation=d[3], control_speed = True)
    servo5 = PWM_Servo(pi, 19, deviation=d[4], control_speed = True)
    servo6 = PWM_Servo(pi, 13, deviation=d[5], control_speed = True)
    Servos = (servo1, servo2, servo3, servo4, servo5, servo6)
    
    for i in range(0, 6, 1):
        Servos[i].setPosition(1500, 1000)  # 1-6号舵机转到中位

def stopLeArm():
    print("停止机械臂")
    pi.stop()   # 断开pwm连接

if __name__ == "__main__":
    initLeArm([0,0,0,0,0,0])
    setServo(1, 1000, 1000)
    time.sleep(1.1)
