这个脚本处理一个pcap 文件，按订制把需要的报文另存为一个pcap文件。

这个脚本的头部过滤我们的的设置，两个列表一个开关：
Allow_msglist，这个列表里面的消息，是我们指定要留下的。可以为空。
Deny_msglist，这个列表里的消息，是我们指定不需要的。可以为空。
Is_allow_others，这个值为True或False， 表示如果某条消息既不属于Allow_msglist也不属于Is_allow_others，是要保存还是要删除。

比如以下面规则 “python filter_pcap.py abc.pcap”后，生成的pcap文件名字为xxabc.pcap。xxabc.pcap文件将复制abc.pcap中除了UlData_SyncInd, DlData_SubfrTypeReq的所有条目。
Allow_msglist = [ ]
Deny_msglist = [UlData_SyncInd, DlData_SubfrTypeReq]
Is_allow_others = True

目前仅支持pcap文件类型，也即linux下 tcpdump -w生成的文件类型，或是wireshark “另存为”中的pcap类型，不支持pcapng等其他类型。







wireshark的安装目录下有分割和合并工具
下面的分割是按10W条一个文件，把一个文件分割成pcap文件。很多参数可选，比如-i是按秒分割。
"C:\Program Files\Wireshark\editcap.exe" -c 100000  -F pcap ping_OK_BB1.pcapng xx.pcap


合并
"C:\Program Files\Wireshark\merge.exe" -w destfile sourcefile1 sourcefile2 .....  

