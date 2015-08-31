#!usr/bin/env python3
from Agent import *
from Action import *
import matplotlib
if __name__ == '__main__':
     TestAction = Action(8,'lamour','localhost',3100,'rsg/agent/nao/nao.rsg',startCoordinates=[-0.5,0.9,0])
    # Test =(NaoRobot(7,'lamour','localhost',3100,'rsg/agent/nao/nao_hetero.rsg 2', startCoordinates=[-4.5, 0.0, 0]))

    #Test Agent.py Use Dict To Easy Init Agent
    # MyNao = { #"Player2":NaoRobot(2,'lamour','localhost',3100,'rsg/agent/nao/nao_hetero.rsg 3', startCoordinates=[-1.5, 0.0, 0]),
    #         "Player3":NaoRobot(3,'lamour','localhost',3100,'rsg/agent/nao/nao_hetero.rsg 3',startCoordinates=[-2.5, 0.0, 0]),
    #         "Player4":NaoRobot(4,'lamour','localhost',3100,'rsg/agent/nao/nao_hetero.rsg 4', startCoordinates=[-3.5, -2.0, 0]),
    #         "Player5":NaoRobot(5,'lamour','localhost',3100,'rsg/agent/nao/nao_hetero.rsg 4', startCoordinates=[-3.5, 0.0, 0]),
    #         "Player6":NaoRobot(6,'lamour','localhost',3100,'rsg/agent/nao/nao_hetero.rsg 2', startCoordinates=[-3.5, 2.0, 0]),
    #        "Player7":NaoRobot(7,'lamour','localhost',3100,'rsg/agent/nao/nao_hetero.rsg 2', startCoordinates=[-4.5, 0.0, 0])
    #        }

#Test Agent.py Init Playmode --------false
    #if(MyNao["Player7"].gamestate.__init__(playmode='Play on')):
    #     Test_By.step_left()
    # Test =(NaoRobot(7,'lamour','localhost',3100,'rsg/agent/nao/nao_hetero.rsg 2', startCoordinates=[-0.5, 0.0, 0]))
#Test Action.py  By use Move_hj_to || Move _hj_by 同样错误的角度值会使机器人关节很奇怪
    # Test_To = Action(7,'lamour','localhost',3100,'rsg/agent/nao/nao.rsg',startCoordinates=[-0.5,0.6,0])
    # Test_By = Action(8,'lamour','localhost',3100,'rsg/agent/nao/nao.rsg',startCoordinates=[-0.5,0.9,0])    #角度开合更大，已经手臂翻转了
    # Test_By.Test_by()
    # Test_To.Test_to()

#Test Action.py Speed By use Move_hj_to || Move _hj_by,机器人会出现骨折现象～～
    # Test_To7 = Action(7,'lamour','localhost',3100,'rsg/agent/nao/nao.rsg',startCoordinates=[-0.5,0.6,0])
    #
    # Test_To8 = Action(8,'lamour','localhost',3100,'rsg/agent/nao/nao.rsg',startCoordinates=[-0.5,0.9,0])
    #
    # Test_To7.Test_to()
    # Test_To8.Test_to2()
#Test Agent.py Test_Orientation
    # Test =(NaoRobot(7,'lamour','localhost',3100,'rsg/agent/nao/nao_hetero.rsg 2', startCoordinates=[-4.5, 0.0, 0]))
    # Test.test_orientation()

#Test Action.py Test_Orientation

    # TestAction.Test_orientation(5.0,'orientation_length5')
    # TestAction.Test_orientation(4.0,'orientation_length4')
    # TestAction.Test_orientation(3.0,'orientation_length3')
    # TestAction.Test_orientation(2.0,'orientation_length2')
    # TestAction.Test_orientation(1.0,'orientation_length1')
    #到这可以知道，length代表的就是时间值，持续多少秒，下面用matplotlib画图看看是什么样的
   # =================================================== #
   #     a simple example to plot a 3d picture
   # =================================================== #
     # import numpy as np
     # import matplotlib.pyplot as plt
     # import mpl_toolkits.mplot3d
     #
     # x,y=np.mgrid[-2:2:20j,-2:2:20j]
     # z=x*np.exp(-x**2-y**2)
     #
     # ax=plt.subplot(111,projection='3d')
     # ax.plot_surface(x,y,z,rstride=2,cstride=1,cmap=plt.cm.coolwarm,alpha=0.8)
     # ax.set_xlabel('x')
     # ax.set_ylabel('y')
     # ax.set_zlabel('z')
     #
     # plt.show()


#Test Action.py Step_by_left
      # TestAction.Test_step_by_left_knee()
      # TestAction.Test_step_by_right_knee()
      # TestAction.Test_Walk()
      # TestAction.Test_step_by_right_foot()
      # TestAction.Test_step_by_left_foot()
      # TestAction.Test_to()
     TestAction.Test_Walk()
     # for testl in range(hjMin['llj3'],hjMax['llj3']):
     #     print("llj3",testl)
     #     testl += 1
