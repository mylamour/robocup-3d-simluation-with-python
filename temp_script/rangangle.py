#!/usr/bin/env python3

#2015/8/24 想到应该写成一个通用的模板，可以使其遍历不同类型的数据区间


from Agent import *
hj = {'hj1': 'Neck Yaw',  # Neck Yaw   脖子左右摇摆
      'hj2': 'Neck Pitch',  # Neck Pitch    脖子上下倾斜
      'raj1': 'Right Shoulder Pitch',  # Right Shoulder Pitch
      'raj2': 'Right Shoulder Yaw',  # Right Shoulder Yaw
      'raj3': 'Right Arm Roll',  # Right Arm Roll
      'raj4': 'Right Arm Yaw',  # Right Arm Yaw
      'laj1': 'Left Shoulder Pitch',  # ___Left Shoulder Pitch
      'laj2': 'Left Shoulder Yaw',  # ___Left Shoulder Yaw
      'laj3': 'Left Arm Roll',  # ___Left Arm Roll
      'laj4': 'Left Arm Yaw',  # ___Left Arm Yaw
      'rlj1': 'Right Hip YawPitch',  # Right Hip YawPitch
      'rlj2': 'Right Hip Roll',  # Right Hip Roll
      'rlj3': 'Right Hip Pitch',  # Right Hip Pitch
      'rlj4': 'Right Knee Pitch',  # Right Knee Pitch
      'rlj5': 'Right Foot Pitch',  # Right Foot Pitch
      'rlj6': 'Right Foot Roll',  # Right Foot Roll
      'llj1': 'Left Hip YawPitch',  # ___Left Hip YawPitch
      'llj2': 'Left Hip Roll',  # ___Left Hip Roll
      'llj3': 'Left Hip Pitch',  # ___Left Hip Pitch
      'llj4': 'Left Knee Pitch',  # ___Left Knee Pitch
      'llj5': 'Left Foot Pitch',  # ___Left Foot Pitch
      'llj6': 'Left Foot Roll', }  # ___Left Foot Roll

hjMax = {'hj1': 120.0,
         'hj2': 45.0,
         'raj1': 120.0,
         'raj2': 1.0,
         'raj3': 120.0,
         'raj4': 90.0,
         'laj1': 120.0,
         'laj2': 95.0,
         'laj3': 120.0,
         'laj4': 1.0,
         'rlj1': 1.0,
         'rlj2': 25.0,
         'rlj3': 100.0,
         'rlj4': 1.0,
         'rlj5': 75.0,
         'rlj6': 45.0,
         'llj1': 1.0,
         'llj2': 45.0,
         'llj3': 100.0,
         'llj4': 1.0,
         'llj5': 75.0,
         'llj6': 25.0, }
hjMin = {'hj1': -120.0,
         'hj2': -45.0,
         'raj1': -120.0,
         'raj2': -95.0,
         'raj3': -120.0,
         'raj4': -1.0,
         'laj1': -120.0,
         'laj2': -1.0,
         'laj3': -120.0,
         'laj4': -90.0,
         'rlj1': -90.0,
         'rlj2': -45.0,
         'rlj3': -25.0,
         'rlj4': -130.0,
         'rlj5': -45.0,
         'rlj6': -25.0,
         'llj1': -90.0,
         'llj2': -25.0,
         'llj3': -25.0,
         'llj4': -130.0,
         'llj5': -45.0,
         'llj6': -45.0, }


# def drange(start, stop, step):
#     r = start
#     while r < stop:
#             yield
#             r += step
#
# for step in drange(hjMin['llj3'],hjMax['llj3'],1):
#     print(hjMax['llj3'],hjMin['llj3'])

# ----------------------------------------------------------#
# count = 0
# while hjMin['llj3'] < hjMax['llj3']:
#     hjMin['llj3'] += 0.1
#     count += 1
#     print(hjMin['llj3'])
#     print(count)

# 这样自动化测试角度，岂不爽歪歪，再设定特征值去筛选动作（划分动作，Ｋ近邻算法　Or　决策树-ID3）
# ----------------------------------------------------------#

# ttcount = 0
# Traversal= 0
# while Traversal<len(hjMin):
#     print(len(hjMin))
#     while hjMin[Traversal] < hjMax[Traversal]:
#         hjMin[Traversal] += 0.1
#         ttcount += 1
#         print(hjMin[Traversal])
#         print(ttcount)
#     Traversal += 1
# --------------------------错误的写法，字典不支持xxx[0~9]使的写法

# print(hjMax.items())
# print(hjMax.pop('llj3'))
# print(hjMax.popitem())    #唯一不好的就是无序的pop不太好，

# print(hjMin.popitem())  ------->      ('llj2', -25.0)
# print(hjMax.popitem())  ------->      ('llj2', 45.0)

#   不过好像也无所谓,但是测试可知，同时弹出的两个字典里的内容是一样的

# print(hjMin.popitem())         #    难道还要提取输出的字符串用python执行shell命令grep 或set 特定值？？？

# Traversal= 0
# while Traversal<len(hjMin):
#     print(len(hjMin))
#     while hjMin.popitem() < hjMax.popitem():
#         hjMin.popitem().__format__() += 0.1
#         ttcount += 1
#         print(hjMin[Traversal])
#         print(ttcount)
#     Traversal += 1

# 其实用numpy库也是可以的
# -------------------------------------------------------------------------------------#
# 到此为止，用于Travsal整个字典并进行角度计算的脚本算是写好了，下面应该定义一些状态，测试角度并记录其值
# 但是想要走路，先要解决多线程的问题，因为python是一种每次只能运行一个线程的玩意，以至于有人还说只要多进
# 程不要多线程，但由于线程之间的状态可以共享。这才能意味着Agent之间共享信息，而且你走一步抬一下腿不可能等
# 你抬膝结束之后再麻木的去翘你的脚，迈你的腿，应该一气呵成，最次也是同步完成，即多线程同时工作。
#
# 在此考量一二，决定回头还是应该给每个Agent一个进程，这意味着独立的个体
# -------------------------------------------------------------------------------------#

# f = open("JointAngelRange", "a")
#
# for travesalhjmin in hjMin:
#     for travesalhjmax in hjMax:
#         if str(travesalhjmin) == str(travesalhjmax):
#             print('This joint name is :', str(travesalhjmin), file=f)
#             print('The Rang is:', hjMin[str(travesalhjmin)], '-->>', hjMax[str(travesalhjmax)], file=f)
#             while hjMin[str(travesalhjmin)] < hjMax[str(travesalhjmax)]:
#                 hjMin[str(travesalhjmin)] += 0.1
#                 print(hjMin[str(travesalhjmin)], file=f)
#     print('\n', file=f)

# 独立的进程才模拟独立的人
# -------------------------------------------------------------------------------------#


# 上面的函数实现了，遍历每个关节的角度域，而不是遍历每个关节的不同关节域（其实只要删除if判断，再加上角度域遍历就能实现，）
# 下面怎么封装成函数，Input object------->  Output 相应关节的计算角度或所有关节角

# class RangeAngle(object):
#     def RangSpecialJointSpecialAngle(jointname, SpecialJointAngleMin == None,SpecialJointAngleMax == None,Step):
#         if SpecialJointAngleMax == SpecialJointAngleMin ==None:                             #测一个角的全部范围
#             for travesalhjmin in hjMin:
#                 for travesalhjmax in hjMax:
#                     if str(travesalhjmin) == str(travesalhjmax) == jointname:
#                         # hjMin[str(travesalhjmin)] = SpecialJointAngleMin
#                         # hjMax[str(travesalhjmax)] = SpecialJointAngleMax
#                         print('This joint name is :', str(travesalhjmin))
#                         print('The Rang is:', hjMin[str(travesalhjmin)], '-->>', hjMax[str(travesalhjmax)])
#                         while hjMin[str(travesalhjmin)] < hjMax[str(travesalhjmax)]:
#                              hjMin[str(travesalhjmin)] += Step
#                              print(hjMin[str(travesalhjmin)])
#
#         if jointname == None:                                                              #测每个关节在一定范围内的角度变化
#             for travesalhjmin in hjMin:
#                 for travesalhjmax in hjMax:
#                     if str(travesalhjmin) == str(travesalhjmax):
#                         hjMin[str(travesalhjmin)] = SpecialJointAngleMin
#                         hjMax[str(travesalhjmax)] = SpecialJointAngleMax
#                         print('This joint name is :', str(travesalhjmin))
#                         print('The Rang is:', hjMin[str(travesalhjmin)], '-->>', hjMax[str(travesalhjmax)])
#                         while hjMin[str(travesalhjmin)] < hjMax[str(travesalhjmax)]:
#                              hjMin[str(travesalhjmin)] += Step
#                              print(hjMin[str(travesalhjmin)])
#
#         if jointname == SpecialJointAngleMax == SpecialJointAngleMin == None:               #测每个关节变化下的所有关节角变化
#             for travesalhjmin in hjMin:
#                 for travesalhjmax in hjMax:
#                         while hjMin[str(travesalhjmin)] < hjMax[str(travesalhjmax)]:
#                              hjMin[str(travesalhjmin)] += 0.1
#                              print(hjMin[str(travesalhjmin)])

# return hjMin[str(travesalhjmin)] #不知道该怎么不断的返回数据，应该不行吧，还是输出到文件，然后再读取吧


# def RangAllJointAllAngle(self):
#
#     for travesalhjmin in hjMin:
#         for travesalhjmax in hjMax:
#             while hjMin[str(travesalhjmin)] < hjMax[str(travesalhjmax)]:
#
#             if str(travesalhjmin) == str(travesalhjmax):
#                 print('This joint name is :', str(travesalhjmin))
#                 print('The Rang is:', hjMin[str(travesalhjmin)], '-->>', hjMax[str(travesalhjmax)])
#                 while hjMin[str(travesalhjmin)] < hjMax[str(travesalhjmax)]:
#                      hjMin[str(travesalhjmin)] += 0.1
#                      print(hjMin[str(travesalhjmin)])

# RangeAngle.RangSpecialJointAngle('llj4',0,10)

# 某个关节细致变化，其他关节大幅变化，然后稳定在一个区域，再在该区域查找
# f = open('testall','a')
# for travesalhjmin in hjMin:
#     print('This is Main  Test Joint :',travesalhjmin,file = f)
#     for travesalhjmax in hjMax:
#         while str(travesalhjmin) == str(travesalhjmax) and hjMin[str(travesalhjmin)] < hjMax[str(travesalhjmax)] :
#             hjMin[str(travesalhjmin)] += 0.1
#             print(hjMin[str(travesalhjmin)],file = f)
#             for travesalMyDifferentHjMax in hjMax:
#                 while str(travesalMyDifferentHjMax) != str(travesalhjmax) and hjMin[str(travesalMyDifferentHjMax)] < hjMax[str(travesalhjmax)]:
#                     print('this joint name:', travesalMyDifferentHjMax,file = f)
#                     hjMin[str(travesalMyDifferentHjMax)] += 0.1
#                     print(hjMin[str(travesalMyDifferentHjMax)],file = f)

# 到现在是做到了几个关节遍历其他所有关节的角，但不是每个关节遍历其他关节的角，不知道逻辑错在哪里，sad




# 明天记得加入matplotlib绘图出来看看，并处理多线程！！多线程，将其放到每个新生成的类之中，object



# print(RangeAngle.RangSpecialJointSpecialAngle('laj2',Step = 1))
MyNao = NaoRobot(7,'lamour','localhost',3100,'rsg/agent/nao/nao_hetero.rsg 2', startCoordinates=[-4.5, 0.0, 0])

def TravesalAngleToFile(JointAngelName='', Step=10):
    f = open(JointAngelName, "a")
    for travesalhjmin in hjMin:
        for travesalhjmax in hjMax:
            if str(travesalhjmin) == str(travesalhjmax) == JointAngelName:
                # print('Joint:', str(travesalhjmin), file=f)
                # print('Rang:', hjMin[str(travesalhjmin)], '-->>', hjMax[str(travesalhjmax)], file=f)
                while hjMin[str(travesalhjmin)] < hjMax[str(travesalhjmax)]:
                    hjMin[str(travesalhjmin)] += Step
                    # print(hjMin[str(travesalhjmin)], file=f)
                    return
    # print('\n', file=f)

def FromFileToAngle(JointAngelName=''):
    # f = open(JointAngelName, "r")
    for text in ():
        print(text)

# time.sleep(0.9)
# MyNao.msched.append([MyNao.move_hj_by, {'hj': 'llj3', 'speed': 100, 'percent': 1}])
# MyNao.msched.append([MyNao.move_hj_by, {'hj': 'rlj3', 'speed': 100, 'percent': 1}])
# TravesalAngleToFile('hj1', 1)







