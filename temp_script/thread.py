__author__ = 'king'


import threading,_thread   #thread 在python3.x以后更名为_thread
import time

from Action import *
from Agent import *

exitFlag = 0

class MultiClient(threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def join(self):
        pass
    # class hh(object):
    #     def __init__ (self,agentID,teamname,host,port,model,startCoordinates):                #把要执行的代码写进run函数里面
    #             #threading.Thread.run()
    #             self.agentID = agentID
    #             self.teamname = teamname
    #             self.host = host
    #             self.port = port
    #             self.model = model
    #             self.startCoordinates = startCoordinates
    #             NaoRobot(self.agentID,self.teamname,self.host,self.port,self.model,self.startCoordinates)
    #             print("starting" + self.name)
    #             print_time(self.name,self.counter,5)
    def lock(self):
        pass
    def live(self):
        pass
    def die(self):
        pass
    def run(self):
        print("starting" + self.name)
        print_time(self.name,self.counter,5)
        print("Exiting" + self.name)

def print_time(threadName,delay,counter):
        while counter:
            if exitFlag:
                _thread.exit()
            time.sleep(delay)
            print ("%s,%s" % threadName,time.ctime(time.time()))
            counter -= 1



#创建新的线程
#Player1 = MultiClient(1,"Player1",1)
#MultiClient.start(1,'lamour','localhost',3100,'rsg/agent/nao/nao.rsg',startCoordinates=[0.5,0.6,0])

Player1 = MultiClient(1,"player1",1)
Player2 = MultiClient(2,"player2",2)

Player1.start()
Player2.start()

print("Exiting Main Thread")