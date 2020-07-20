#!! /usr/bin/python3
# encoding: utf-8
#必须将编码注释放在第一行或者第二行

import pigpio #pigpio是一个允许控制GPIO的C语言库，同时pigpio是一个适用于树莓派的Python 模块，允许用过pigpio daemon程序控制通用GPIO口
import time    # 引入time模块
import threading #多线程库（重量级）

class PWM_Servo(object): #class定义一个类，object在python3中默认加

    def __init__(self, pi, pin, freq = 50, min_width = 500, max_width=2500, deviation=0, control_speed=False):
        #__init__方法在类的对象被建立时，马上运行。该方法用来对对象进行初始化
        self.pi = pi  #在LeArm.py中会被调用
        self.SPin = pin   #舵机引脚号
        self.Freq = freq #在LeArm.py中会被调用
        self.Min = min_width   #最小脉宽值
        self.Max = max_width  #最大脉宽值
        self.Deviation = deviation #舵机偏差
        self.speedControl = control_speed #舵机运行的速度
        
        self.Position = 1500  #舵机当前位置值
        self.positionSet = self.Position #初始化位置
        
        self.stepTime = 20  #每步运行时间
        self.positionInc = 0.0 #当前位置与目标位置差值
        self.Time = 0 #非必要
        self.Time_t = 0 #运行时间参数
        self.incTimes = 0  #分步次数
        
        self.positionSet_t = 0 #运行角度参数
        self.posChanged = False  #位置变化标志
        self.servoRunning = False  #舵机运行标志

        #self.pi.set_PWM_range(self.SPin, 1000000 / self.Freq) #在LeArm.py中会被调用
        #self.pi.set_PWM_frequency(self.SPin, self.Freq) #在LeArm.py中会被调用
        
        if control_speed is True: #当运行速度改变时
            t = threading.Thread(target=PWM_Servo.updatePosition, args=(self,))
            t.setDaemon(True)
            t.start()

    def setPosition(self, pos, time = 0): #若无time参数则默认为0
        if pos < self.Min or pos > self.Max: #防止超出舵机转动范围
            print(pos)
            return
        if time == 0: #如果没有输入时间参数
            self.Position = pos
            self.positionSet = self.Position
            self.pi.set_PWM_dutycycle(self.SPin, self.Position + self.Deviation) #在LeArm.py中会被调用
        else:
        #单步时间过长或过短则调整到上下限值
            if time < 20: #最短时间20ms
                self.Time_t = 20
            elif time > 30000: #最长30000ms 即30秒
                self.Time_t = 30000
            else:
                self.Time_t = time
            self.positionSet_t = pos #目标角度
            self.posChanged = True #参数都符合则置舵机运动标志为真

            
    def getPosition(self): #当前舵机位置值
        return self.Position

    def updatePosition(self):
       
        while True:
            if self.posChanged is True: #角度有变化
                self.Time = self.Time_t  #目标运行时间
                self.positionSet = self.positionSet_t #目标角度
                self.posChanged = False #清除标志

                self.incTimes = int(self.Time / self.stepTime )#分步次数
                self.positionInc =  self.Position - self.positionSet #差值
                self.positionInc = int(self.positionInc / self.incTimes) #每步转动的角度
                self.servoRunning = True #            置舵机运行标志为真

            if self.servoRunning is True:
                self.incTimes -= 1 #运行次数每次减一
                if self.incTimes == 0: #直到次数为0
                    self.Position = self.positionSet #记录当前位置
                    self.servoRunning = False #舵机停止转动
                else:
                    self.Position = self.positionSet + self.positionInc * self.incTimes #舵机当前位置值
                #self.pi.set_PWM_dutycycle(self.SPin, self.Position + self.Deviation) #在LeArm.py中会被调用
                self.pi.set_servo_pulsewidth(self.SPin, int(self.Position + self.Deviation) )
            time.sleep(0.02) #延时20ms让舵机到达指定位置
            
            
        def setDeviation(newD = 0): #偏差调整
            if newD > 300 or newD < -300: #偏差范围
                return
            self.Deviation = newD






