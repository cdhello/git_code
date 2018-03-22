# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
 
#θ，指照射方面与天线阵列法线的夹角
theta = np.arange(-90, 90, 0.2)

vibnum = 4
phase_num = 50
phase = 0

title = "vibrators num:%u, phase cases num%u"%(vibnum,phase_num)
ax = plt.subplot(111)
ax.set_title(title) 

for p in range(0,phase_num):
    phase +=  np.pi*2/phase_num
    res = 0
    for i in range(0, vibnum):
        res = res + np.cos(phase - np.pi*np.sin(np.pi/180*theta)*i)
    
    res = res/vibnum
    res = np.abs(res) #有相位翻转，所以会有负值
    
    #plt.plot(theta, res, lw=2, label="1vibrator") #lw:line width
    plt.plot(theta, res, lw=1)

#plt.ylim(-0.5,1.2)
plt.xlim(-90,90)
plt.show()

#这个图画出来，就可以直接把图像中的峰、谷等同于空口远场的beamForming效果了
#想像一下把x轴弯曲，形成一个半圆。那个上面每个值就就是圆弧的弧度值。中间的波峰就是beam，两边的就是旁瓣
#振子越多，beam越窄，旁瓣也越多但越小。