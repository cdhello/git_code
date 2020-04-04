import socket
import select
import logging

BUF_SIZE = 256
def run():
    print "server started."

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    serveradd  = "0.0.0.0"; #INADDR_ANY
    myport = 1567;
    s.bind((serveradd, myport));
    
    print "Listening."
    s.listen(1);

    clientsock,caddr=s.accept();
    print "A client coming,", caddr;
    clientsock.setblocking(False)
    buf = "";
    readneeded = [clientsock]
    writeneeded = [clientsock];
    
    logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                    datefmt='%d %b %Y %H:%M:%S',  
                    filename='server.log',  
                    filemode='w')  
    
    while (1):
        if len(readneeded) < 1 and 0 == len(buf):
            print "trans over.";
            clientsock.close();
            break;

        readable,writable,exceptional = select.select(readneeded, writeneeded, [])
        if len(readable)>0 and readable[0] == clientsock and len(buf)<BUF_SIZE:
            recv_data = clientsock.recv(BUF_SIZE-len(buf));
            if (len(recv_data)>0):
                buf+=recv_data
            else:
                print "client sent over."
                readneeded.remove(clientsock)
            #print "recv %u, len of buf %u"%(len(recv_data),len(buf))
            logging.info("recv %u, len of buf %u"%(len(recv_data),len(buf)))
                
        if len(writable)>0 and len(buf)>0:
            i = clientsock.send(buf);
            buf = buf[i:];
            #print "sent %u, len of buf %u"%(i,len(buf))
            logging.info("sent %u, len of buf %u"%(i,len(buf)))

    s.close();
    print "bye bye"

if __name__ == '__main__':
    run()

