#! /usr/bin/env python3


import sys, time, math
import threading
import socket, struct
import numpy as np
from collections import deque
from World import *


# ============================================================================ #

# Constants
CYCLE_LENGTH = 0.02 # cycle length in seconds

# ============================================================================ #

class PNS(object):
    """Peripheral nervous system
    周围神经系统
    Creates socket connections to the simulation server.
    创建套接字连接到仿真服务器
    Sends effector messages.
    发送效应器消息
    Receives perceptor messages.
    接受感知器消息
    Upon creation the agent is registered with the server.
    一旦创建智能体，就向服务器注册
    """
    def __init__(self, agentID, teamname, host='localhost', port=3100,
            model='', debugLevel=10):

        """='rsg/agent/nao/nao.rsg'
        other model:(scene rsg/agent/nao/nao_hetero.rsg 0)
        (scene rsg/agent/nao/nao_hetero.rsg 1)
        (scene rsg/agent/nao/nao_hetero.rsg 2)
        (scene rsg/agent/nao/nao_hetero.rsg 3)
        (scene rsg/agent/nao/nao_hetero.rsg 4)
        :rtype : object
        """
        self.agentID    = agentID
        self.teamname   = teamname
        self.host       = host
        self.port       = port
        self.model      = model
        self.debugLevel = debugLevel

        # create socket and connect to simulation server
        #创建并连接到仿真服务器
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        # create and initialize agent
        #创建并初始化一个智能体
        self._send_effector('(scene {})'.format(self.model))
        self.receive_perceptors()
        self._send_effector('(init (unum {})(teamname {}))'.format(self.agentID, self.teamname))
        self.receive_perceptors()

# ==================================== #

    def _send_effector(self, message):
        """Each message is prefixed with the length of the payload message.
        每个消息命令都有一个前缀标识
        The length prefix is a 32 bit unsigned integer in network order
        这个在网络命令中的前缀标识是一个32位无符号整形
        """

        # report message
        if (self.debugLevel >= 10):
            print("S:", message)

        # convert message to ASCII encoded byte string
        length   = len(message)
        bmessage = bytes(message, 'ASCII')

        # send length of message
        lengthMessage = struct.pack("!I", length)
        bytesSent = 0
        while (bytesSent < 4):
            bytesSent += self.socket.send(lengthMessage[bytesSent:])

        # send actual message
        bytesSent = 0
        while (bytesSent < length):
            bytesSent += self.socket.send(bmessage[bytesSent:])

# ==================================== #

    def receive_perceptors(self):

        # receive length of the message (4 bytes)
        length = self._receive_message(4)
        length = struct.unpack("!I", length)[0]

        # receive actual message
        perceptors = self._receive_message(length)
        perceptors = str(perceptors, 'ASCII')

        return self._parse_perceptors(perceptors)
    
# ==================================== #

    def _receive_message(self, length):
        """Receive a message from server communication socket of given length
        经由套接字从服务器接收消息"""

        message = b''
        while (len(message) < length):
            nextBytes = self.socket.recv(length - len(message))
            if (nextBytes == ''):
                raise OSError('Socket to simulation server was closed')
            else:
                message += nextBytes
 
        return message

# ==================================== #

    def _parse_perceptors(self, perceptors):
        """Minimal parsing of perceptor message.
        Convert message to nested python lists, substituting '[' and ']'
        for '(' and ')'
        解析感知器信息，并存储到列表中--->把()内的内容转换为嵌套式的列表
        """

        return self.__str2list(perceptors)

#这个写的是真棒，所有东西最核心基础的地方
# ==================================== #

    def __str2list(self, string):
        """Convert a string to a (nested) python list, substituting '[' and ']'
        for '(' and ')'
        用列表存储接收到的字符串
        """
        
        l     = []
        bra   = '('
        ket   = ')'
        space = ' '
        nbra  = 0 # number of '('       左括号的数量
        nket  = 0 # number of ')'       右括号的数量

        nonword = [space, bra, ket]

        # begin and end indices of new sublist　　开始到结束之间一共有多少子表
        begin = 0
        end   = 0

        prevc = ''
        for i, c in enumerate(string):

            # detect word beginnings    探测开始字符
            if (i == 0 and c != bra):
                begin = i
            elif (nbra == 0 and c not in nonword and (prevc == bra or prevc == space)):
                begin = i

            # detect beginning of new nested list　　探测嵌入列表  (gyr (n torse) (pol x y z))
            elif (c == bra and nbra == nket):
                begin = i+1
            elif (c == ket and nbra == nket+1):
                end = i
                l.append(self.__str2list(string[begin:end]))

            # detect word endings       探测结束字符
            if (i == len(string)-1 and c != ket):
                word = string[begin:]
                try: word = int(word)
                except:
                    try: word = float(word)
                    except: pass
                l.append(word)
            if (c == space and nbra == 0 and prevc not in nonword):
                end = i
                word = string[begin:end]
                try: word = int(word)
                except:
                    try: word = float(word)
                    except: pass 
                l.append(word)
 

            if (c == bra): nbra += 1
            if (c == ket): nket += 1

            prevc = c
                
        # return
        if len(l) == 1:
            return l[0]
        else:
            return l

# ==================================== #

    def hinge_joint_effector(self, name, rate):
        """Set the change rate in degree/cycle of the
        hinge joint with the provided name
        铰链关节效应器：通过提供关节名字，发送每周期的角速度的改变
        """
        message = "({} {:.2f})".format(name, rate)
        self._send_effector(message)

# ==================================== #

    def universal_joint_effector(self, name, rate1, rate2):
        """Set the change rate in degree/cycle of axis 1 and 2 of the
        普通关节的改变
        hinge joint with the provided name"""
        message = "({} {:.2f} {:.2f})".format(name, rate1, rate2)
        self._send_effector(message)

# ==================================== #

    def beam_effector(self, x, y, rotation):
        """Position the player on the field before the game starts
        and after a goal was scored.
        在比赛前和一方得分后初始化球员的位置
        Position and orientation of the team playing from right to left is
        point reflected at the center point.
        从右方到左方的球队的位置和方向反射自中心点
        x, y        Coordinates
        rotation旋转    horizontal orientation（水平方向） with respect to x-axis in degree"""
        message = "(beam {:.2f} {:.2f} {:.2f})".format(x, y, rotation)
        self._send_effector(message)

# ==================================== #

    def say_effector(self, message):
        """Broadcast a message to other agents.
        广播一个消息给其他智能体
        At most 20 ASCII characters are allowed
        最多20个字符
        white space and normal brackets are prohibited.
        空格和方括号是被禁止的（防注入?）"""
        if len(message) > 20:
            message = message[:20]
        for c in message:
            if (c == ' ' or c == '(' or c == ')'):
                print("Character not allowed for say effector: '{}'".format(c))
                print("Nothing sent.")
                return
        message = "(say {})".format(message)
        self._send_effector(message)
 

# ============================================================================ #

# ============================================================================= #
class MovementScheduler(deque):
    """A queue for scheduling robot movements.
    动作调度： 用一个队列储存调度机器人的动作参数
    It guarantees that each function is scheduled only once at a time
    这确保它的每个功能都只能被调度一次
    to prevent conflicts with the potential of deadlocking the bot
    这阻止了潜在的死锁可能（为什么呢？参照事务～）"""

    def append(self, newitem):
        """The first element（元素） in the newitem list must be a function that gets called
        repeatedly until it returns 'done'.
        新指令(list)中的第一个元素是一个函数，可重复调用直到它返回‘done'
        The second element is a dictionary that contains the keyword arguments passed to the function.
         第二个元素是一个字典（包含了动作的关键参数），传递参数给函数
         The third item is optional and should contain a list (as the  simplest mutable datatype)
        whose zeroth element is set to true once the function contains 'done'
        to signal completion.
        第三部分是的参数是可选择的，它应该包含一个列表（简单易变的数据类型），包含一个确认指令（done）
        """
        # check proper format of item first 检查格式是否正确
        if not type(newitem) == list:
            raise QueueItemError("MovementQueue items must be lists.")
        elif not (len(newitem) == 2 or len(newitem) == 3):
            raise QueueItemError("MovementQueue items must be of format: [<function>, <kwargs dict>, <list>].")
        elif len(newitem) == 3 and type(newitem[2]) != list:
            raise QueueItemError("Third (optional) item to MovementQueue entries must be a list.")
        elif not callable(newitem[0]):
            raise QueueItemError("First item in list must be a function.")
        elif not type(newitem[1]) == dict:
            raise QueueItemError("MovementQueue items must be of format: [<function>, <kwargs dict>, <list>].")

        for item in self:
            function      = item[0]
            dictionary    = item[1]
            newFunction   = newitem[0]
            newDictionary = newitem[1]
            if function == newFunction:
                try:
                    if dictionary['hj'] == newDictionary['hj']:
                        # two functions operating on the same hj not allowed
                        #两个函数都是操控同一个铰链关节是不允许的。（假如在多线程的情况下是不是可以？，难道非要把一整套的关节弄好输入到新的字典中？
                        raise SchedulerConflict('The function "{}" is already in the queue.'.format(item[0]))
                except KeyError:
                    SchedulerConflict.resue_socket_addr(host=3100)
                    #pass这并不是同用一个端口造成的，所有这个异常写的没有用



        super().append(newitem) 

# ==================================== #

    def run(self):
        """Execute all functions currently in msched
        Reschedule if they are not done"""

        for i in range(len(self)):
            item     = self.popleft()
            function = item[0]
            argDict  = item[1]

            returnVal = function(**argDict)

            if returnVal != "done":
                self.append(item)
            elif len(item) == 3:
                item[2][0] = True


# ============================================================================ #
# General Perceptors :
                        # GyroRate Perceptor                  √
                        # HingeJoint Perceptor                √
                        # UniversalJoint Perceptor          --need--
                        # Touch Perceptor                   --need--
                        # ForceResistance Perceptor           √
                        # Accelerometer                       √



class GameState(object):
    """Store game state information"""

    def __init__(self, time=0.0, gametime=0.0, scoreLeft=0, scoreRight=0,
            playmode='BeforeKickOff'):
        self.time       = time
        self.gametime   = gametime
        self.scoreLeft  = scoreLeft
        self.scoreRight = scoreRight
        self.playmode   = playmode

# ==================================== #

    def set_time(self, time):
        self.time       = time
    def set_gametime(self, gametime):
        self.gametime   = gametime
    def set_scoreLeft(self, scoreLeft):
        self.scoreLeft  = scoreLeft
    def set_scoreRight(self, scoreRight):
        self.scoreRight = scoreRight
    def set_playmode(self, playmode):
        self.playmode   = playmode 

    def get_time(self):
        return self.time
    def get_gametime(self):
        return self.gametime
    def get_scoreLeft(self):
        return self.scoreLeft
    def get_scoreRight(self):
        return self.scoreRight
    def get_playmode(self):
        return self.playmode

# ==================================== #
    
    def __str__(self):
        string = ""
        string += "time       = {}\n".format(self.time      )
        string += "gametime   = {}\n".format(self.gametime  )
        string += "scoreLeft  = {}\n".format(self.scoreLeft )
        string += "scoreRight = {}\n".format(self.scoreRight)
        string += "playmode   = {}"  .format(self.playmode  )
        return string


# ============================================================================ #


class Gyroscope(object):
    """Gyroscope perceptor holding information about the change in
    陀螺仪感受器手机信息关于所有的改变
    orientation of a body with respect to the global coordinate system
    在身体和方向等方面的全局坐标系统
    The rate of change is measured in deg/s
    """

    def __init__(self, name):
        self.name = name
        self.rate = np.zeros(3, dtype=np.float)

        # unit vectors of body with respect to global coordinate system
        self.x = np.array([1.0, 0.0, 0.0])
        self.y = np.array([0.0, 1.0, 0.0])
        self.z = np.array([0.0, 0.0, 1.0])

    def set(self, rate):
        for i in range(3):
            self.rate[i] = rate[i]

        # rotation in degree during the last cycle
        rotationAngle = np.linalg.norm(self.rate) / (1.0/CYCLE_LENGTH) 

        # rotate local coordinate frame
        #使用local坐标系
        self.x = rotate_arbitrary(self.rate, self.x, angle=rotationAngle)
        self.y = rotate_arbitrary(self.rate, self.y, angle=rotationAngle)
        self.z = rotate_arbitrary(self.rate, self.z, angle=rotationAngle)

    def get_rate(self):
        return self.rate

    def get_orientation(self):
        return self.x, self.y, self.z
    

# ============================================================================ #


class Accelerometer(object):
    """Accelerometer to measure the acceleration relative to free fall
    Will therefore indicate 1g = 9.81m/s at rest in positive z direction
    计算相对于自由落体的加速度，因此以9.81m/s 在z轴正方向
    """

    def __init__(self, name):
        self.name = name
        self.acceleration = np.zeros(3, dtype=np.float)

    def set(self, acceleration):
        for i in range(3):
            self.acceleration[i] = acceleration[i]
        self.acceleration[i] -= 9.81

    def get(self):
        return self.acceleration


# ============================================================================ #


class ForceResistanceSensor(object):
    """Sensor state of a Force resistance perceptor
    point is the point of origin of the force
    force is the force vector
    力量抵抗感知器：一个位于原点的力的向量"""

    def __init__(self, name):
        self.name  = name
        self.point = np.zeros(3, dtype=np.float)
        self.force = np.zeros(3, dtype=np.float)

    def set(self, point, force):
        """Set the point of origin and the force
        Any 3 dimensional object that holds data convertible to float is valid
        设置原点和力，任何三维物体将数值转换为浮点型是有效的"""
        for i in range(3):
            self.point[i] = point[i]
            self.force[i] = force[i]

    def get_point(self):
        """get the point of origin coordinates
        得到原点坐标"""
        return self.point

    def get_force(self):
        """get the force vector"""
        return self.force

# ============================================================================ #
# 连个Vision都没有，玩你妹╮（╯＿╰）╭　
#  Soccer Perceptors:
                                    # Vision Perceptor          --need--        √ 2015/8/24
                                    # GameState Perceptor         √
                                    # Hear Perceptor           --need--
                                    # AgentState Perceptor     --need--         server 没有开启充电这一块的功能

# ============================================================================ #
#[name,[x,y,z]]
class Vision(object):
    def __init__(self,name):
        self.name = name
        self.flag= np.zeros(3, dtype=np.float)
        self.ballLocation = np.zeros(3, dtype=np.float)
        self.playerLocation = np.zeros(3, dtype=np.float)
        self.teamname = ''
        self.playerid = ''
        self.playerinfo = {'teamname':self.teamname,
                           'id':self.playerid,
                           'location' :self.playerLocation }

    def setMyFlag(self,hflag):
        for i in range(3):
            # self.flag[i] = flag
            self.flag = hflag
    def setBallLocation(self,ball):
        for i in range(3):
            self.ballLocation = ball

    def setPlayerLocation(self,hplayerLocation):
        for i in range(3):
            self.playerLocation = hplayerLocation

    def setPlayerId(self,unid):
        self.playerid = unid

    def setTeamname(self,unname):
        self.teamname = unname

    def getPlayerInfo(self):
        return self.playerinfo
    def getFlagLocation(self):
        return  self.flag
    def getBallLocation(self):
        return self.ballLocation
    def getPlayerLocation(self):
        return self.playerLocation
# =========================================================================== #

"""Actually the underlying model stems from the 2D Soccer Simulation and has been
integrated in the 3D simulator since server version 0.4."""

# (hear <time> ’self’|<direction> <message>)        ASCII[32-126] 20byter
#每个player每0.4s最多只能传递一条，并且不能对手也能听到
#这属于对未知数据进行划分，猜测和预测，是不是属于高级的机器学习算法呢？想想都和激动呢～～～
#思路：选取特征码，and不会了

class Hear(object):
    def __init__(self):
        pass


class NaoRobot(object):
    """Class that represents the Nao Soccer Robot
    机器人的实现"""

    def __init__(self, agentID, teamname, host='localhost', port=3100, model='', debugLevel=0,
            startCoordinates=[-0.5, 0, 0]): 

        self.agentID       = agentID
        self.teamname      = teamname
        self.host          = host
        self.port          = port
        self.model         = model
        self.debugLevel    = debugLevel
        self.alive         = False
        self.realstarttime = None # starttime of robot
        self.simstarttime  = None 

        # set maximum hinge effector speed
        self.maxhjSpeed = 7.035

        # movement schedule
        # each sublist should contain a function object and
        # a dictionary of keyword arguments
        #每个调度表应该包含一个函数对象和一个关键参数的字典
        # e.g. [foo, {'kw1': val1, 'kw2', val2}]
        # the function will be executed until it returns "done"
        self.msched     = MovementScheduler()

        # games state information
        self.gamestate  = GameState()

        # gyroscope and accelerometer
        self.gyr        = Gyroscope    ('torso')
        self.acc        = Accelerometer('torso')

        # self.see        = Vision('F1L')               应该枚举一下，或者字典类型？　　　for flag in itemuarter ,return
        # self.see        =[Vision('F1L'),Vision('F2L'),Vision('F1R'),Vision('F2R'),Vision('G1L'),Vision('G2L'),Vision('G1R'),Vision('G2R'),Vision('B'),Vision('team'),Vision('id')]


        # hinge joint perceptor states
        #对应的三种状态，左右摇摆，上下倾斜，沿轴转动
        self.hj         = {'hj1' : 0.0,         #Neck Yaw   脖子左右摇摆
                           'hj2' : 0.0,         #Neck Pitch    脖子上下倾斜
                           'raj1': 0.0,         #Right Shoulder Pitch
                           'raj2': 0.0,         #Right Shoulder Yaw
                           'raj3': 0.0,         #Right Arm Roll
                           'raj4': 0.0,         #Right Arm Yaw
                           'laj1': 0.0,         #___Left Shoulder Pitch
                           'laj2': 0.0,         #___Left Shoulder Yaw
                           'laj3': 0.0,         #___Left Arm Roll
                           'laj4': 0.0,         #___Left Arm Yaw
                           'rlj1': 0.0,         #Right Hip YawPitch
                           'rlj2': 0.0,         #Right Hip Roll
                           'rlj3': 0.0,         #Right Hip Pitch
                           'rlj4': 0.0,         #Right Knee Pitch
                           'rlj5': 0.0,         #Right Foot Pitch
                           'rlj6': 0.0,         #Right Foot Roll
                           'llj1': 0.0,         #___Left Hip YawPitch
                           'llj2': 0.0,         #___Left Hip Roll
                           'llj3': 0.0,         #___Left Hip Pitch
                           'llj4': 0.0,         #___Left Knee Pitch
                           'llj5': 0.0,         #___Left Foot Pitch
                           'llj6': 0.0,}        #___Left Foot Roll

        # corresponding hinge joint effectors
        #铰链关节感受器与之对应的效应器
        self.hjEffector = {'hj1' : 'he1',
                           'hj2' : 'he2',
                           'raj1': 'rae1',
                           'raj2': 'rae2',
                           'raj3': 'rae3',
                           'raj4': 'rae4',
                           'laj1': 'lae1',
                           'laj2': 'lae2',
                           'laj3': 'lae3',
                           'laj4': 'lae4',
                           'rlj1': 'rle1',
                           'rlj2': 'rle2',
                           'rlj3': 'rle3',
                           'rlj4': 'rle4',
                           'rlj5': 'rle5',
                           'rlj6': 'rle6',
                           'llj1': 'lle1',
                           'llj2': 'lle2',
                           'llj3': 'lle3',
                           'llj4': 'lle4',
                           'llj5': 'lle5',
                           'llj6': 'lle6',} 

        # force resistance perceptors
        #力量抵抗感知器
        self.frp        = {'rf': ForceResistanceSensor('rf'),
                           'lf': ForceResistanceSensor('lf')}

        # =========================================================增加vision
        self.vision     = {
                            'F1L' : Vision('F1L'),
                            'F2L' : Vision('F2L'),
                            'F1R' : Vision('F1R'),
                            'F2R' : Vision('F2R'),
                            'G1L' : Vision('G1L'),
                            'G1R' : Vision('G1R'),
                            'G2L' : Vision('G2L'),
                            'G2R' : Vision('G2R'),
                            'B'   : Vision('B'),
                            'P'   : Vision('P'),
                            'id'  : Vision('id'),
                            'team': Vision('team')
                        }

        # =================================================================2015/8/24

        # hinge joint effector states
        #要明白一个关节转动之后对其他关节的带动及影响
        self.he         = {'he1' : 0.0,
                           'he2' : 0.0,
                           'rae1': 0.0,
                           'rae2': 0.0,
                           'rae3': 0.0,
                           'rae4': 0.0,
                           'lae1': 0.0,
                           'lae2': 0.0,
                           'lae3': 0.0,
                           'lae4': 0.0,
                           'rle1': 0.0,
                           'rle2': 0.0,
                           'rle3': 0.0,
                           'rle4': 0.0,
                           'rle5': 0.0,
                           'rle6': 0.0,
                           'lle1': 0.0,
                           'lle2': 0.0,
                           'lle3': 0.0,
                           'lle4': 0.0,
                           'lle5': 0.0,
                           'lle6': 0.0,} 


        # maxima of hinge joints
        self.hjMax      = {'hj1' :  120.0,
                           'hj2' :   45.0,
                           'raj1':  120.0,
                           'raj2':    1.0,
                           'raj3':  120.0,
                           'raj4':   90.0,
                           'laj1':  120.0,
                           'laj2':   95.0,
                           'laj3':  120.0,
                           'laj4':    1.0,
                           'rlj1':    1.0,
                           'rlj2':   25.0,
                           'rlj3':  100.0,
                           'rlj4':    1.0,
                           'rlj5':   75.0,
                           'rlj6':   45.0,
                           'llj1':    1.0,
                           'llj2':   45.0,
                           'llj3':  100.0,
                           'llj4':    1.0,
                           'llj5':   75.0,
                           'llj6':   25.0,} 

        # minima of hinge joints
        self.hjMin      = {'hj1' : -120.0,
                           'hj2' :  -45.0,
                           'raj1': -120.0,
                           'raj2':  -95.0,
                           'raj3': -120.0,
                           'raj4':   -1.0,
                           'laj1': -120.0,
                           'laj2':   -1.0,
                           'laj3': -120.0,
                           'laj4':  -90.0,
                           'rlj1':  -90.0,
                           'rlj2':  -45.0,
                           'rlj3':  -25.0,
                           'rlj4': -130.0,
                           'rlj5':  -45.0,
                           'rlj6':  -25.0,
                           'llj1':  -90.0,
                           'llj2':  -25.0,
                           'llj3':  -25.0,
                           'llj4': -130.0,
                           'llj5':  -45.0,
                           'llj6':  -45.0,}  

        # defaults (starting positions) of hinge joints in percent
        self.hjDefault  = {'hj1' : 0.0,
                           'hj2' : 0.0,
                           'raj1': 0.0,
                           'raj2': 0.0,
                           'raj3': 0.0,
                           'raj4': 0.0,
                           'laj1': 0.0,
                           'laj2': 0.0,
                           'laj3': 0.0,
                           'laj4': 0.0,
                           'rlj1': 0.0,
                           'rlj2': 0.0,
                           'rlj3': 0.0,
                           'rlj4': 0.0,
                           'rlj5': 0.0,
                           'rlj6': 0.0,
                           'llj1': 0.0,
                           'llj2': 0.0,
                           'llj3': 0.0,
                           'llj4': 0.0,
                           'llj5': 0.0,
                           'llj6': 0.0,}




 
        # create peripheral nervous system (server communication)
        #创建PNS
        #def __init__(self, agentID, teamname, host='localhost', port=3100,
        #    model='rsg/agent/nao/nao.rsg', debugLevel=10):

        self.pns = PNS(self.agentID, self.teamname,
                host=self.host, port=self.port, model=self.model, debugLevel=self.debugLevel)
        #因为球员平台对类型的要求较多，所以，需要修改model作为参数传入
        self.perceive()
        self.pns.beam_effector(startCoordinates[0], startCoordinates[1], startCoordinates[2])

        # set default hing joint angles设置默认的铰链关节角度
        for hj in self.hjDefault.keys():
            self.hjDefault[hj] = self.get_hj(hj)

        self.lifeThread = threading.Thread(target=self.live)                #难道要直接在类里面使用？
        self.lifeThread.start()

        #percent的存在使得对不同球员来讲，调好一个智能体的角度之后，可以使用其百分比应用于不同类型
        # put arms down
       # self.msched.append([self.move_hj_to, {'hj': 'raj1', 'speed': 25, 'percent': 10}])
       # self.msched.append([self.move_hj_to, {'hj': 'laj1', 'speed': 25, 'percent': 10}])


# ==================================== #

    def live(self):
        """Start the robot"""

        # only one live thread allowed!
        #只允许有一个活动线程，所以说，如何使用多线程？？
        if self.alive:
            return

        self.alive = True

        startSkippingNumber = 10

        iteration         = -1
        skippedIterations =  0
        while self.alive:
            iteration += 1

            if self.check_sync() >= startSkippingNumber:
                while self.check_sync() > 2:
#                    print(self.check_sync())
                    self.perceive(skip=True)
                    iteration         += 1
                    skippedIterations += 1 

            self.perceive()
            self.msched.run()


            if iteration * CYCLE_LENGTH % 3.0 == 0:
#                print("Robot {} lags {} cycles behind after {} iterations".format(self.agentID, self.check_sync(), iteration+1))
                print("gametime - realtime: {:.5f}".format(self.gamestate.get_gametime() - time.time()))


        # report statistics
        iterations = iteration + 1
        print("Robot {} lived for {:.1f} seconds,\n\ti.e. {} iterations, {} of which have been skipped ({:.2f}%).".format(self.agentID, time.time()-self.realstarttime, iterations, skippedIterations, 100.0*skippedIterations/iterations))


# ==================================== #

    def die(self, timeout=0):
        """Stop robot execution and close socket connection to server
        If timeout is > 0, give the robot some time to finish scheduled movements.
        如果超时，则给机器人一些时间去结束动作调度"""
        start    = time.time()
        timeleft = timeout - time.time() + start
        while timeleft > 0:
            if len(self.msched) == 0:
                self.alive = False
                break
            timeleft = timeout - time.time() + start
        self.alive = False
        self.lifeThread.join()
        self.pns.socket.close()

# ==================================== #

    def perceive(self, skip=False):
        """Receive perceptor information from server and
        update status accordingly
        根据从服务器接收到的感知信息更新自身状态"""

#        start = time.time()
        perceptors = self.pns.receive_perceptors()
#        print("receive_perceptors() took {:.8f} sec.".format(time.time()-start))

        for perceptor in perceptors:

            # time
            if perceptor[0] == 'time':
                self.gamestate.set_time(perceptor[1][1])
                if self.realstarttime == None:
                    self.realstarttime = time.time()                #真时的时间
                    self.simstarttime  = self.gamestate.get_time()  #仿真服务器的时间
                if skip:
                    break

            # game state
            elif perceptor[0] == 'GS':
                for field in perceptor[1:]:
                    if field[0] == 'sl':                            #我是左边开球
                        self.gamestate.set_scoreLeft(field[1])      #我是右边开球
                    elif field[0] == 'sr':
                        self.gamestate.set_scoreRight(field[1])
                    elif field[0] == 't':
                        self.gamestate.set_gametime(field[1])
                    elif field[0] == 'pm':
                        self.gamestate.set_playmode(field[1])

            # gyroscope
            elif perceptor[0] == 'GYR':
                self.gyr.set(perceptor[2][1:])

            # set accelerometer
            elif perceptor[0] == 'ACC':
                self.acc.set(perceptor[2][1:])

            # vision information
            elif perceptor[0] == 'See':
                # pass
                # 添加vision,由于前面是使用字典进行解析的，所以不能使用类似这种格式，self.vision['f1l'].setflag(xxx),擦，竟然又可以了，什么鬼
                #在这里指存储一遍，故不必设置成字典相对应
                for field in perceptor[1:]:
                    if field[0] == 'F1L':
                        # self.vision[perceptor[1][1]].setFlag(perceptor[2][1:])
                        #上面这种写法竟然是错的，虽然逻辑是相同的，但是提示unhashable list,don't know why
                        self.vision['F1L'].setFlag(perceptor[2][1:])
                    elif field[0] == 'F2L':
                        self.vision['F2L'].setMyFlag(perceptor[2][1:])
                        # self.vision[perceptor[1][1]].setMyFlag(perceptor[2][1:])
                    elif field[0] == 'F1R':
                        self.vision['F1R'].setMyFlag(perceptor[2][1:])
                        # self.vision[perceptor[1][1]].setMyFlag(perceptor[2][1:])
                    elif field[0] == 'F2R':
                        self.vision['F2R'].setMyFlag(perceptor[2][1:])
                        # self.vision[perceptor[1][1]].setMyFlag(perceptor[2][1:])
                    elif field[0] == 'G1L':
                        self.vision['G1L'].setMyFlag(perceptor[2][1:])
                        # self.vision[perceptor[1][1]].setMyFlag(perceptor[2][1:])
                    elif field[0] == 'G2L':
                        self.vision['G2L'].setMyFlag(perceptor[2][1:])
                        # self.vision[perceptor[1][1]].setMyFlag(perceptor[2][1:])
                    elif field[0] == 'G1R':
                        self.vision['G1R'].setMyFlag(perceptor[2][1:])
                        # self.vision[perceptor[1][1]].setMyFlag(perceptor[2][1:])
                    elif field[0] == 'G2R':
                        self.vision['G2R'].setMyFlag(perceptor[2][1:])
                        # self.vision[perceptor[1][1]].setMyFlag(perceptor[2][1:])
                    elif field[0] == 'B':
                        self.vision['B'].setMyFlag(perceptor[2][1:])
                        # self.vision[perceptor[1][1]].setBallLocation(perceptor[2][1:])

                    elif field[0] == 'team':
                        self.vision['team'].setTeamname(perceptor[2][1:])
                    elif field[0] == 'id':
                        self.vision['id'].setPlayerId(perceptor[2][1:])
                    # elif field[0] == 'P':
                    #     # if self.vision['P'].setPlayerLocation(perceptor[3][1:]) == None :
                    #     #     pass
                    #     # else:
                    #     print(self.vision['P'].setPlayerLocation(perceptor[4][1:]))

            #针对player这一块的信息解析来讲，是有问题的，幸好可以使用最后的排除方法。所以vison['p]标签本来是没什么用的及时解析到也没用，但可以用来存储player的位置信息
            #此处有错误，但不知问题出在哪里IndexError: list index out of range, 是不是因为没有player才导致呢？先注释掉试试



            # hinge joints
            elif perceptor[0] == 'HJ':
                self.hj[perceptor[1][1]] = perceptor[2][1]

            # force resistance perceptors
            elif perceptor[0] == 'FRP':
                self.frp[perceptor[1][1]].set(perceptor[2][1:], perceptor[3][1:])

            # unknown perceptor
            else:
                if self.debugLevel >= 10:
                    print("DEBUG: unknown perceptor: {}".format(perceptor[0]))
                    print(perceptor)
         
# ==================================== #

    def check_sync(self):
        """Check if perceived time is in sync with real time
        Return True if so, else False
        检查时间是否同步"""

        realruntime = time.time() - self.realstarttime
        simruntime  = self.gamestate.get_time() - self.simstarttime

        cycleDiff = int((realruntime - simruntime) / CYCLE_LENGTH)
        return cycleDiff

# ==================================== #

    def rock_hj(self, hj, speed, minAngle, maxAngle):
        """Rock a hinge joint at the given speed between min and max degrees"""

        he = self.hjEffector[hj]
        speed = abs(speed)

        if abs(self.he[he]) < speed:
            self.pns.hinge_joint_effector(he, speed)
            self.he[he] = speed

        if self.hj[hj] > maxAngle and self.he[he] > 0:
            self.pns.hinge_joint_effector(he, -speed)
            self.he[he] = -speed
        elif self.hj[hj] < minAngle and self.he[he] < 0:
            self.pns.hinge_joint_effector(he,  speed)
            self.he[he] =  speed

        return "not done"

# ==================================== #

#    move_hj_to:移动关节到特殊角
#    move_hj_by:通过特殊角移动关节

# +++++++++++++++++++++++++++++++++++++++ #
    def move_hj_to(self, hj, angle=None, percent=None, speed=25):
        """Move the given hinge joint to the specified angle
        移动铰链关节达到特殊的角度
        The angle can be given in degree (angle=<degree>)
        角度的格式可以是度数angle=<degree>或者是百分比，
        or percent (percent=<percentage>). If both are specified, the angle keyword
        gets priority.
        如果两者都是特殊的，将被指定优先级
        Speed is specified in percent of maximum speed"""

        # get corresponding hinge effector
        he = self.hjEffector[hj]

        if angle == None and percent == None:
            raise Exception("Either angle or percent must be specified in move_hj_to()")
        elif angle != None:
            # just to give angle keyword priority over percent
            pass
        else:
            angle = self.hjMin[hj] + percent/100.0*(self.hjMax[hj]-self.hjMin[hj])
        
        if   angle > self.hjMax[hj]: angle = self.hjMax[hj]
        elif angle < self.hjMin[hj]: angle = self.hjMin[hj]
        if   speed > 100: speed = 100.0                             #即便如此，我发现当每次speed为>100和>>100的时候，机器人的运转还是不一样的
        elif speed < 0:   speed = 0.0

        speed = speed/100.0 * self.maxhjSpeed
        accuracy = 0.1
        diff  = self.hj[hj] - angle

        if abs(diff) <= accuracy:
            self.pns.hinge_joint_effector(he, 0.0)
            self.he[he] = 0.0
            if self.debugLevel > 20:
                print(hj, "done")
            return "done"

        if abs(speed) > abs(diff)/4.0:
            speed = abs(diff)/4.0

        if self.debugLevel > 20:
            print("hj: {}, he: {} target={:.2f}, current={:.2f}, diff={:.2f}, speed={:.2f}".format(hj, he, angle, self.hj[hj], diff, speed))

        if self.hj[hj] < angle:
            self.pns.hinge_joint_effector(he, abs(speed))
            self.he[he] = abs(speed) 
        elif self.hj[hj] > angle:
            self.pns.hinge_joint_effector(he, -abs(speed))
            self.he[he] = -abs(speed)

        return "not done"

# ==================================== #

    def move_hj_by(self, hj, angle=None, percent=None, speed=25):
        """Move the given hinge joint by the specified angle
        移动铰链关节通过给予特定的角度值
        The angle can be given in degree (angle=<degree>)
        or percent (percent=<percentage>). If both are specified, the angle keyword
        gets priority.
        Speed is specified in percent of maximum speed""" 

        if angle == None and percent == None:
            raise Exception("Either angle or percent must be specified in move_hj_by()")

        elif angle != None:
            # just to give angle keyword priority over percent
            pass

        else:
            angle = percent/100.0*(self.hjMax[hj]-self.hjMin[hj]) 

        targetAngle = self.hj[hj] + angle
        kwDict = {'hj': hj, 'angle': targetAngle, 'speed': speed}
        self.msched.append([self.move_hj_to, kwDict])

        return "done"

# ==================================== #

    def get_hj(self, hj):
        """Return hj value in percent
        返回铰链关节的百分比"""

        angle    = self.hj[hj]
        minAngle = self.hjMin[hj]
        maxAngle = self.hjMax[hj]

        percent  = 100.0 * (angle - minAngle) / (maxAngle - minAngle)

        return percent

# ==================================== #

    def step_left(self):
        """Make a step with the left foot
        迈左脚"""
        done = [False]
        print("ACC:", np.linalg.norm(self.acc.get()))
        #numpy.linalg.norm欧氏距离公式可以直接求空间中两点的距离,numpy.linalg.norm(a-b)    a,b分别存储一个三维坐标

        done[0] = False
#        self.msched.append([self.move_hj_to, {'hj': 'rlj3', 'percent': 50}, done])
#        self.msched.append([self.move_hj_to, {'hj': 'rlj4', 'percent': 50}, done])
        self.msched.append([self.move_hj_to, {'hj': 'rlj5', 'percent': 100}, done])
        self.msched.append([self.move_hj_to, {'hj': 'llj5', 'percent': 100}, done])

        self.test_orientation(0.1)              #orientation方向，定位


        # while not done[0]:
        #    print("ACC:", np.linalg.norm(self.acc.get()))
        #    print("GYR:", self.gyr.get())
        #    print(self.gyr.x)
        #    print(self.gyr.y)
        #    print(self.gyr.z)
        #    print("")
        #    time.sleep(0.05)
        #
        # time = time.time()
        # time.sleep(1.0)
        #
        # done[0] = False
        # self.msched.append([self.move_hj_to, {'hj': 'hj1', 'percent': 0}, done])
        # while not done[0]:
        #     pass
        # done[0] = False
        # self.msched.append([self.move_hj_to, {'hj': 'hj1', 'percent': 50}, done])
        # while not done[0]:
        #     pass

# ============================================================================ #

#####################
# UTILITY FUNCTIONS  #
#####################

def rotate_arbitrary(axis, point, angle=None, degree=True):
    """Rotate the 3D point about the given axis.
    通过得到轴线旋转3D点
    If axis is not normalized and angle is None, the angle is taken as the norm
    of axis. If degree == False, angles are expected in radiant.
    如果axis没有标准化且角度为空，这个角将使用一个基准脚，如果degree == false 角是弧度"""

    # ensure axis is unit length        确定轴线是单位长
    axisNorm = np.linalg.norm(axis)
    if axisNorm == 0: return point
    axisn    = axis / axisNorm
    if angle == None:
        angle = axisNorm
        
    if degree:
        # convert to radiant　转化成弧度制
        angle *= np.pi / 180.0

    u = axisn[0]
    v = axisn[1]
    w = axisn[2]
    x = point[0]
    y = point[1]
    z = point[2]

    sin = math.sin(angle)
    cos = math.cos(angle)
    dot = np.dot(axisn, point)
    tmp = dot * (1 - cos)

    result = np.array([u * tmp + x*cos + (-w*y + v*z) * sin, \
                       v * tmp + y*cos + ( w*x - u*z) * sin, \
                       w * tmp + z*cos + (-v*x + u*y) * sin])

    return result

# ============================================================================ #

##############
# EXCEPTIONS 解决异常#
##############

class SchedulerConflict(Exception):
    """Raised upon trying to schedule a function that
    is already in the MovementScheduler
    调度冲突；"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

    def resue_socket_addr(self,port):
        resue_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        old_state = resue_socket.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
        print("Old State:%s" %old_state)

        resue_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        new_state = resue_socket.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
        print("New State: %s" %new_state)

        self.port = port

        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        srv.bind('',self.port)
        srv.listen(1)
        print("Listening On Port :%s " %self.port)

        while(True):
            try:
                connection,addr = srv.accept()
                print( "Connect by %s:%s" % (addr[0],addr[1]))
            except KeyboardInterrupt:
                break
           # except socket.error,msg:
           #      print("%s" %msg)





class QueueItemError(Exception):
    """Raised if an item to be schedule with the MovementScheduler
    has the wrong format"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



