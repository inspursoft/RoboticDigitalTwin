#!/usr/bin/python3
# encoding: utf-8
import asyncio
import threading
import time
import ArmController as controller #舵机转动
import random
import json
import websockets

POS = {"clow": 1500, "head": 1500, "middle": 1500, "bottom": 1500}

# 机械臂位置校准
def Arm_Pos_Corr():
    controller.setServo(1, 1000, 500)
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
        clow = controller.Servos[0].getPosition() + random.randint(-20, 20) * 10

        # bottom = bottom if bottom > 1000 and bottom < 2000 else 1500
        clow = clow if clow > 500 and clow < 1500 else 1000
        controller.setServo(1, clow, spend)                                                         # clow [1500 - 500]
        controller.setServo(3, controller.Servos[2].getPosition() + random.randint(-20, 20) * 20, spend) # head
        # controller.setServo(4, controller.Servos[3].getPosition() + random.randint(-20, 20) * 20, spend) # middle
        # controller.setServo(5, controller.Servos[4].getPosition() + random.randint(-20, 20) * 20, spend) # botton
        time.sleep((spend + 100) / 1000)


# 服务器端主逻辑
async def getArmPos(websocket, path):
    while True:
        try:
            POS["clow"] = controller.Servos[0].getPosition()
            POS["head"] = controller.Servos[2].getPosition()
            POS["middle"] = controller.Servos[3].getPosition()
            POS["bottom"] = controller.Servos[4].getPosition()
            await websocket.send(json.dumps(POS))
            time.sleep(1.0 / 30)  # 约 30 帧/秒
        except websockets.ConnectionClosed:
            print("ConnectionClosed...", path)    # 链接断开
            break
        except websockets.InvalidState:
            print("InvalidState...")    # 无效状态
            break
        except Exception as e:
            print("Exception:", e)


if __name__ == "__main__":
    print("start")
    controller.initLeArm([0,0,0,0,0,0])
    time.sleep(1)
    Arm_Pos_Corr()
    print("init")

    # get_pos = threading.Thread(target=get_arm_pos)
    animate = threading.Thread(target=animate_arm)
    # get_pos.setDaemon(True)
    # animate.setDaemon(True)
    # get_pos.start()
    animate.start()
    
    asyncio.get_event_loop().run_until_complete(websockets.serve(getArmPos, "10.164.17.14", 8181))
    asyncio.get_event_loop().run_forever()
    # get_pos.join()
    animate.join()
    print("end")
