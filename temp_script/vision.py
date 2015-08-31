__author__ = 'king'
"""
class Vision(object):                   #版本１
    # Class that Robot Agent Can See Something And To Localize itself
    def __init__(self,name):
        self.name = name
        # self.Location = np.zeros((8,3),dtype=np.float)          #F1L,F2L,F1R,F2R,G1L,G2L,G1R,G2R但是不确定会传来几个标杆，这不对
                                                                #(F1L (<distance> <angle1> <angle2>
        self.F1L = np.zeros(3,dtype=np.float)
        self.F2L = np.zeros(3,dtype=np.float)
        self.F1R = np.zeros(3,dtype=np.float)
        self.F2R = np.zeros(3,dtype=np.float)
        self.G1L = np.zeros(3,dtype=np.float)
        self.G2L = np.zeros(3,dtype=np.float)
        self.G1R = np.zeros(3,dtype=np.float)
        self.G2R = np.zeros(3,dtype=np.float)

        self.BallLocation = np.zeros(3,dtype=np.float)
        self.OtherPlayerLocation = np.zeros(3,dtype=np.float)                #(p (team Robolog) (id 1) (pol x,y,z))
        self.OtherPlayerId = ""                                              #先以字符串形式接收过来，然后用一个字符转int的函数转回来
        self.OtherPlayerTeamName = ""

        self.isMyTeam = True
        self.isMyEnmy = True
    # 或许应该将写成np.zeros((11,dtype=np.float))
    # 或许应该将

    def getMyLocation(self):
        return Localizer.__init__()                                                                #想想怎么用卡尔曼滤波来写？

    def getOtherPlayerLocation(self):
        return self.OtherPlayerLocation

    def getBallPostion(self):
        return self.BallLocation

    def getOtherPlayerType(self):

        if self.OtherPlayerTeamName == NaoRobot.teamname:
            return self.isMyTeam
        else:
            return self.isMyEnmy

    def getOtherPlayerInfo(self):
        return self.OtherPlayerTeamName,self.OtherPlayerLocation,self.OtherPlayerId         #hehe switch

    def getDirections(self):
        pass

# =========================================================================== #

class Localizer(Vision):
    def __init__(self):    #KalManLocalizer
        pass

"""