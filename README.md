	之前本项目的是由C++实现的，代码实在混乱异常,极不利于维护。
	现自己边学习，边使用python重新编写robocup 3d simulaiton 项目代码，并进行机器学习代码的编写（代码和书籍参考机器学习实战）。
	虽然不知道以自己的实力能得到什么名次，但愿意通过这个项目的学习提升自己，开阔眼界。
	愿一切顺利

出现的问题：
	1.怎么使用多线程
	2.找到刚体动力学的库				√
	3.接口到matlab		
					way :
							-->  matlab---计算--->
				
						--->输出一个xml文件——读取一个xml文件---
														
							---计算---3Dserver--------
						具体：
								使用robotics工具箱绘制出一个机器人的模型，使其运动，然后读取这些坐标，记录到
											xml文件中。
											在python中直接调用配置文件进行读取
										
										
2015/8/3:
	希望尽快完成基本的动作设计，调试并使其流畅。
	问题：	
			1.将多线程的应用到每个动作上，为每个Agent实行一个独立的进程	
			2.遍历所有关节的所有角
			3.三个模型　Agent FrameWork/World FrameWork/Local FrameWork   三个坐标系而已
			4.How To See, How To Localize,How to Get Goal
			5.基本动作成型
	已解决:
			1.多线程使用				√
			2.特定关节角的遍历			√
			
			
2015/8/4:
	继续抓狂中，这个Agent框架实在是无语了
	Bug列表:
			1.无Vision perceptor	
			2.套接字地址不能重用(before today)			√
			3.待补充
			
	已解决：什么也没解决,看usermanual去了

2015/8/8:
	看完userManual发现这的确不是个框架，因为他还缺少几个基本的Perceptors和effectors
	以下:
		# General Perceptors :
                        # GyroRate Perceptor                   √
                        # HingeJoint Perceptor                 √
                        # UniversalJoint Perceptor          --need--
                        # Touch Perceptor                   --need--
                        # ForceResistance Perceptor            √
                        # Accelerometer                        √
        #  Soccer Perceptors:
                        # Vision Perceptor          		--need--
                        # GameState Perceptor         		   √
                        # Hear Perceptor           			--need--
                        # AgentState Perceptor     			--need--

                        
2015/8/12--2015/8/19:
	玩耍中

2015/8/21--2015/8/22:
	卡尔曼和贝叶斯滤波资料阅读
	在usermanul中可以看出nosie来自：
			•　A small calibration error is added to the camera position. For each axis, the error is
				uniformly distributed between -0.005 m and 0.005 m. The error is calculated once and
				remains constant during the complete match.
			• Dynamic noise normally distributed around 0.0
					+ distance error: sigma = 0.0965 (also, distance error is multiplied by distance/100)
					+ angle error (x-y plane): sigma = 0.1225
					+ angle error (latitudal): sigma = 0.1480

2015/8/24:
	今天安装了pip install filterpy(pip3,之前pip时一直是有错误的)	
	Nao (独立开进行设计动作及其他）
		Nao
		Nao1
		Nao2
		Nao3
		Nao4	
	world 写好了
													
													