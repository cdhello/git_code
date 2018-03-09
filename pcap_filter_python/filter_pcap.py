#coding:utf-8
import struct
import sys

DlData_XpbchSendReq          = 0x0106 
DlData_EpbchSendReq          = 0x010b 
DlData_AddressReq            = 0x0104 
DlData_AddressResp           = 0x0105 
DlData_PdcchSendReq          = 0x0109 
DlData_SubfrTypeReq          = 0x0107 
DlData_PdschSendReq          = 0x010a 
DlData_PatternConfigReq      = 0x010c 
DlData_PdschPayloadTbSendReq = 0x0108 

LoData_DlRlcPduSendReq       = 0x0400
LoData_UlRlcPduReceiveInd    = 0x0401
LoData_UeDataPathInfoInd     = 0x0402
LoData_FreeTypes_LoData      = 0x0403
LoData_DlRlcStatusPduSendReq = 0x0404

UlData_PuschReceiveRespLo    = 0x0208
UlData_AddressReq            = 0x0204
UlData_AddressResp           = 0x0205
UlData_SyncInd               = 0x0206
UlData_PuschReceiveRespPsD   = 0x0209
UlData_PuschReceiveRespPsU   = 0x020a
UlData_PuschReceiveReq       = 0x0207
UlData_PuschReceiveRespHarqU = 0x020b
UlData_PrachReceiveInd       = 0x020c
UlData_DelayResp             = 0x020d
UlData_DelayReq              = 0x020e
UlData_PucchReceiveReq       = 0x0210
UlData_PucchReceiveRespPsD   = 0x0211
UlData_PucchReceiveRespPsU   = 0x0212
UlData_PucchReceiveRespHarqD = 0x020f

############################################################################################
Allow_msglist = [DlData_PdcchSendReq, DlData_PdschSendReq,DlData_PdschPayloadTbSendReq,UlData_PuschReceiveRespLo,UlData_PuschReceiveRespPsD,UlData_PuschReceiveRespPsD, 
UlData_PuschReceiveRespPsU,  
UlData_PuschReceiveReq, 
UlData_PuschReceiveRespHarqU,
UlData_PrachReceiveInd, 
UlData_PucchReceiveReq ,     
UlData_PucchReceiveRespPsD, 
UlData_PucchReceiveRespPsU,
UlData_PucchReceiveRespHarqD]
############################################################################################

############################################################################################
Deny_msglist = [UlData_SyncInd, DlData_SubfrTypeReq, DlData_PatternConfigReq, DlData_XpbchSendReq, DlData_EpbchSendReq]
############################################################################################

############################################################################################
Is_allow_others = False  # True or False
############################################################################################

# in struct.Struct()
# I = u32 H=u16 B=u8 Q=u64,
# and < is little-endian, > is Big-endian, ! is Network order

#typedef struct _pcap_file_header
#{
#  u32           magic; /* =0xa1b2c3d4。 */
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

def getBipMsgID_fromEth(pktBuf):
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

def run(pcapfile):
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

    NameOfDstFile = "xx"+NameOfSrcFile   
    outputfile = open(NameOfDstFile,"wb")

    outputfile.write(buf[:pcap_file_header_len]);
    OFF = pcap_file_header_len

    tcnt = 0
    allowCnt = 0
    while len(buf) - OFF >pcap_pkt_header_len:
        
        pcap_pkt_header = pcap_pkt_header_pattern.unpack(buf[OFF :(OFF + pcap_pkt_header_len)])
        pktlen = pcap_pkt_header[2]
        if len(buf) < OFF + pcap_pkt_header_len + pktlen:
            print "A  invalid pkt in the end"
            break
        ##格林威治时间
        #timeStamp = pcap_pkt_header[0]  
        #timeArray = time.localtime(timeStamp) #格林威治时间转成本地时间 
        #otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)  #格式化
        #print "%s.%.6u"%(otherStyleTime, pcap_pkt_header[1]) #和后面的微秒一起输出

        pkt = buf[OFF:OFF+pktlen+pcap_pkt_header_len]
        OFF+=pktlen+pcap_pkt_header_len
        
        msgid = getBipMsgID_fromEth(pkt[pcap_pkt_header_len : ( pcap_pkt_header_len + pktlen)])
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

    outputfile.close()
    srcfile.close() 
    
    print "Done. %u/%u items were saved."%(allowCnt, tcnt)

if __name__ == '__main__':

    if (len(sys.argv) > 1):
        run(sys.argv[1]);
    else:
        print "Please input a pcap file."

 
