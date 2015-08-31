#!usr/bin/env python3

from Agent import *
from World import *
import numpy as np



#所有动作命名规范为，大写字母开头，正常动作单词首字母大写
# import numpy as np
# import matplotlib.pyplot as plt
# import mpl_toolkits.mplot3d
#  self.msched.append([function,{dictionary负责传递参数给函数}])


hjMax = {'hj1': 120.0,
         'hj2': 45.0,
         'raj1': 120.0,
         'raj2': 1.0,
         'raj3': 120.0,
         'raj4': 90.0,
         'laj1': 120.0,
         'laj2': 95.0,
         'laj3': 120.0,
         'laj4': 1.0,
         'rlj1': 1.0,
         'rlj2': 25.0,
         'rlj3': 100.0,
         'rlj4': 1.0,
         'rlj5': 75.0,
         'rlj6': 45.0,
         'llj1': 1.0,
         'llj2': 45.0,
         'llj3': 100.0,
         'llj4': 1.0,
         'llj5': 75.0,
         'llj6': 25.0, }
hjMin = {'hj1': -120.0,
         'hj2': -45.0,
         'raj1': -120.0,
         'raj2': -95.0,
         'raj3': -120.0,
         'raj4': -1.0,
         'laj1': -120.0,
         'laj2': -1.0,
         'laj3': -120.0,
         'laj4': -90.0,
         'rlj1': -90.0,
         'rlj2': -45.0,
         'rlj3': -25.0,
         'rlj4': -130.0,
         'rlj5': -45.0,
         'rlj6': -25.0,
         'llj1': -90.0,
         'llj2': -25.0,
         'llj3': -25.0,
         'llj4': -130.0,
         'llj5': -45.0,
         'llj6': -45.0, }


def TravesalAngleToFile(JointAngelName='',Step = 1):
    f = open(JointAngelName, "a")
    for travesalhjmin in hjMin:
        for travesalhjmax in hjMax:
            if str(travesalhjmin) == str(travesalhjmax) == JointAngelName:
                # print('Joint:', str(travesalhjmin), file=f)
                # print(str(travesalhjmin), file=f)
                # print('Rang:', hjMin[str(travesalhjmin)], '-->>', hjMax[str(travesalhjmax)], file=f)
                # print(hjMin[str(travesalhjmin)], '-->>', hjMax[str(travesalhjmax)], file=f)
                while hjMin[str(travesalhjmin)] < hjMax[str(travesalhjmax)]:
                    hjMin[str(travesalhjmin)] += Step
                    yield hjMin[str(travesalhjmin)]
                    # print(hjMin[str(travesalhjmin)], file=f)
    print('\n', file=f)
    f.close()


def FromFileToAngle(JointAngelName= ''):
    pass
    # with open(JointAngelName,'r') as file:      #用with打开可以自动close
    #     data = file.readlines()
    #
    # for line in data:
    #     line = line.split(' ')                   #分割单个数据
    #     FileToList = map(line)                  #转化为浮点数
    #     print(FileToList)
    # print(hh)

TravesalAngleToFile('llj3',1)

FromFileToAngle('llj3')


class Localizer(object):
    def __init__(self):
        pass

hj = {
    'hj1':{'angle':30},
    'hj2':{'percent':20}

}



class Action(NaoRobot):

    def Test_move_hj_to(self):
        self.msched.append([self.move_hj_to, {'hj': 'raj1', 'speed': 25, 'percent': 80}])
        self.msched.append([self.move_hj_to, {'hj': 'laj1', 'speed': 25, 'percent': 80}])
        self.msched.run()
    def Test_move_hj_to2(self):
        self.msched.append([self.move_hj_to, {'hj': 'raj1', 'speed': 3000, 'percent': 80}])     #if>100 3000=100
        self.msched.append([self.move_hj_to, {'hj': 'laj1', 'speed': 3000, 'percent': 80}])
        self.msched.run()

    def Test_move_hj_by(self):
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

    def Test_step_by_left_knee(self, time=time):             #结果是一直倒啊倒
        done = [False]

        print("ACC:", np.linalg.norm(self.acc.get()))

        done[0] = False
        self.msched.append([self.move_hj_to, {'hj': 'rlj3', 'percent': 50}, done])          #1 1+2斜左侧倒 1+3 向前倒　1+4侧着倒
        self.msched.append([self.move_hj_to, {'hj': 'rlj4', 'percent': 50}, done])        #2　2+3向右侧倒　　2+4向后倒
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

    def Test_step_by_right_knee(self, time=time):             #结果是一直倒啊倒
        done = [False]

        print("ACC:", np.linalg.norm(self.acc.get()))

        done[0] = False
        self.msched.append([self.move_hj_to, {'hj': 'llj3', 'percent': 50}, done])
        self.msched.append([self.move_hj_to, {'hj': 'llj4', 'percent': 50}, done])
        # self.msched.append([self.move_hj_to, {'hj': 'rlj5', 'percent': 100}, done])
        # self.msched.append([self.move_hj_to, {'hj': 'llj5', 'percent': 100}, done])

        self.Test_orientation(0.1)


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

    def Test_step_by_left_foot(self):
        self.msched.append([self.move_hj_to, {'hj': 'rlj5', 'percent': 70}])
    def Test_step_by_right_foot(self):
        self.msched.append([self.move_hj_to, {'hj': 'llj5', 'percent': 70}])
    def Test_Walk(self):
        # self.Test_step_by_left_foot()
        self.msched.append([self.move_hj_to, {'hj': 'rlj3', 'percent': 50}])
        self.msched.append([self.move_hj_to, {'hj': 'rlj4', 'percent': 50}])
        time.sleep(0.4)
        self.Test_step_by_right_foot()
        self.msched.append([self.move_hj_to, {'hj': 'llj3', 'percent': 50}])
        self.msched.append([self.move_hj_to, {'hj': 'llj4', 'percent': 50}])

        # while True:
        #     self.Test_step_by_left()
        #     self.Test_step_by_right()



    def Step_By_Left(self):
        pass

    def Step_By_Right(self):
        pass

    def Walk(self):
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

    def Stand_From_Back(self):
        pass

    def Stand_From_front(self):
        pass

    def Defend(self):
        pass

    def FindBall(self):
        pass

    def KeepFindBall(self):
        pass

    def CheckMyState(self,state):       #检查自己是倒是站是跑是协作
        pass

# if __name__ == '__main__':
#     Test = Action(7,'lamour','localhost',3100,'rsg/agent/nao/nao.rsg')
    #Test.Test_Weclome()
    #for i in range(1,100):      #动弹１００个循环看看
    # while(True) :
    #     Test.Test_Walk()             #此处发现错误
    # raise SchedulerConflict('The function "{}" is already in the queue.'.format(item[0]))Agent.SchedulerConflict: 'The function "<bound method Action.move_hj_to of <__main__.Action object at 0x7fa4b681ed68>>" is already in the queue.
    #应该是属于重用套接字地址错误,但机器人依然是可以动弹的
    #Test.Test_Weclome()