from Agent import *
from Action import *
from enum import Enum



FallDirection = Enum('Not_FALLING','FALL_TO_FRONT','FALL_TO_LEFT','FALL_TO_RIGHT')


class Localizer(object):                    #已经找到robotkalmanfilter，不用自己写了,先去看看
    def UpdateBallLocation(self):
        pass


class Think(object):
    def __init__(self):
        pass
    def WhereToLook(self):
        pass
    def WhereToWalk(self):
        pass
    def WhereToRun(self):
        pass
    def WhereToKick(self):
        pass
    def HowToLook(self):
        pass
    def HowToWalk(self):
        pass
    def HowToRun(self):
        pass
    def HowToKick(self):
        pass
    def HowToAttack(self):
        pass
    def HowToDefend(self):
        pass
