#!usr/bin/env python3

from Agent import *

class Action(NaoRobot):                 #先给几个参数试试能不能懂，speed这里有bug
    def Test_Weclome(self):
        self.msched.append([self.move_hj_to, {'hj': 'raj1', 'speed': 25, 'percent': 80}])
        self.msched.append([self.move_hj_to, {'hj': 'laj1', 'speed': 25, 'percent': 80}])
        self.msched.run()

    def Test_Walk(self,skip=False ):
        self.msched.append([self.move_hj_to,{'hj': 'rlj2', 'speed': 25, 'percent': 20}])
        self.msched.append([self.move_hj_to,{'hj': 'rlj3', 'speed': 25, 'percent': 20}])
        self.msched.append([self.move_hj_to,{'hj': 'rlj1', 'speed': 305, 'percent': 20}])
        self.msched.append([self.move_hj_to,{'hj': 'llj1', 'speed': 205, 'percent': 20}])
        self.msched.append([self.move_hj_to,{'hj': 'llj2', 'speed': 205, 'percent': 20}])
        self.msched.append([self.move_hj_to,{'hj': 'llj3', 'speed': 205, 'percent': 20}])
        self.msched.run()

    def Test_Weclome2(self):
        self.msched.append([self.move_hj_by,{'hj':'laj1', 'speed':25, 'percent': 80}])
        self.msched.append([self.move_hj_by,{'hj':'raj1', 'speed':25, 'percent': 80}])
if __name__ == '__main__':
    Test = Action(7,'lamour','localhost',3100,'rsg/agent/nao/nao.rsg')
    #Test.Test_Weclome()
    #for i in range(1,100):      #动弹１００个循环看看
    Test.Test_Weclome2()              #此处发现错误
    # raise SchedulerConflict('The function "{}" is already in the queue.'.format(item[0]))Agent.SchedulerConflict: 'The function "<bound method Action.move_hj_to of <__main__.Action object at 0x7fa4b681ed68>>" is already in the queue.
    #应该是属于重用套接字地址错误,但机器人依然是可以动弹的
    Test.Test_Weclome()