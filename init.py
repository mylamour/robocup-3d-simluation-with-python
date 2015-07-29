__author__ = 'king'

#! /usr/bin/env python3
import threading

from Agent import *
from Action import *
from Think import *




if __name__ == '__main__':
    Naomodel = {"Default" : 'rsg/agent/nao/nao.rsg',
                "Type_0" : 'rsg/agent/nao/nao_hetero.rsg 0',
                "Type_1" : 'rsg/agent/nao/nao_hetero.rsg 1',
                "Type_2" : 'rsg/agent/nao/nao_hetero.rsg 2',
                "Type_3" : 'rsg/agent/nao/nao_hetero.rsg 3',
                "Type_4" : 'rsg/agent/nao/nao_hetero.rsg 4'
                }
    MyNao = {"Player1":NaoRobot(1,'lamour','localhost',3100,Naomodel["Type_0"], startCoordinates=[-0.5, 0.0, 0]),
            # "Player2":NaoRobot(2,'lamour','localhost',3100,Naomodel["Type_0"], startCoordinates=[-1.5, 0.0, 0]),
            # "Player3":NaoRobot(3,'lamour','localhost',3100,Naomodel["Type_0"],startCoordinates=[-2.5, 0.0, 0]),
            # "Player4":NaoRobot(4,'lamour','localhost',3100,Naomodel["Type_1"], startCoordinates=[-3.5, -2.0, 0]),
            # "Player5":NaoRobot(5,'lamour','localhost',3100,Naomodel["Type_1"], startCoordinates=[-3.5, 0.0, 0]),
             #"Player6":NaoRobot(6,'lamour','localhost',3100,Naomodel["Type_2"], startCoordinates=[-3.5, 2.0, 0]),
             #"Player7":NaoRobot(7,'lamour','localhost',3100,Naomodel["Type_2"], startCoordinates=[-4.5, 0.0, 0]),
             "Player8":NaoRobot(8,'lamour','localhost',3100,Naomodel["Type_2"], startCoordinates=[-5.5, 0.0, 0]),
             "Player9":NaoRobot(9,'lamour','localhost',3100,Naomodel["Type_3"], startCoordinates=[-6.5, -3.0, 0]),
             "Player10":NaoRobot(10,'lamour','localhost',3100,Naomodel["Type_3"], startCoordinates=[-6.5, 0.0, 0]),
             "Player11":NaoRobot(11,'lamour','localhost',3100,Naomodel["Type_3"], startCoordinates=[-11.5, 0.0, 0])
             }
            #不知道为什么在一个文件里初始化不能全部上场，但通过两个脚本文件便可以将１１个搞定
