#!/usr/bin/python3
# encoding: utf-8

import socketserver
import threading
import time
import re
import ArmController as controller #舵机转动
import LeConf #偏差
from ArmCmd import LeError 
import ArmCmd
import ArmWebServer as web

class ServoServer(socketserver.BaseRequestHandler):
    def handle(self):
        print("已连接")
        conn = self.request
        Flag = True
        recv = b''
        recv_data = ""
        while Flag:
            try:
                recv = conn.recv(1024)
                recv_data += recv.decode()
                # print(recv_data)
                if not recv_data:
                    Flag = False
                    print("break")
                    break
                recv_data = recv_data.replace(' ', '')
                cp = re.compile(r'\r\n')
                test = cp.search(recv_data)
                if test:
                    rdata = recv_data.split("\r\n")  #分割
                    recv_data = recv_data[len(rdata[0]) + 2:]
                    
                    rdata = [rdata[0]]
                    for data in rdata:
                        if data:
                            rex = re.compile(r'^(I[0-9]{3}).*')  # 判断收到的指令是否符合规则
                            match = data
                            #print(match)
                            match = rex.match(match)
                            # print('******')
                            if match:
                                if not 0 == match.start() or not len(data) == match.end():
                                    print("错误指令 1")
                                else:
                                    data = data.split('-')
                                    cmd = data[0][1:5]
                                    del data[0]
                                    par = []
                                    #print(data)
                                    try:
                                        cmd = int(cmd)
                                        if cmd >= 3 and cmd <= 7:
                                            print(cmd)
                                            ArmCmd.cmd_list[cmd](conn, data)
                                        else:
                                            for p in data:
                                                par.append(int(p))
                                            print(cmd, par)
                                            ArmCmd.cmd_list[cmd](par)
                                    except LeError as err:
                                        print(err.msg)
                                        print(err.data)
                                    except:
                                        print("指令执行错误")
                            if not Flag:
                                print("break1")
                                break
            except Exception as e:
                print(e)
                break

    def finish(self):
        print("已断开")


class LeServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    if not len(LeConf.Deviation) == 6:
        print("偏差数量错误")
        sys.exit()
    else:
        d = []
        for i in range(0,len(LeConf.Deviation), 1):
            if LeConf.Deviation[i] > 1600 or LeConf.Deviation [i]< 1400:
                print("偏差值超出范围1200-1800")
                sys.exit()
            else:
                d.append(LeConf.Deviation[i] - 1500)

    controller.initLeArm(tuple(d))
    ArmCmd.cmd_i001([1000, 6, 1, 1500, 2, 1500, 3, 1500, 4, 1500, 5, 1500, 6, 500])
    server = LeServer(("", 8947), ServoServer)
    try:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
        web.run()
        while True:
            time.sleep(0.1)
    except:
        server.shutdown()
        server.server_close()
        controller.stopLeArm()
