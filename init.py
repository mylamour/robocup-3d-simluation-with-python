__author__ = 'king'

#! /usr/bin/env python3

from Agent import PNS
from Agent import MovementScheduler
from Agent import GameState
from Agent import Gyroscope
from Agent import Accelerometer
from Agent import ForceResistanceSensor
from Agent import NaoRobot
from Agent import SchedulerConflict
from Agent import QueueItemError


if __name__ == '__main__':
    myNao=NaoRobot(1,'hahahha','localhost',3100)
    myNao.live()



