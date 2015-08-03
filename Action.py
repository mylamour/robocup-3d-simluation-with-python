#!usr/bin/env python3

from Agent import *


# import numpy as np
# import matplotlib.pyplot as plt
# import mpl_toolkits.mplot3d


class Action(NaoRobot):                 #先给几个参数试试能不能懂，speed这里有bug
    def Test_to(self):
        done = [False]
        self.msched.append([self.move_hj_to, {'hj': 'raj1', 'speed': 25, 'percent': 80},done])
        self.msched.append([self.move_hj_to, {'hj': 'laj1', 'speed': 25, 'percent': 80},done])
        self.msched.run()
    def Test_to2(self):
        self.msched.append([self.move_hj_to, {'hj': 'raj1', 'speed': 3000, 'percent': 80}])     #if>100 3000=100
        self.msched.append([self.move_hj_to, {'hj': 'laj1', 'speed': 3000, 'percent': 80}])
        self.msched.run()

    def Test_by(self):
        self.msched.append([self.move_hj_by, {'hj': 'raj1', 'speed': 25, 'percent': 80}])
        self.msched.append([self.move_hj_by, {'hj': 'laj1', 'speed': 25, 'percent': 80}])
        self.msched.run()

    def Test_orientation(self, length=1.0,filename='Test_Orientation'):  #自定义输出
        start = time.time()
        # gyrx = []         #回去看gyr类定义可知，它对x,y,z都是数组，不是列表，所以不能append和extend
        gyrx = np.array([1.0,0.0,0.0])
        gyry = np.array([1.0,0.0,0.0])
        gyrz = np.array([1.0,0.0,0.0])
        self.filename = filename
        f = open(self.filename,"a")            #a代表追加,其他还有，'w','r'
        while time.time() - start < length:
            print("Lengeh:",length,file = f)
            print("time: {:.3f}".format(time.time()-start),file = f)    #这才是３中的写法
            # print >> f,(self.gyr.rate)                #python 2中的写法
            print("Gyr.rate",self.gyr.rate,file = f)
            print("Gyr.x",self.gyr.x,file = f)
            # print(gyrx.__add__(self.gyr.x),file=f)
            print("Gyr.y",self.gyr.y,file = f)
            # print(gyry.__add__(self.gyr.y),file=f)
            print("Gyr.z",self.gyr.z,file = f)
            # print(gyrz.__add__(self.gyr.z),file=f)
            print("\n",file = f)
            time.sleep(CYCLE_LENGTH)

            #print(gyrx.extend(self.gyr.x))                  #怪不得不行，此处extend之后根本没有进gyrx数组
            #print(gyry.append(self.gyr.y))                  #为什么append也不行？
            #print(gyrz.append(self.gyr.z))
            #pylab.plot(self.gyr.x,self.gyr.y,self.gyr.x)
            # ax = plt.subplot(111,projection = '3d')
            # ax.plot_surface(gyrx,gyry,gyrz)
            # ax.set_xlabel('x')
            # ax.set_xlabel('y')
            # ax.set_xlabel('z')
            # plt.show()

    def Test_step_by_left(self, time=time):             #结果是一直倒啊倒
        done = [False]

        print("ACC:", np.linalg.norm(self.acc.get()))

        done[0] = False
        # self.msched.append([self.move_hj_to, {'hj': 'rlj3', 'percent': 50}, done])          #1 1+2斜左侧倒 1+3 向前倒　1+4侧着倒
        # self.msched.append([self.move_hj_to, {'hj': 'rlj4', 'percent': 50}, done])        #2　2+3向右侧倒　　2+4向后倒
        # self.msched.append([self.move_hj_to, {'hj': 'rlj5', 'percent': 100}, done])       #3　　3+4向前俯卧撑式
        # self.msched.append([self.move_hj_to, {'hj': 'llj5', 'percent': 100}, done])         #4

        self.Test_orientation(0.1)             #orientation方向，定位       这些数字有什么用，画个图看看？？


        while not done[0]:
            print("ACC:", np.linalg.norm(self.acc.get()))
            print("GYR:", self.gyr.get_orientation())
            print(self.gyr.x)
            print(self.gyr.y)
            print(self.gyr.z)
            print("")
            time.sleep(0.05)



        time = time.time()
        time.sleep(1.0)

        done[0] = False
        # self.msched.append([self.move_hj_to, {'hj': 'hj1', 'percent': 0}, done])
        # while not done[0]:
        #     pass
        # done[0] = False
        # self.msched.append([self.move_hj_to, {'hj': 'hj1', 'percent': 50}, done])
        # while not done[0]:
        #     pass

    def Walk(self):
        pass
    def Step_by_left(self):
        pass

    def Step_by_right(self):
        pass

    def Run(self):
        pass

    def Kick(self):
        pass

    def LongKick(self):
        pass

    def BallInterception(self):
        pass

    def GoalTending(self):
        pass

    def Dribbling(self):
        pass

    def Stand(self):
        pass

    def Stand_from_Back(self):
        pass

    def Stand_from_front(self):
        pass

    def Defend(self):
        pass

    def FindBall(self):
        pass

    def CheckMyState(self,state):       #检查自己是倒是站是跑是协作
        pass

if __name__ == '__main__':
    Test = Action(7,'lamour','localhost',3100,'rsg/agent/nao/nao.rsg')
    #Test.Test_Weclome()
    #for i in range(1,100):      #动弹１００个循环看看
    while(True) :
        Test.Test_Walk()             #此处发现错误
    # raise SchedulerConflict('The function "{}" is already in the queue.'.format(item[0]))Agent.SchedulerConflict: 'The function "<bound method Action.move_hj_to of <__main__.Action object at 0x7fa4b681ed68>>" is already in the queue.
    #应该是属于重用套接字地址错误,但机器人依然是可以动弹的
    #Test.Test_Weclome()