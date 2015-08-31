"""
一共有五种NAO，采取这种写法是为了将每种类型的进行独立控制，这个是上下倾斜快，关节转动慢的
#faster ankle-pitch and slower ankle-roll speed Nao
{
    'Hip1RelTorso_X' => 0.055,
    'Hip1RelTorso_Z' => -0.115,
    'ThighRelHip2_Z' => -0.04,
    'AnkleRelShank_Z' => -0.055,
    'lj5_max_abs_speed' => 8.80667,
    'lj6_max_abs_speed' => 3.47234,
    'ElbowRelUpperArm_Y' => 0.07,
    'UseToe' => 'false'
}
"""


from Agent import *
from Action import *
from Think import *

class Nao２(NaoRobot):                    #faster ankle-pitch and slower ankle-roll speed Nao
    def __init__(self,agetID,teamname,startCoordinates=[]):
        NaoRobot.__init__(agentID=self.agentID, teamname=self.teamname, host='localhost', port=3100, model='rsg/agent/nao/nao_hetero.rsg 2', debugLevel=0,startCoordinates=self.startCoordinates)

    def Action(self):
        NaoAction = MyNao2Action

class MyNao2Action(Action):
    def __init__(self):
        pass
