# -*- coding: utf-8 -*-
import struct
import sys
import wx
import os

# in struct.Struct()
# I = u32 H=u16 B=u8 Q=u64,
# and < is little-endian, > is Big-endian, ! is Network order

#typedef struct _pcap_file_header
#{
#  u32           magic; /* =0xa1b2c3d4¡£ */
#  u16           version_major; /* =2 */
#  u16           version_minor; /* =4 */
#  u32           thiszone; /* no used, = 0 */
#  u32           sigfigs;/* no used, = 0 */
#  u32           snaplen;/* max packet length */
#  u32           linktype;/* 1 for eth */
#}pcap_file_header;
pcap_file_header_pattern = struct.Struct('I HH IIII')
pcap_file_header_len = 24;

#typedef struct _pcap_pkthdr
#{
#    u32 GMTtime;
#    u32 microTime;
#    u32 caplen;/* captured length. caplen = min(len, snaplen) */
#    u32 len; /* Original legnth of the packet */
#}pcap_pkthdr;
pcap_pkt_header_pattern = struct.Struct('IIII')
pcap_pkt_header_len = 16

eth_header_pattern = struct.Struct('!BBBBBB BBBBBB H') #6bytes dmac, 6bytes smac, 2bytes ethtype in ETH2 or length in 802.3
eth_header_len = 14

Vlan_tag_pattern = struct.Struct('!HH') # 3bits priority, 1 bit CFI(always 0), 12 bits vlan id, 2bytes type
Vlan_tag_len = 4

#typeid u16, eventsize u16, eventnum u8, fragmentIndex u8, localqid u16, reserved1 u16, messageid u16, reserved2 u32
BIP_header_pattern = struct.Struct('!HHBBHHHI') 
BIP_header_len = 16

msgList = (
    ("DlData_XpbchSendReq"          , 0x0106), 
    ("DlData_EpbchSendReq"          , 0x010b), 
    ("DlData_AddressReq"            , 0x0104), 
    ("DlData_AddressResp"           , 0x0105), 
    ("DlData_PdcchSendReq"          , 0x0109), 
    ("DlData_SubfrTypeReq"          , 0x0107), 
    ("DlData_PdschSendReq"          , 0x010a), 
    ("DlData_PatternConfigReq"      , 0x010c), 
    ("DlData_PdschPayloadTbSendReq" , 0x0108), 
 
    ("LoData_DlRlcPduSendReq"       , 0x0400),
    ("LoData_UlRlcPduReceiveInd"    , 0x0401),
    ("LoData_UeDataPathInfoInd"     , 0x0402),
    ("LoData_FreeTypes_LoData"      , 0x0403),
    ("LoData_DlRlcStatusPduSendReq" , 0x0404),
 
    ("UlData_PuschReceiveRespLo"    , 0x0208),
    ("UlData_AddressReq"            , 0x0204),
    ("UlData_AddressResp"           , 0x0205),
    ("UlData_SyncInd"               , 0x0206),
    ("UlData_PuschReceiveRespPsD"   , 0x0209),
    ("UlData_PuschReceiveRespPsU"   , 0x020a),
    ("UlData_PuschReceiveReq"       , 0x0207),
    ("UlData_PuschReceiveRespHarqU" , 0x020b),
    ("UlData_PrachReceiveInd"       , 0x020c),
    ("UlData_DelayResp"             , 0x020d),
    ("UlData_DelayReq"              , 0x020e),
    ("UlData_PucchReceiveReq"       , 0x0210),
    ("UlData_PucchReceiveRespPsD"   , 0x0211),
    ("UlData_PucchReceiveRespPsU"   , 0x0212),
    ("UlData_PucchReceiveRespHarqD" , 0x020f)
    )
class FileDrop(wx.FileDropTarget):
    def __init__(self, fpanel):
        wx.FileDropTarget.__init__(self)
        self.panel = fpanel

    def OnDropFiles(self, x, y, filePath):         
        #handle = open(filePath[0], "r")
        #ss = handle.read(10); 
        #print ss
        #handle.close()
        #wx.FileDropTarget.OnDropFiles(self, x, y, filePath)
        
        self.panel.tobedeal.SetValue(filePath[0])
        self.panel.fileter_a_pcap(filePath[0])
        return True

class FilterPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
  
        self.msglists = []
        deltalH = 21
        s = self.CreatAllowList("allowMsgs", (10, 10),deltalH)
        
        self.CreatDenyList("DenyMsgs", (10+s[0]+15, 10), deltalH)
        
        self.othersMsgCheck = wx.CheckBox(self, -1, label="others", pos=(10+s[0] * 2+25, 10+25))
        self.othersMsgCheck.SetValue(1)
        
        # open file button                         
        self.openFilebutton = wx.Button(self, label='Open', pos=(10, s[1]+20), size = (50,30))
        self.Bind(wx.EVT_BUTTON, self.OnopenFilebutton, self.openFilebutton)
        
        tobedealpos = (70, s[1]+20)
        tobodealsize = (455, 30)
        self.tobedeal = wx.TextCtrl(self, value="",pos = tobedealpos, size = tobodealsize, style = wx.TE_READONLY, name = "name")
        
        self.filter_it = wx.Button(self, label='Filter', pos=(tobedealpos[0] + tobodealsize[0] + 10, s[1]+20), size = (50,30))
        self.filter_it.Disable()
        self.Bind(wx.EVT_BUTTON, self.Onfilter_it, self.filter_it)

        self.fileDrop = FileDrop(self) 
        self.SetDropTarget(self.fileDrop)
        
    def EvtCheckBox(self, event):
        print 'EvtCheckBox: %d\n' % event.IsChecked()
        #print type(event)
        #print dir(event)
        print 'Id: %d\n' % event.GetId()
        #print type(event.GetId())     
        
    def showchecklist(self):
        for i in self.allowMsgList:
            print "%s(%d) 's checked? %d"%(i.GetLabel(), i.GetId(), i.IsChecked())
            
    def fileter_a_pcap(self, filename):
        allowList = []
        for i in self.allowMsgList:
            if i.GetValue():
                allowList.append(i.GetId() - 10000)
 
        denylist = []
        for i in self.denyMsgList:
            if i.GetValue():
                denylist.append(i.GetId() - 20000)
        
        self.do_fileter(filename, allowList,denylist, self.othersMsgCheck.GetValue())
        
    def Onfilter_it(self, event):
        filename = self.tobedeal.GetValue()
        if os.path.isfile(filename):
            self.fileter_a_pcap(filename)
    def OnopenFilebutton(self, event):
        #self.logger.AppendText('Click on object with Id %d\n' % event.GetId())

        filename = ""
        file_wildcard = "Pcap files(*.pcap)|*.pcap|All files(*.*)|*.*" 
        dlg = wx.FileDialog(self, "Open paint file...",
                            os.getcwd(),
                            wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            self.tobedeal.SetValue(filename)
            
        dlg.Destroy()
        
        if len(filename) > 0:
            self.fileter_a_pcap(filename)
 
    def reverseMsgBoxs(self, MsgBoxList):
        valueList = []
        for a_box in MsgBoxList:
            valueList.append(a_box.GetValue())
        if 0 in valueList:
            for a_box in MsgBoxList:
                a_box.SetValue(1)
        else:
            for a_box in MsgBoxList:
                a_box.SetValue(0)

    def OnAllowALLbutton(self, event):
        self.reverseMsgBoxs(self.allowMsgList)

    def OnDenyALLbutton(self, event):
        self.reverseMsgBoxs(self.denyMsgList)
        
    def CreatAllowList(self, groupLabel, GroupPos, deltalH):
        self.allowMsgList = []
        x = GroupPos[0]+10
        y = GroupPos[1]+25
        h = y

        for bipmsg in msgList:
            msgname = bipmsg[0]
            msgid = bipmsg[1]
            boxID = msgid + 10000
            checkBox = wx.CheckBox(self, boxID, label=msgname, pos=(x,h)); h+=deltalH;
            self.allowMsgList.append(checkBox)

        self.AllowALLbutton = wx.Button(self, label='Select/Unselect all', pos=(x, h),size = (150,25))
        h+=deltalH
        self.Bind(wx.EVT_BUTTON, self.OnAllowALLbutton, self.AllowALLbutton)

        GroupW = 280
        GroupH = h - GroupPos[1] + 15
        box = wx.StaticBox(self, -1, label=groupLabel, pos = GroupPos, size = (GroupW, GroupH))

        return (GroupW, GroupH)

    def CreatDenyList(self, groupLabel, GroupPos, deltalH):
        self.denyMsgList = []
        x = GroupPos[0]+10
        y = GroupPos[1]+25
        h = y

        for bipmsg in msgList:
            msgname = bipmsg[0]
            msgid = bipmsg[1]
            boxID = msgid + 20000
            checkBox = wx.CheckBox(self, boxID, label=msgname, pos=(x,h)); h+=deltalH;
            self.denyMsgList.append(checkBox)

        self.DenyALLbutton = wx.Button(self, label='Select/Unselect all', pos=(x, h),size = (150,25))
        h+=deltalH
        self.Bind(wx.EVT_BUTTON, self.OnDenyALLbutton, self.DenyALLbutton)

        GroupW = 280
        GroupH = h - GroupPos[1] + 15
        box = wx.StaticBox(self, -1, label=groupLabel, pos = GroupPos, size = (GroupW, GroupH))

        return (GroupW, GroupH)

    def getBipMsgID_fromEth(self, pktBuf):
        offset_in_pkt = 0;
        if len(pktBuf) < offset_in_pkt + eth_header_len:
            print "wrong eth pkt"
            return 0xffff
        
        eth_header = eth_header_pattern.unpack(pktBuf[offset_in_pkt:(offset_in_pkt + eth_header_len)])
        offset_in_pkt += eth_header_len

        pkt_type = eth_header[12]
        while 0x8100 == pkt_type:  # Loop incase of QinQ
            if len(pktBuf) < offset_in_pkt + Vlan_tag_len:
                print "wrong vlan pkt"
                return 0xffff
            vlan_tag = Vlan_tag_pattern.unpack(pktBuf[offset_in_pkt:(offset_in_pkt + Vlan_tag_len)])
            offset_in_pkt += Vlan_tag_len
            pkt_type = vlan_tag[1]

        if 0x8951 == pkt_type: #bip
            if len(pktBuf) < offset_in_pkt + Vlan_tag_len:
                print "wrong bip pkt"
                return 0xffff
     
            bipheader = BIP_header_pattern.unpack(pktBuf[offset_in_pkt:(offset_in_pkt + BIP_header_len)])
            offset_in_pkt += BIP_header_len
            _msgid = bipheader[6]
            return _msgid

        return 0xffff #means it is not a bip msg

    def do_fileter(self, pcapfile, Allow_msglist, Deny_msglist, Is_allow_others):
        print Allow_msglist
        print Deny_msglist
        print Is_allow_others
        NameOfSrcFile = pcapfile
        srcfile = open(NameOfSrcFile, "rb")

        buf = srcfile.read(); 
        if (not buf) or (len(buf) < pcap_file_header_len):
            print "Read failed or '%s' is a non-pcap file."%(NameOfSrcFile)
            return
        fileHeader = pcap_file_header_pattern.unpack(buf[:pcap_file_header_len])
        print "magic = 0x%x, version_major:0x%x,version_minor:0x%x, thiszone=0x%x, sigfigs=0x%x, snaplen=%x linktype=%x"%fileHeader
        if 0xa1b2c3d4 != fileHeader[0]:
            print "Doesn't support a non-pcap file."
            return;

        NameOfDstFile = os.path.dirname(NameOfSrcFile) + "\\xx" +os.path.basename(NameOfSrcFile)
        #NameOfDstFile = "dst.pcap"   
        outputfile = open(NameOfDstFile,"wb")
        print "outputfile:",NameOfDstFile

        outputfile.write(buf[:pcap_file_header_len]);
        OFF = pcap_file_header_len
        
        # Gauge(parent, id=ID_ANY, range=100, pos=DefaultPosition, size=DefaultSize, style=GA_HORIZONTAL, validator=DefaultValidator, name=GaugeNameStr) 
        self.progressBar = wx.Gauge(self, wx.ID_ANY, range=100, pos = (10, 798-75), size = (300, 30))
        
        buf_len_div_100 = len(buf)/100;
        tcnt = 0
        allowCnt = 0
        while len(buf) - OFF >pcap_pkt_header_len:
            
            pcap_pkt_header = pcap_pkt_header_pattern.unpack(buf[OFF :(OFF + pcap_pkt_header_len)])
            pktlen = pcap_pkt_header[2]
            if len(buf) < OFF + pcap_pkt_header_len + pktlen:
                print "A  invalid pkt in the end"
                break

            pkt = buf[OFF:OFF+pktlen+pcap_pkt_header_len]
            OFF+=pktlen+pcap_pkt_header_len
            
            msgid = self.getBipMsgID_fromEth(pkt[pcap_pkt_header_len : ( pcap_pkt_header_len + pktlen)])
            if msgid in Allow_msglist:
                outputfile.write(pkt);
                allowCnt+=1;
            elif msgid in Deny_msglist:
                pass
            elif Is_allow_others:
                outputfile.write(pkt);
                allowCnt+=1;
            
            tcnt+=1
            if 0 == (tcnt % 100000):
                print "%u items were scaned."%(tcnt)
            
            self.progressBar.SetValue(OFF/buf_len_div_100)
        outputfile.close()
        srcfile.close() 
        
        import time
        time.sleep(1)
        self.progressBar.Destroy()
        
        print "Done. %u/%u items were saved."%(allowCnt, tcnt)

Filter = wx.App(False)
frame = wx.Frame(None,size = (680, 798),title="pcap filter" ,style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX)
panel = FilterPanel(frame)
frame.Show()
Filter.MainLoop()        