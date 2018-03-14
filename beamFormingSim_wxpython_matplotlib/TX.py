# -*- coding: utf-8 -*-

import wx
import math

w = 2000
h = 1100
Margin = 200
class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
 
        # ��ѡ��
        self.isConsiderPathLoss = wx.CheckBox(self, label="Path Loss?", pos=(20,20))
        
        # ������Ŀ
        self.vib_List = ['1', '2', '4', '8', '16', '32', '64']
        self.vibs = wx.RadioBox(self,label="Vibrator num", pos=(20, 70),choices=self.vib_List, majorDimension=1, style=wx.RA_SPECIFY_COLS)
        
        # ��λƫ����Ŀ
        radioList = ['-90', '-60', '-30', '0', '30', '60', '90']
        self.phase = wx.RadioBox(self,label="Phase offset", pos=(20, 370),choices=radioList, majorDimension=1, style=wx.RA_SPECIFY_COLS)
        self.phase.SetSelection(3)
        
        self.scaleFactors = ['1', '2', '4', '8', '16', '32', '64'];
        self.ScaleFs = wx.RadioBox(self,label="scale Factors", pos=(20, 670),choices=self.scaleFactors, majorDimension=1, style=wx.RA_SPECIFY_COLS)
        
        # start��ť                          
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
        SF = int(self.scaleFactors[self.ScaleFs.GetSelection()])
        phaseOFF = math.pi/6 * (self.phase.GetSelection() - 3) # pi/6 is 30 degree
        isPathL = self.isConsiderPathLoss.GetValue()

        dc = wx.ClientDC(self)
        
        #����ϴε�����
        dc.Clear()
        
        #print "vibsNUM is %u, phase off is %lf, is considerPathLoss %u"%(vibsNUM, phaseOFF, isPathL)
        self.simulate_bf(vibsNUM, phaseOFF, isPathL,SF);
    
        self.bitmp = self.img.ConvertToBitmap()
        self.bitmp.SaveFile("xxxxx.bmp", wx.BITMAP_TYPE_BMP)

        #������
        dc.DrawBitmap(self.bitmp, Margin,0, True)

    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bitmp, Margin,0, True)

    def simulate_bf(self, VibratorNum, phaseoff, isPathLoss, scalf):
        image_size = self.img.GetSize();
        
        #����
        la = math.pi * 5
        #la = 4
        
        #�������Ӽ����
        dis_of_Vib = la/2
        Vibrators = [int(image_size[1]/2 - dis_of_Vib*(VibratorNum/2))]
        i = 1;
        while i< VibratorNum:
            Vibrators.append(int(Vibrators[i-1]+la/2))
            i+=1

        #print Vibrators

        #����Ƕ��õģ�����ѭ������
        
        Factor = 2*math.pi/la;
        for i in range(image_size[0]):
            for j in range(image_size[1]):
                elec_mag_val = []

                c = 0
                for vib in Vibrators:
                    pd = math.pow(i*scalf,2) + math.pow((vib-j)*scalf,2)
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
                    self.img.SetRGB(i, j, point_value, 0, 0) #��ɫ
                else:
                    self.img.SetRGB(i, j, 0, 0, -point_value) #��ɫ
                    
        #������λ���ð׵���ʾ����
        for vib in Vibrators:
            for i in range(3):
                for j in range(vib-1, vib+2):
                    self.img.SetRGB(i, j, 255, 255, 255)
        

app = wx.App(False)
frame = wx.Frame(None,title = "BeamForming simulator", size = (w, h))
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()