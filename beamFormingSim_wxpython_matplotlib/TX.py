# -*- coding: utf-8 -*-

import wx
import math

w = 2000
h = 1100
Margin = 200
class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
 
        # 复选框
        self.isConsiderPathLoss = wx.CheckBox(self, label="Path Loss?", pos=(20,20))
        
        # 振子数目
        self.vib_List = ['1', '2', '4', '8', '16', '32', '64']
        self.vibs = wx.RadioBox(self,label="Vibrator num", pos=(20, 70),choices=self.vib_List, majorDimension=1, style=wx.RA_SPECIFY_COLS)
        
        # 相位偏移数目
        radioList = ['-90', '-60', '-30', '0', '30', '60', '90']
        self.phase = wx.RadioBox(self,label="Phase offset", pos=(20, 370),choices=radioList, majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.phase.SetSelection(3)

        # start按钮                          
        self.button = wx.Button(self, label='Show', pos=(20, 930))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        
        self.img = wx.Image(w - Margin, h, True)
        self.bitmp = self.img.ConvertToBitmap()
        
        #Vlist = [1,2,4,8,16,32,64]
        #Plist = [-math.pi/2,-math.pi/3,-math.pi/6,0,math.pi/6,math.pi/3,math.pi/2]
        #Llist = [True, False]
        #
        #for i in Vlist:
        #    for j in Plist:
        #        for k in Llist:
        #            
        #            d = int(j/math.pi*180)
        #            if k:
        #                s = "%uVibrators_%uPhaseOff_withPathLoss"%(i,d)
        #            else:
        #                s = "%uVibrators_%uPhaseOff_withoutPathLoss"%(i,d)
        #                
        #            print s
        #                
        #            self.simulate_bf(i, j, k,1);
        #            self.bitmp = self.img.ConvertToBitmap()
        #            
        #            self.bitmp.SaveFile("results\\"+s +".png", wx.BITMAP_TYPE_PNG)
        
        self.img = wx.Image(w - Margin, h, True)
        self.bitmp = self.img.ConvertToBitmap()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnClick(self, event):
        #print 'Click on object with Id %d\n' % event.GetId()
        #print "GetValue %u"%self.isConsiderPathLoss.GetValue()
        #print "GetSelection %u"%self.vibs.GetSelection()
        image_size = self.img.GetSize();

        vibsNUM = int(self.vib_List[self.vibs.GetSelection()])
        phaseOFF = math.pi/6 * (self.phase.GetSelection() - 3) # pi/6 is 30 degree
        isPathL = self.isConsiderPathLoss.GetValue()

        dc = wx.ClientDC(self)
        
        #清除上次的内容
        dc.Clear()
        
        #print "vibsNUM is %u, phase off is %lf, is considerPathLoss %u"%(vibsNUM, phaseOFF, isPathL)
        self.simulate_bf(vibsNUM, phaseOFF, isPathL);
    
        self.bitmp = self.img.ConvertToBitmap()
        #self.bitmp.SaveFile("xxxxx.bmp", wx.BITMAP_TYPE_BMP)

        #画出来
        dc.DrawBitmap(self.bitmp, Margin,0, True)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmp, Margin,0, True)

    def simulate_bf(self, VibratorNum, phaseoff, isPathLoss):
        image_size = self.img.GetSize();
        
        #波长
        la = math.pi * 10
        #la = 4
        
        #相邻振子间距离
        dis_of_Vib = la/2
        Vibrators = [int((image_size[1]  - dis_of_Vib*(VibratorNum - 1))/2)]
        i = 1;
        while i< VibratorNum:
            Vibrators.append(int(Vibrators[i-1]+la/2))
            i+=1

        #print Vibrators

        ymid_x = float(0);
        ymid_y = float(image_size[1]/2);
        circle_r = float(image_size[1]*1.3);
        circle_rP2 = math.pow(circle_r,2)
        
        #计算角度用的，放在循环外面
        Factor = 2*math.pi/la;
        for i in range(image_size[0]):
            for j in range(image_size[1]):
                if abs(math.sqrt(math.pow(i-ymid_x,2) + math.pow(j-ymid_y,2)) - circle_r) < 0.5:
                    self.img.SetRGB(i, j, 255, 255, 255)
                elif i == image_size[0]/2:
                    self.img.SetRGB(i, j, 255, 255, 255)
                elif j == image_size[1]/2:
                    self.img.SetRGB(i, j, 255, 255, 255)
                else:
                    elec_mag_val = []

                    c = 0
                    for vib in Vibrators:
                        pd = math.pow(i,2) + math.pow(vib-j,2)
                        distan =math.sqrt(pd)
                        val = math.sin(distan*Factor + phaseoff*c)
                        c+=1

                        if isPathLoss and pd:
                            val = val/(0.00001*pd)
                        elec_mag_val.append(val)
                        
                    sum = 0.0
                    for v in elec_mag_val:
                        sum +=v;
                    aver = sum/len(elec_mag_val)
                        
                    point_value = int(aver*255)

                    if point_value>0:
                        self.img.SetRGB(i, j, point_value, 0, 0) #红色
                    else:
                        self.img.SetRGB(i, j, 0, 0, -point_value) #蓝色
                
                
                
        #把振子位置用白点显示出来
        for vib in Vibrators:
            for i in range(3):
                for j in range(vib-1, vib+2):
                    self.img.SetRGB(i, j, 255, 255, 255)
        

app = wx.App(False)
frame = wx.Frame(None,title = "BeamForming simulator", size = (w, h))
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()