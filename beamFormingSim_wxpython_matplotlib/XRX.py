# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
 
#�ȣ�ָ���䷽�����������з��ߵļн�
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
    res = np.abs(res) #����λ��ת�����Ի��и�ֵ
    
    #plt.plot(theta, res, lw=2, label="1vibrator") #lw:line width
    plt.plot(theta, res, lw=1)

#plt.ylim(-0.5,1.2)
plt.xlim(-90,90)
plt.show()

#���ͼ���������Ϳ���ֱ�Ӱ�ͼ���еķ塢�ȵ�ͬ�ڿտ�Զ����beamFormingЧ����
#����һ�°�x���������γ�һ����Բ���Ǹ�����ÿ��ֵ�;���Բ���Ļ���ֵ���м�Ĳ������beam�����ߵľ����԰�
#����Խ�࣬beamԽխ���԰�ҲԽ�൫ԽС��