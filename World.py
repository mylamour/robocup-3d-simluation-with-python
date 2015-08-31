__author__ = 'king'
"""
一个想法：混合shell编程，直接读取rcssserver目录下的naosoccersim.rb然后正则分析进来，这样应该说更具有仿真性，
更像一个人获取到世界一样，而不是每次都要自己设置，这不像一个人
"""

from Agent import *
# import numpy as np
# from enum import Enum
import math
#有的是从一个配置文件读取，有的是从消息中获取

NaoSoccerSimParam = {
            'AgentRadius':0.4,
            'NotStandingMaxTime':30.0,
            'GoalieNotStandingMaxTime':60.0,        #守门员不能站起的最大时间

            'WaitBeforeKickOff':30.0,
            'AutomaticKickOff':False,

            'FieldLength':30.0,
            'FieldWidth':20.0,
            'FieldHeight':40.0,

            'GoalWidth':2.1,
            'GoalDepth':0.6,
            'GoalHeight':0.8,

            'PenaltyLength':1.8,                     #Penalty罚球
            'PenaltyWidth':3.9,

            'FreeKickDistance':2.0,
            'FreeKickMoveDist':2.2,

            'GoalKickDist':1.0,
            'BorderSize':0.0,


            'BallRadius':0.042,
            'BallMass':0.026,

            'MaxPlayersInsideOwnArea':3.0,
            'MinOppDistance':0.8,
            'Min2OppDistance':0.4,
            'Min3OppDistance':1.0
        }

FlagPlayerOnLeft = {

    'F1L' : {'x': -NaoSoccerSimParam['FieldLength']/2.0,
            'y':  NaoSoccerSimParam['FieldWidth']/2.0,
            'z':  1e-9},

    'F2L' : {'x': -NaoSoccerSimParam['FieldLength']/2.0,
            'y':  -NaoSoccerSimParam['FieldWidth']/2.0,
            'z':  1e-9},

    'F1R' : {'x': NaoSoccerSimParam['FieldLength']/2.0,
            'y':  NaoSoccerSimParam['FieldWidth']/2.0,
            'z':  1e-9},

    'F2R' : {'x': NaoSoccerSimParam['FieldLength']/2.0,
            'y':  -NaoSoccerSimParam['FieldWidth']/2.0,
            'z':  1e-9},

    'G1L' : {'x': -NaoSoccerSimParam['FieldLength']/2.0,
            'y':  NaoSoccerSimParam['GoalWidth']/2.0,
            'z':  NaoSoccerSimParam['GoalHeight']},

    'G2L' : {'x': -NaoSoccerSimParam['FieldLength']/2.0,
            'y':  -NaoSoccerSimParam['GoalWidth']/2.0,
            'z':  NaoSoccerSimParam['GoalHeight']},

    'G1R' : {'x': NaoSoccerSimParam['FieldLength']/2.0,
            'y':  NaoSoccerSimParam['GoalWidth']/2.0,
            'z':  NaoSoccerSimParam['GoalHeight']},

    'G2R' : {'x': NaoSoccerSimParam['FieldLength']/2.0,
            'y':  -NaoSoccerSimParam['GoalWidth']/2.0,
            'z':  NaoSoccerSimParam['GoalHeight']}
}

FlagPlayerOnRight = {

    'F1L' : {'x': NaoSoccerSimParam['FieldLength']/2.0,
            'y':  -NaoSoccerSimParam['FieldWidth']/2.0,
            'z':  1e-9},

    'F2L' : {'x': NaoSoccerSimParam['FieldLength']/2.0,
            'y':  NaoSoccerSimParam['FieldWidth']/2.0,
            'z':  1e-9},

    'F1R' : {'x': -NaoSoccerSimParam['FieldLength']/2.0,
            'y':  -NaoSoccerSimParam['FieldWidth']/2.0,
            'z':  1e-9},

    'F2R' : {'x': -NaoSoccerSimParam['FieldLength']/2.0,
            'y':  NaoSoccerSimParam['FieldWidth']/2.0,
            'z':  1e-9},

    'G1L' : {'x': NaoSoccerSimParam['FieldLength']/2.0,
            'y':  -NaoSoccerSimParam['GoalWidth']/2.0,
            'z':  NaoSoccerSimParam['GoalHeight']},

    'G2L' : {'x': NaoSoccerSimParam['FieldLength']/2.0,
            'y':  NaoSoccerSimParam['GoalWidth']/2.0,
            'z':  NaoSoccerSimParam['GoalHeight']},

    'G1R' : {'x': -NaoSoccerSimParam['FieldLength']/2.0,
            'y':  -NaoSoccerSimParam['GoalWidth']/2.0,
            'z':  NaoSoccerSimParam['GoalHeight']},

    'G2R' : {'x': -NaoSoccerSimParam['FieldLength']/2.0,
            'y':  NaoSoccerSimParam['GoalWidth']/2.0,
            'z':  NaoSoccerSimParam['GoalHeight']}
}

Loction = {
    'HeadLocation'  :   {},             #Global coordinate Head  Location
    # 'TorseLocation' :   {},             #Global coordinate Torse Location
    'BallLocation'  :   {'BallLocation'        :  {'x':1,'y':2,'z':3},#NaoRobot.vision.getBallLocation(),
                         'BallLocationToTorse' :  {'x':1,'y':2,'z':3},
                         'BallLocationToHead'  :  {'x':1,'y':2,'z':3},
                         'BallPredictLocation' :  {'x':1,'y':2,'z':3}
                         },
    'CachBallLocation' : {
                            'x':-NaoSoccerSimParam['FieldLength']/2.0
                            },          #截球点
    'KickBallLocation' :1,              #开球点
    'ProtectedLocation' :2,
    'TorseLocation'     :3,
    'LastTorseLocation' :4,
    'PlayerSeeInfoLocation' : {'Head'           :  {'x':1,'y':2,'z':3},
                               'HeadToGlobal'   : {'x':1,'y':2,'z':3},

                               'Arm'   :  {'RLOWER':{ 'x':1,'y':2,'z':3},
                                           'LLOWER':{'x':1,'y':2,'z':3},
                                           'RHight':{ 'x':1,'y':2,'z':3},
                                           'LHight':{'x':1,'y':2,'z':3}},

                               'Foot'  :  {'R':{ 'x':1,'y':2,'z':3},
                                           'L':{'x':1,'y':2,'z':3}},

                               'Time'  :  {'RLOWERARM' : float,
                                           'LLOWERARM' : float,
                                           'RFOOT'     : float,
                                           'LFOOT'     : float,
                                           'CHANGETIME': float,                 #通过视觉任何一个地方可能改变的时间
                                           'HEARTIME'  : float                  #通过听觉接收到的消息
                                           }

                               }
}

# mytest = Loction['PlayerSeeInfoLocation']
# print(mytest['Head']['x'])
# # print(Flag['F1L']['x']+Flag['F2L']['x'])

class World(object):
    def __init__(self):
        pass
    def getDirectionOfOpponentGoal(self,Playername):                   #对手面对目标的方向
        pass
    def otherTeamMateCloserToBall(self):
        pass
    def otherTeamMateCloserTo(self):
        pass

    # def getFieldLength(self):
    #     return NaoSoccerSimParam['FieldLength']
    # def getFieldWidth(self):
    #     return NaoSoccerSimParam['FieldWidth']
    # def getFielfHieht(self):
    #     return NaoSoccerSimParam['FieldHeight']

    # def getGoalHeight(self):
    #     return NaoSoccerSimParam['GoalHeight']
    # def getGoalWidth(self):
    #     return NaoSoccerSimParam['GoalWidth']
    # def getGoalDepth(self):
    #     return NaoSoccerSimParam['GoalDepth']

    # def getGoalKickDist(self):
    #     return NaoSoccerSimParam['GoalKickDist']
    #
    # def getFreeKickDistance(self):
    #     return NaoSoccerSimParam['FreeKickDistance']
    #
    # def getFreeKickMoveDistance(self):
    #     return NaoSoccerSimParam['FreeKickMoveDist']

    def getField(Field):
        return {
            'FieldLength' : NaoSoccerSimParam['FieldLength'],
            'FieldWidth'  : NaoSoccerSimParam['FieldWidth'],
            'FieldHeight' : NaoSoccerSimParam['FieldHeight']
        }

    def getGoal(Goal):
        return {
            'GoalHeight' : NaoSoccerSimParam['GoalHeight'],
            'GoalWidth'  : NaoSoccerSimParam['GoalWidth'],
            'GoalDepth'  : NaoSoccerSimParam['GoalDepth']
        }

    def getPenalty(Penalty):
        return {
            'PenaltyLength' : NaoSoccerSimParam['PenaltyLength'],
            'PenaltyWidth'  : NaoSoccerSimParam['PenaltyWidth']
            }
    def getBall(Ball):
        return {
            'BallRadius' : NaoSoccerSimParam['BallRadius'],
            'BallMass'   : NaoSoccerSimParam['BallMass']
            }


    def getTime(TimeTypeName):
        return {
            'WaitBeforeKickOff':NaoSoccerSimParam['WaitBeforeKickOff'],                  #写到这才发现switch问题，and要用这种格式重写world吗？算了，懒才不要
            'NotStandingMaxTime':NaoSoccerSimParam['NotStandingMaxTime'],
            'GoalieNotStandingMaxTime':NaoSoccerSimParam['GoalieNotStandingMaxTime']
        }

    def getDistance(DistanceTypeName):
        return {
            'MaxPlayersInsideOwnArea' : NaoSoccerSimParam['MaxPlayersInsideOwnArea'],
            'MinOppDistance'   :  NaoSoccerSimParam['MinOppDistance'],
            'Min2OppDistance'  :  NaoSoccerSimParam['Min2OppDistance'],
            'Min3OppDistance'  :  NaoSoccerSimParam['Min3OppDistance'],

            'GoalKickDist'     :  NaoSoccerSimParam['GoalKickDist'],
            'FreeKickMoveDistance' : NaoSoccerSimParam['FreeKickMoveDist'],
            'FreeKickDistance' :  NaoSoccerSimParam['FreeKickDistance']
        }




    #有时间还是重写一下把，这样写出来的话运行效率肯定比较低,最好这样：
    #def f(x):
    #   return {
    #               'tmie': 1,
    #               'dis' : 2
    #   }
    #但是这样写应该也有好处，将数据和方法分开了


class Parse(object):
    def __init__(self):
        pass



def PolAngle(x,y,z):            #原函数使用的是1e-5
    pol = {'x':float,'y':float,'z':float}

    r = x
    theta = y
    phi = z

    m = r*r
    n = math.tan((theta+90)*math.pi/180)
    p = math.tan((phi)*math.pi/180)

    if (math.fabs(theta) <= (1*math.e-9)) or math.fabs(theta+180) <= (1*math.e-9) :
        tmp = m/(1+p*p)

        pol['x'] = 0.0
        pol['y'] = math.sqrt(tmp)
        pol['z'] = math.sqrt(p*p*tmp)

        realTheta = NormalizedAngle(theta + 90)

        if math.fabs(realTheta) <= (1*math.e-9) :
            pol['y'] = (-pol['y'])
        if math.fabs(p) <= (1*math.e-9):
            pol['z'] = (-pol['z'])
    else:
        if math.fabs(phi-90) <= (math.e-9):
            pol['x'] = pol['y'] = 0.0
            pol['z'] = r
        elif math.fabs(phi+90) <= (math.e-9):
            pol['x'] = pol['y'] = 0.0
            pol['z'] = (-r)

        else:
            a = b = c = 0.0
            if math.fabs(p) <= (math.e-9):
                pol['z'] = 0.0
            else:
                c = m / (1+1.0/p/p)
                pol['z'] = math.sqrt(c)
                if math.fabs(p) <= (math.e-9):
                    pol['z'] = (-pol['z'])

            a = (m-c)/(1+n*n)
            b = n*n*a

            pol['x'] = math.sqrt(a)
            pol['y'] = math.sqrt(b)

            realTheta = NormalizedAngle(theta+90)

            if math.fabs(realTheta) <= (math.e-9):
                pol['y'] = (-pol['y'])
            if realTheta <= -90 or realTheta >=90:
                pol['x'] = (-pol['x'])
    temp = pol['x']
    pol['x'] = pol['y']
    pol['y'] = -temp

    return pol


def NormalizedAngle(Theta):
    while Theta >= 180:
        Theta = Theta -360
    while Theta <= -180:
        Theta = Theta + 360
    return Theta


# sd = {'x':1,'y':9}
# ss = (-sd['y'])
# print(sd)
