"""
有脚趾的一类
Nao Toes Model
{
    'Hip1RelTorso_X' => 0.055,
    'Hip1RelTorso_Z' => -0.115,
    'ThighRelHip2_Z' => -0.04,
    'AnkleRelShank_Z' => -0.055,
    'lj5_max_abs_speed' => 6.1395,
    'lj6_max_abs_speed' => 6.1395,
    'ElbowRelUpperArm_Y' => 0.07,
    'UseToe' => 'true',
    'ToeLength' => 0.035517656
}
"""

from Agent import *
from Action import *
from Think import *

class Nao4(NaoRobot):                    # Nao toe
    def __init__(self,agetID,teamname,startCoordinates=[]):
        NaoRobot.__init__(agentID=self.agentID, teamname=self.teamname, host='localhost', port=3100, model='rsg/agent/nao/nao_hetero.rsg 4', debugLevel=0,startCoordinates=self.startCoordinates)

    def Action(self):
        NaoAction = MyNao4Action

class MyNao4Action(Action):                                                     #针对kick和walk的不同角度
    def __init__(self):
        pass