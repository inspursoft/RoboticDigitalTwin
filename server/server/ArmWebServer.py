#!/usr/bin/python3
# encoding: utf-8
# web 远程控制
import asyncio
import threading
import time
import ArmController as controller  # 舵机转动
import ArmCmd as cmd
import random
import json
import websockets
import requests

POS = {"claw": 1500, "head": 1500, "middle": 1500, "bottom": 1500, "base": 500}
VIEWERS = set()
message = None
receiveTime = time.time()

# 机械臂位置校准


def Arm_Pos_Corr():
    controller.setServo(1, 1500, 500)
    controller.setServo(2, 500, 500)
    time.sleep(1)


async def update_pos():
    global message

    while True:
        POS["claw"] = controller.Servos[0].getPosition()
        POS["head"] = controller.Servos[2].getPosition()
        POS["middle"] = controller.Servos[3].getPosition()
        POS["bottom"] = controller.Servos[4].getPosition()
        POS["base"] = controller.Servos[5].getPosition()
        message = json.dumps(POS)
        # print("claw: \033[31m%d\033[0m \t head: \033[33m%d\033[0m \t middle: \033[34m%d\033[0m \t bottom: \033[32m%d\033[0m" %(POS["claw"],POS["head"],POS["middle"],POS["bottom"]))
        await asyncio.sleep(1.0 / 30) # 约 30 帧/秒

sight = {"left":"red"}
async def hearing_and_sight():
    global receiveTime
    global sight
    hearingUrl = "http://192.168.149.48:8000/getColor" # 10.165.19.234
    sightUrl = "http://10.164.17.14:8183"

    while True:
        try:
            hear = requests.get(hearingUrl).text
            # hear = "无"
            # ra = random.randint(0,100)
            # if ra < 25:
            #     hear = "红"
            # elif ra > 75:
            #     hear = "蓝"
            # print(ra)
            if (hear == "蓝" or hear == "红") and time.time() - receiveTime > 15:
                receiveTime = time.time()
                try:
                    sight = json.loads(requests.get(sightUrl).text)
                except Exception as e:
                    print(e)
                receiveTime = time.time()
                base = 500
                if (sight["left"] == 'red' and hear == "蓝") or (sight["left"] == 'blue' and hear == "红"):
                    base = 2500
                print("hearing: %s\tsight-left: %s" %(hear, sight["left"]))
                await catchCube(base)
                await asyncio.sleep(5.5)
            else:
                await asyncio.sleep(5.5)
        except Exception as e:
            await asyncio.sleep(5.5)
            print(e)


async def catchCube(base):
    cmd.cmd_i001([1900, 6, 1, 500, 2, 500, 3, 1500,
                  4, 1500, 5, 1500, 6, base])  # reset
    await asyncio.sleep(2)
    cmd.cmd_i001([2900, 6, 1, 500, 2, 500, 3, 580, 4,
                  800, 5, 1500, 6, base])  # prepare
    await asyncio.sleep(3)
    controller.setServo(1, 1200, 400)  # catch
    await asyncio.sleep(0.5)
    cmd.cmd_i001([2000, 6, 1, 1200, 2, 500, 3, 1100,
                  4, 1100, 5, 1500, 6, base])  # show
    await asyncio.sleep(4)
    cmd.cmd_i001([1900, 6, 1, 1200, 2, 500, 3, 580, 4,
                  800, 5, 1500, 6, base])  # put down
    await asyncio.sleep(2)
    controller.setServo(1, 500, 400)  # loose
    await asyncio.sleep(0.5)
    cmd.cmd_i001([3000, 6, 1, 1500, 2, 500, 3, 1500,
                  4, 1500, 5, 1500, 6, base])  # reset
    await asyncio.sleep(3)


async def operation(msg):
    global receiveTime

    try:
        if msg == "reset":
            if time.time() - receiveTime > 2:
                receiveTime = time.time()
                cmd.cmd_i001([2000, 6, 1, 1500, 2, 500, 3,
                              1500, 4, 1500, 5, 1500, 6, 500])
        else:
            msg_data = msg.split(":")
            if msg_data[0] == "catch" and time.time() - receiveTime > 15:
                receiveTime = time.time()
                base = 500
                if msg_data[1] == "right":
                    base = 2500
                await catchCube(base)
            else:
                move_arm(msg_data[0], int(msg_data[1]))
    except Exception as e:
        raise e


def move_arm(arm, pos):
    if arm == "claw":
        controller.setServo(1, pos, 150)
    elif arm == "head":
        controller.setServo(3, pos, 150)
    elif arm == "middle":
        controller.setServo(4, pos, 150)
    elif arm == "bottom":
        controller.setServo(5, pos, 150)
    elif arm == "base":
        controller.setServo(6, pos, 1000)
    else:
        print("error action:", arm, pos)


async def send_msg(websocket):
    global message
    while True:
        try:
            if message:
                await websocket.send(message)
            # 直接用time.sleep会造成只能一个客户端连接，见 https://websockets.readthedocs.io/en/stable/faq.html#server-side
            await asyncio.sleep(1.0 / 30)
        except:
            raise


async def recv_msg(websocket):
    while True:
        try:
            recv_text = await websocket.recv()
            print(websocket.remote_address[0], ">", recv_text)
            await operation(recv_text)
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


def thread_loop_task(loop):

    # 为子线程设置自己的事件循环
    asyncio.set_event_loop(loop)

    task = asyncio.gather(update_pos(), hearing_and_sight())
    loop.run_until_complete(task)


def run():
    print("start")
    # 创建一个事件循环thread_loop
    thread_loop = asyncio.new_event_loop()

    # 将thread_loop作为参数传递给子线程
    t = threading.Thread(target=thread_loop_task, args=(thread_loop,))
    t.daemon = True
    t.start()

    asyncio.get_event_loop().run_until_complete(websockets.serve(get_pos, "", 8181))
    asyncio.get_event_loop().run_forever()

    print("end")


if __name__ == "__main__":
    run()
