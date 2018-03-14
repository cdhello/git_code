# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

#ax = plt.subplot(111)

def get_seq(phase, vibnum, t):
    res = np.cos(phase - np.pi*np.pi/180*t*0)
    for i in range(1, vibnum):
        res = res + np.cos(phase - np.pi*np.pi/180*t*i)
    
    return res/vibnum

    
#θ，指照射方面与天线阵列法线的夹角
theta = np.arange(0, 90, 0.2)
phase = 0; #入射电磁波函数为cos(phase),当phase为0时，就是最大峰值
s1 = get_seq(phase, 1, theta)
s2 = get_seq(phase, 2, theta)
s4 = get_seq(phase, 4, theta)
s8 = get_seq(phase, 8, theta)
s16 = get_seq(phase, 16, theta)

plt.plot(theta, s1, lw=2, label="1vibrator")
plt.plot(theta, s2, lw=2, label="2vibrators")
plt.plot(theta, s4, lw=2, label="4vibrators")
plt.plot(theta, s8, lw=2, label="8vibrators")
plt.plot(theta, s16, lw=2, label="16vibrators")

leg = plt.legend(loc='best', ncol=20, mode="expand", shadow=True, fancybox=True)
leg.get_frame().set_alpha(0.1)

plt.ylim(-0.5,1.2)
plt.xlim(0,90)
plt.show()


#print help(plt.plot)