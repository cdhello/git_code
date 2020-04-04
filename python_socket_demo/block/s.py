import socket
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

    while (1):
        recv_data = clientsock.recv(BUF_SIZE);
        if (0 == len(recv_data)):
            clientsock.close();
            print "client gone."
            break
        
        #clientsock.send(recv_data); # return the length of the sent data.
        #print "recvd ",len(recv_data)," byte(s)"
        
        clientsock.sendall(recv_data); # try to send all of the data, return none, else raise a exception
        logging.info("recv and send %u bytes"%(len(recv_data)))

    s.close();
    print "bye bye"

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,  
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
                datefmt='%d %b %Y %H:%M:%S',  
                filename='server.log',  
                filemode='w')
    run() 
 

