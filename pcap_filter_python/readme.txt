����ű�����һ��pcap �ļ��������ư���Ҫ�ı������Ϊһ��pcap�ļ���

����ű���ͷ���������ǵĵ����ã������б�һ�����أ�
Allow_msglist������б��������Ϣ��������ָ��Ҫ���µġ�����Ϊ�ա�
Deny_msglist������б������Ϣ��������ָ������Ҫ�ġ�����Ϊ�ա�
Is_allow_others�����ֵΪTrue��False�� ��ʾ���ĳ����Ϣ�Ȳ�����Allow_msglistҲ������Is_allow_others����Ҫ���滹��Ҫɾ����

������������� ��python filter_pcap.py abc.pcap�������ɵ�pcap�ļ�����Ϊxxabc.pcap��xxabc.pcap�ļ�������abc.pcap�г���UlData_SyncInd, DlData_SubfrTypeReq��������Ŀ��
Allow_msglist = [ ]
Deny_msglist = [UlData_SyncInd, DlData_SubfrTypeReq]
Is_allow_others = True

Ŀǰ��֧��pcap�ļ����ͣ�Ҳ��linux�� tcpdump -w���ɵ��ļ����ͣ�����wireshark �����Ϊ���е�pcap���ͣ���֧��pcapng���������͡�







wireshark�İ�װĿ¼���зָ�ͺϲ�����
����ķָ��ǰ�10W��һ���ļ�����һ���ļ��ָ��pcap�ļ����ܶ������ѡ������-i�ǰ���ָ
"C:\Program Files\Wireshark\editcap.exe" -c 100000  -F pcap ping_OK_BB1.pcapng xx.pcap


�ϲ�
"C:\Program Files\Wireshark\merge.exe" -w destfile sourcefile1 sourcefile2 .....  

