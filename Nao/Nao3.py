"""
这个不仅是长胳膊长腿还是大屁股的
longer legs and arms + wider hip Nao
{
    'Hip1RelTorso_X' => 0.072954143,
    'Hip1RelTorso_Z' => -0.115,
    'ThighRelHip2_Z' => -0.067868424,
    'AnkleRelShank_Z' => -0.082868424,
    'lj5_max_abs_speed' => 6.1395,
    'lj6_max_abs_speed' => 6.1395,
    'ElbowRelUpperArm_Y' => 0.125736848,
    'UseToe' => 'false'
}
"""


from Agent import *
from Action import *
from Think import *

class Nao3(NaoRobot):                    #longer legs and arms + wider hip Nao
    def __init__(self,agetID,teamname,startCoordinates=[]):
        NaoRobot.__init__(agentID=self.agentID, teamname=self.teamname, host='localhost', port=3100, model='rsg/agent/nao/nao_hetero.rsg 3', debugLevel=0,startCoordinates=self.startCoordinates)
    def Action(self):
        NaoAction = MyNao3Action

class MyNao3Action(Action):
    def __init__(self):
        pass