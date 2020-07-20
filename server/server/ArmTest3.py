#!/usr/bin/python3
# encoding: utf-8
# 多客户端连接查看
import asyncio
import threading
import time
import ArmController as controller #舵机转动
import random
import json
import websockets

POS = {"clow": 1500, "head": 1500, "middle": 1500, "bottom": 1500}
VIEWERS = set()
message = None

# 机械臂位置校准
def Arm_Pos_Corr():
    controller.setServo(1, 1000, 500)
    controller.setServo(2, 500, 500)
    time.sleep(1)


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


def update_pos():
    global message

    while True:
        POS["clow"] = controller.Servos[0].getPosition()
        POS["head"] = controller.Servos[2].getPosition()
        POS["middle"] = controller.Servos[3].getPosition()
        POS["bottom"] = controller.Servos[4].getPosition()
        message = json.dumps(POS)
        print("clow: \033[31m%d\033[0m \t head: \033[33m%d\033[0m \t middle: \033[34m%d\033[0m \t bottom: \033[32m%d\033[0m" %(POS["clow"],POS["head"],POS["middle"],POS["bottom"]))
        time.sleep(1.0 / 30) # 约 30 帧/秒


# 加入消息列表
async def get_pos(websocket, path):
    global message

    while True:
        try:
            VIEWERS.add(websocket)
            if message:
                await websocket.send(message)
            await asyncio.sleep(1.0 / 30) # 直接用time.sleep会造成只能一个客户端连接，见 https://websockets.readthedocs.io/en/stable/faq.html#server-side
        except websockets.ConnectionClosed:
            print("ConnectionClosed...", path)    # 链接断开
            VIEWERS.remove(websocket)
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

    animate = threading.Thread(target=animate_arm)
    update = threading.Thread(target=update_pos)
    animate.setDaemon(True)
    update.setDaemon(True)
    animate.start()
    update.start()
    
    asyncio.get_event_loop().run_until_complete(websockets.serve(get_pos, "10.164.17.14", 8181))
    asyncio.get_event_loop().run_forever()

    animate.join()
    update.join()
    print("end")