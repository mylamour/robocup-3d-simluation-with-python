"""
一共有五种NAO，采取这种写法是为了将每种类型的进行独立控制，这个是长胳膊长腿的
#This is a Long legs and arms Nao
{
    'Hip1RelTorso_X' => 0.055,
    'Hip1RelTorso_Z' => -0.115,
    'ThighRelHip2_Z' => -0.05832,
    'AnkleRelShank_Z' => -0.07332,
    'lj5_max_abs_speed' => 6.1395,
    'lj6_max_abs_speed' => 6.1395,
    'ElbowRelUpperArm_Y' => 0.10664,
    'UseToe' => 'false'
}
"""

from Agent import *
from Action import *
from Think import *

class Nao1(NaoRobot):                    #Long legs and arms Nao
    def __init__(self,agetID,teamname,startCoordinates=[]):
        NaoRobot.__init__(agentID=self.agentID, teamname=self.teamname, host='localhost', port=3100, model='rsg/agent/nao/nao_hetero.rsg 1', debugLevel=0,startCoordinates=self.startCoordinates)
    def Action(self):
        NaoAction = MyNao1Action

class MyNao1Action(Action):
    def __init__(self):
        pass
