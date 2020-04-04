import sys
import socket
import time   
import logging

BUF_SIZE = 256
srcfilename = "a.pptx"

def run():
    print "hi, i m client";
    
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
    bytesCount = 0;
    bytesCount2 = 0
    while(1):
        data2send=srcfile.read(BUF_SIZE) 
        if (0 == len(data2send)):
            s.shutdown(socket.SHUT_WR); #inform server
            break;
        bytesCount2+=len(data2send)
        
        #logging.info("read %u bytes"%(len(data2send)))
        #s.send(data2send); # return the length of the sent data.
        s.sendall(data2send); # try to send all of the data, return none, else raise a exception
        recv_data = s.recv(BUF_SIZE);
        logging.info("read %u, write %u "%(len(data2send), len(recv_data)))
        outputfile.write(recv_data);
        bytesCount += len(recv_data);
        
    try:
        recv_data = s.recv(BUF_SIZE);
    except:
        print "recv failed."    	
        
    while(1):
        if (0 == len(recv_data)):
            break;
        logging.info("(last data) write %u "%( len(recv_data)))
        outputfile.write(recv_data);
        bytesCount += len(recv_data);
        recv_data = s.recv(BUF_SIZE);
        
    timeend = time.time()  
    print "seconds: %lf, bytes: %u, rate: %lf(KBs)"%(timeend - timestart, bytesCount, (bytesCount>>10)/(timeend - timestart));
    print "2 byes %u"%bytesCount2

    ltime = time.localtime(time.time())
    print "time :%d:%d:%d"%(ltime.tm_hour,ltime.tm_min,ltime.tm_sec)
    outputfile.close()
    srcfile.close()
    s.close();

    print "client bye bye"
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,  
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                datefmt='%d %b %Y %H:%M:%S',  
                filename='client.log',  
                filemode='w')
    run()
 