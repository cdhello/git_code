import re
import os,sys
import numpy as np

def check():
    t = []
    tfile = open("t.txt", "r")
    line = tfile.readline()
    while line:
        #real = %lf, imag = %lf
        res = re.search("real = (.*), imag = (.*)", line);
        if res:
            x = complex(float(res.group(1)), float(res.group(2)))
            t.append(x)
        line = tfile.readline()
    tfile.close()

    k = []
    kfile = open("k.txt", "r")
    line = kfile.readline()
    while line:
        #real = %lf, imag = %lf
        res = re.search("real = (.*), imag = (.*)", line);
        if res:
            x = complex(float(res.group(1)), float(res.group(2)))
            k.append(x)
        line = kfile.readline()
    kfile.close()
    
    t2 = []
    t2file = open("t2.txt", "r")
    line = t2file.readline()
    while line:
        #real = %lf, imag = %lf
        res = re.search("real = (.*), imag = (.*)", line);
        if res:
            x = complex(float(res.group(1)), float(res.group(2)))
            t2.append(x)
        line = t2file.readline()
    t2file.close()
    L = len(t)

    libk = list(np.fft.fft(t))

    libkfile = open("libk.txt", "w")
    diff = open("result.txt","w")
    for i in range(L):
        libkfile.write("real = %lf, imag = %lf\r\n"%(libk[i].real, libk[i].imag));

        fftdelta = libk[i] - k[i]
        ifftdelta = t2[i] - t[i]
        diff.write( "fftdelta: %+.6lf%+.6lfj"%(fftdelta.real, fftdelta.imag))
        diff.write( "-----------------ifftdelta: %+.6lf%+.6lfj\r\n"%(ifftdelta.real, ifftdelta.imag));
    libkfile.close()
    diff.close()

if __name__ == '__main__':

    os.system("gcc fft.c -lm -o fft.out")
    if len(sys.argv) > 1:
        N = int(sys.argv[1])
        if 0 < N and N <= 4096:
            os.system("./fft.out %d"%N)
            check()
        else:
            print "fft size should in (0, 4096]"
    else:
        print "need fft size"