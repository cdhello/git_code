#pip install paramiko
#ssh side
import paramiko, time, socket, select
from socket import MSG_DONTWAIT
from urllib2 import urlopen
import re

class Codec():
    codebook = []

    def __init__(self):
        self.codebook = [152, 41, 37, 27, 79, 34, 86, 60, 243, 153, 5, 248, 203, 49, 195, 241, 183, 47, 253, 142, 236, 209, 30, 103, 255, 164, 170, 156, 104, 123, 99, 61, 184, 167, 96, 157, 186, 131, 50, 76, 144, 188, 181, 217, 158, 221, 17, 148, 107, 249, 78, 223, 235, 29, 12, 145, 54, 162, 24, 231, 150, 45, 4, 10, 199, 65, 171, 115, 168, 33, 177, 22, 112, 43, 82, 108, 66, 182, 74, 26, 58, 210, 198, 14, 68, 239, 222, 62, 70, 23, 233, 205, 129, 7, 119, 124, 13, 180, 208, 63, 52, 212, 2, 154, 128, 16, 200, 245, 84, 201, 185, 193, 116, 242, 120, 92, 118, 207, 178, 244, 19, 250, 36, 227, 204, 71, 101, 122, 160, 149, 127, 190, 55, 126, 110, 216, 202, 197, 192, 106, 161, 133, 176, 228, 219, 175, 80, 211, 57, 230, 20, 174, 166, 51, 102, 11, 113, 97, 125, 155, 39, 90, 215, 95, 238, 173, 67, 237, 234, 81, 98, 59, 151, 77, 91, 69, 135, 35, 141, 111, 206, 75, 87, 165, 213, 146, 137, 83, 15, 105, 246, 93, 117, 0, 21, 247, 40, 214, 89, 218, 121, 251, 88, 100, 8, 189, 220, 53, 169, 130, 139, 73, 32, 132, 229, 232, 196, 28, 194, 114, 136, 109, 226, 64, 138, 147, 9, 94, 6, 159, 140, 38, 172, 252, 134, 48, 191, 31, 85, 72, 1, 18, 240, 56, 163, 25, 44, 46, 254, 224, 187, 42, 225, 179, 3, 143]
        #self.decodebook = [193, 240, 102, 254, 62, 10, 228, 93, 204, 226, 63, 155, 54, 96, 83, 188, 105, 46, 241, 120, 150, 194, 71, 89, 58, 245, 79, 3, 217, 53, 22, 237, 212, 69, 5, 177, 122, 2, 231, 160, 196, 1, 251, 73, 246, 61, 247, 17, 235, 13, 38, 153, 100, 207, 56, 132, 243, 148, 80, 171, 7, 31, 87, 99, 223, 65, 76, 166, 84, 175, 88, 125, 239, 211, 78, 181, 39, 173, 50, 4, 146, 169, 74, 187, 108, 238, 6, 182, 202, 198, 161, 174, 115, 191, 227, 163, 34, 157, 170, 30, 203, 126, 154, 23, 28, 189, 139, 48, 75, 221, 134, 179, 72, 156, 219, 67, 112, 192, 116, 94, 114, 200, 127, 29, 95, 158, 133, 130, 104, 92, 209, 37, 213, 141, 234, 176, 220, 186, 224, 210, 230, 178, 19, 255, 40, 55, 185, 225, 47, 129, 60, 172, 0, 9, 103, 159, 27, 35, 44, 229, 128, 140, 57, 244, 25, 183, 152, 33, 68, 208, 26, 66, 232, 165, 151, 145, 142, 70, 118, 253, 97, 42, 77, 16, 32, 110, 36, 250, 41, 205, 131, 236, 138, 111, 218, 14, 216, 137, 82, 64, 106, 109, 136, 12, 124, 91, 180, 117, 98, 21, 81, 147, 101, 184, 197, 162, 135, 43, 199, 144, 206, 45, 86, 51, 249, 252, 222, 123, 143, 214, 149, 59, 215, 90, 168, 52, 20, 167, 164, 85, 242, 15, 113, 8, 119, 107, 190, 195, 11, 49, 121, 201, 233, 18, 248, 24]

    def code(self, data_in):
        data_out = ""
        i = 0
        while i < len(data_in):
            in_c = data_in[i]
            in_b = ord(in_c)
            out_b = self.codebook[in_b]
            out_c = chr(out_b)
            data_out = data_out + out_c
            i += 1

        return data_out

def get_remote_ip():
    #TO DO
    return ""

def get_ssh_channel():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='127.0.0.1', username='', password = "")
    channel = client.invoke_shell();
    return client, channel;

codec = Codec()

ser_add  = ""
ser_port = 15067;
xxx = 0;
while True:
    if xxx&0xff == 0:
        ser_add  = get_remote_ip();
    xxx += 1
    
    if len(ser_add) == 0:
        time.sleep(10)
        continue

    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
        result = sock.connect((ser_add, ser_port));
    except Exception as connnect_exception:
        print "connect %s:%u failed, reason:%s, continue"%(ser_add, ser_port, str(connnect_exception))
        time.sleep(10) #10 seconds
        continue

    print "connect %s:%u ok"%(ser_add, ser_port)
    
    sshclient, sshchannel = get_ssh_channel()

    read_needed = [sshchannel, sock]

    while read_needed:
        readable,writable,exceptional = select.select(read_needed, [], []);#select(rlist, wlist, xlist[, timeout])
        if sock in readable:
            command = sock.recv(1300)
            if len(command) == 0:
                print "tcp session is closed."
                sshclient.close()
                read_needed.remove(sock)
                break;
            sshchannel.send(codec.code(command))

        elif sshchannel in readable:  #something maybe changed(i.e. closed), one select do one thing
            sshout = sshchannel.recv(1300)
            if len(sshout) == 0:
                print "ssh session is closed."
                sock.close()
                read_needed.remove(sshchannel)
                break;
            sock.send(codec.code(sshout), MSG_DONTWAIT)
