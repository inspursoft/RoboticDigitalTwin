#!/usr/bin/python3
# encoding: utf-8
import asyncio
import threading
import time
import ArmController as controller #舵机转动
import random
import websockets

# 机械臂位置校准
def Arm_Pos_Corr():
    controller.setServo(1, 1200, 500)
    controller.setServo(2, 500, 500)
    time.sleep(1)

def get_arm_pos():
    while True:
        pos = []
        for i in [0,2,3,4]:
            pos.append(controller.Servos[i].getPosition())
        print(pos)
        time.sleep(1.0 / 30)  # 30 帧/秒


def animate_arm():
    while True:
        spend = 2000 + random.randint(-20, 20) * 40
        # bottom = controller.Servos[4].getPosition() + random.randint(-20, 20) * 20
        # middle = controller.Servos[3].getPosition() + random.randint(-20, 20) * 20
        # head = controller.Servos[2].getPosition() + random.randint(-20, 20) * 20
        # clow = controller.Servos[0].getPosition() + random.randint(-20, 20) * 20
        controller.setServo(1, controller.Servos[0].getPosition() + random.randint(-20, 20) * 20, spend)
        controller.setServo(3, controller.Servos[2].getPosition() + random.randint(-20, 20) * 20, spend)
        controller.setServo(4, controller.Servos[3].getPosition() + random.randint(-20, 20) * 20, spend)
        controller.setServo(5, controller.Servos[4].getPosition() + random.randint(-20, 20) * 20, spend)
        time.sleep((spend + 100) / 1000)


if __name__ == "__main__":
    print("start")
    controller.initLeArm([0,0,0,0,0,0])
    time.sleep(1)
    Arm_Pos_Corr()
    get_pos = threading.Thread(target=get_arm_pos)
    animate = threading.Thread(target=animate_arm)
    # get_pos.setDaemon(True)
    # animate.setDaemon(True)
    get_pos.start()
    animate.start()
    get_pos.join()
    animate.join()
    print("end")
