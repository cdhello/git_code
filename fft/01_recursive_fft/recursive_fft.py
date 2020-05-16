import random
import time
import math

def dft(seq_in):

    N = len(seq_in)

    seq_out = [0] * N
    for k in range(N):
        for i in range(N):
            angle = -2j * math.pi * k * i / N
            seq_out[k] = seq_out[k] + (math.e**angle) * seq_in[i]
    return seq_out

def recursive_fft(input):   #Decimation-in-time
    N = len(input)

    if N < 2:
        return input

    if N %2 != 0:
        return dft(input)

    evens = input[0::2] #[start:stop:step] 
    odds  = input[1::2]

    evens_freq = recursive_fft(evens)
    odds_freq = recursive_fft(odds)

    output = [0] * N
    for i in range(N):
        output[i] = evens_freq[i%(N/2)] + odds_freq[i%(N/2)] * (math.e**(-2j * math.pi * i / N))

    return output

#########################################################################################################

LOOP = 500
N = 128

s = []
for i in range(N):
    s.append(random.random())

print "Calculate N=%u size for %u times:"%(N, LOOP)
timestart = time.time()
i = 0
while (i < LOOP):
    recursive_fft(s)
    i = i + 1
timeend = time.time()  
print "recursive fft cost %lf seconds"%(timeend - timestart);

timestart = time.time()
i = 0
while (i < LOOP):
    dft(s)
    i = i + 1
timeend = time.time()  
print "dft cost %lf seconds"%(timeend - timestart);

import numpy.fft as fft
libk = list(fft.fft(s))
k = recursive_fft(s)

i = 0
while i < N:
    diff = libk[i]-k[i]
    print "%lf%+lf"%(diff.real,diff.imag)
    i = i + 1