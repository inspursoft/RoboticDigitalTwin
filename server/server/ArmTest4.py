#!/usr/bin/python3
# encoding: utf-8
# web 远程控制
import asyncio
import threading
import time
import ArmController as controller #舵机转动
import ArmCmd
import random
import json
import websockets

POS = {"claw": 1500, "head": 1500, "middle": 1500, "bottom": 1500}
VIEWERS = set()
message = None
receiveTime = time.time()

# 机械臂位置校准
def Arm_Pos_Corr():
    controller.setServo(1, 1500, 500)
    controller.setServo(2, 500, 500)
    time.sleep(1)


def update_pos():
    global message

    while True:
        POS["claw"] = controller.Servos[0].getPosition()
        POS["head"] = controller.Servos[2].getPosition()
        POS["middle"] = controller.Servos[3].getPosition()
        POS["bottom"] = controller.Servos[4].getPosition()
        message = json.dumps(POS)
        # print("claw: \033[31m%d\033[0m \t head: \033[33m%d\033[0m \t middle: \033[34m%d\033[0m \t bottom: \033[32m%d\033[0m" %(POS["claw"],POS["head"],POS["middle"],POS["bottom"]))
        time.sleep(1.0 / 30) # 约 30 帧/秒


def operation(msg):
    global receiveTime

    try:
        if msg == "reset":
            if time.time() - receiveTime > 0.5:
                receiveTime = time.time()
                ArmCmd.cmd_i001([500, 6, 1, 1500, 2, 500, 3, 1500, 4, 1500, 5, 1500, 6, 1500])
        else:
            msg_data = msg.split(":")
            move_arm(msg_data[0], int(msg_data[1]))
    except Exception:
        raise


def move_arm(arm, pos):
    if arm == "claw":
        controller.setServo(1, pos, 150)
    elif arm == "head":
        controller.setServo(3, pos, 150)
    elif arm == "middle":
        controller.setServo(4, pos, 150)
    elif arm == "bottom":
        controller.setServo(5, pos, 150)
    else:
        raise Exception("error arm!")


async def send_msg(websocket):
    global message
    while True:
        try:
            if message:
                await websocket.send(message)
            await asyncio.sleep(1.0 / 30) # 直接用time.sleep会造成只能一个客户端连接，见 https://websockets.readthedocs.io/en/stable/faq.html#server-side
        except:
            raise

async def recv_msg(websocket):
    while True:
        try:
            recv_text = await websocket.recv()
            print(websocket.remote_address[0], ">", recv_text)
            operation(recv_text)
        except:
            raise


# 加入消息列表
async def get_pos(websocket, path):
    global message

    VIEWERS.add(websocket)
    print("Connect to", websocket.remote_address[0])
    try:
        res = await asyncio.gather(
            send_msg(websocket),
            recv_msg(websocket),
            return_exceptions=True
        )
        raise res[0]
    except websockets.ConnectionClosed:
        print("Connection closed:", websocket.remote_address[0])    # 链接断开
        VIEWERS.remove(websocket)
    except websockets.InvalidState:
        print("InvalidState:", websocket.remote_address[0])    # 无效状态
    except Exception as e:
        print("Exception:", e)


def run():
    print("start")

    update = threading.Thread(target=update_pos)
    update.setDaemon(True)
    update.start()
    
    asyncio.get_event_loop().run_until_complete(websockets.serve(get_pos, "", 8181))
    asyncio.get_event_loop().run_forever()

    print("end")


if __name__ == "__main__":
    run()
