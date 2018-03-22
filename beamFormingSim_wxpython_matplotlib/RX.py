# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

#ax = plt.subplot(111)

def get_seq(phase, vibnum, t):
    res = np.cos(phase - np.pi*np.pi/180*t*0)
    for i in range(1, vibnum):
        res = res + np.cos(phase - np.pi*np.sin(np.pi/180*t)*i)
    
    return res/vibnum

    
#θ，指照射方面与天线阵列法线的夹角
theta = np.arange(-90, 90, 0.2)
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
plt.xlim(-90,90)
plt.show()


#print help(plt.plot)


#这个图画出来，不可以直接把图像中的峰、谷等同于空口的beamForming效果
#比如，图中有负值出现
#是因为是只画了一个相位。负值出现其实是出现了相位的翻转。 用发送解释，就是发送的同相的圆弧的弧度变大了，这个可以在发送仿真图里同相波面与圆面的交叉线可以看出来。
#真正的Beam是比如中间的那个要宽的。要想看到，就要把phase等于各个相位，求cos或sin，再取绝对值，画出来的图叠加在一起。看XRX.py