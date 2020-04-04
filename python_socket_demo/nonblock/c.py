import sys
import socket
import time
import select
import logging

SEND_BUF_SIZE = 256
RECV_BUF_SIZE = 256
srcfilename = "a.pptx"

def run():
    print "hi, i m client";
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%d %b %Y %H:%M:%S',  
                    filename='client.log',  
                    filemode='w') 

    global srcfilename

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    ser_add  = "10.140.162.26";
    ser_port = 1567;

    try:
        result = s.connect((ser_add, ser_port));
    except:
        print "connect failed, return"
        return
    else:
        print "connect ok"

    if len(sys.argv)<2:
        pass
    else:
        srcfilename = sys.argv[1]

    ltime = time.localtime(time.time())
    print "time: %d:%d:%d"%(ltime.tm_hour,ltime.tm_min,ltime.tm_sec)

    try:
        srcfile = open(srcfilename, "rb")
    except:
        print "There is no file named '%s'. return"%(srcfilename)
        s.close();
        return
    else:
        print "File '%s' is opend"%srcfilename
    outputfile = open("output.txt","wb")

    timestart = time.time() 
    
    s.setblocking(False)  
    buf = "";
    rneeded = [s]
    wneeded = [s]
    bytesCount = 0;
    
    while(1):
        if 0 == len(buf) and len(wneeded) > 0:
            buf = srcfile.read(SEND_BUF_SIZE)
            logging.info("readdata from srcFile.%u"%(len(buf)))
            if 0 == len(buf):
                s.shutdown(socket.SHUT_WR);
                wneeded.remove(s)
                print "data is sent over."
                
        
        readable,writable,exceptional = select.select(rneeded, wneeded, [])
        if len(writable)>0:
            i = s.send(buf); # return the length of the sent data.
            buf = buf[i:];
            logging.info("sent data %u, buf len:%u"%(i, len(buf)))
            bytesCount += i;

        if len(readable)>0:
            recv_data = s.recv(RECV_BUF_SIZE);
            logging.info("recv data %u"%(len(recv_data)))
            if len(recv_data)>0:
                outputfile.write(recv_data);
            else:
                print "recv over"
                break;
                
    timeend = time.time()  
    print "seconds: %lf, bytes: %u, rate: %lf(KBs)"%(timeend - timestart, bytesCount, (bytesCount>>10)/(timeend - timestart));

    ltime = time.localtime(time.time())
    print "time :%d:%d:%d"%(ltime.tm_hour,ltime.tm_min,ltime.tm_sec)
    outputfile.close()
    srcfile.close()
    s.close();

    print "client bye bye"
    
if __name__ == '__main__':
    run()

