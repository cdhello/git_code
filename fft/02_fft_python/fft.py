import numpy as np

def bit_reverse(n, LEN):
    i = 0;
    res = 0;

    while i < LEN:
        res = (((n >> i) & 1) << (LEN -1 - i)) + res
        i = i + 1
    return res

def dft(seq_in, in_interval, N):
    seq_out = [0] * N;

    k = 0;
    while k < N:
        i = 0;
        while i < N:
            phase = -2j*np.pi*k*i/N
            seq_out[k] = seq_out[k] + (np.e**phase) * seq_in[i * in_interval]
            i = i + 1;
        k = k + 1;

    return seq_out

def idft(seq_in, in_interval, N):
    seq_out = [0] * N;

    i = 0;
    while i < N:
        k = 0;
        while k < N:
            phase = 2j*np.pi*k*i/N
            seq_out[i] = seq_out[i] + (np.e**phase) * seq_in[k * in_interval] 
            k = k + 1;
        seq_out[i] = seq_out[i] / N
        i = i + 1;

    return seq_out

def get_rank(N):
    rank = 0;
    while (not(N & 1)):
        N = N >> 1
        rank = rank + 1
    return rank

def fft(seq_in):
    N = len(seq_in)
    rank = get_rank(N)

    sub_seq_len =  N >> rank
    num_of_odd_seqs = interval = 1 << rank
    outseq = []
    i = 0;
    while i < num_of_odd_seqs:
        seq_start = bit_reverse(i, rank)

        outseq = outseq + dft(seq_in[seq_start:], interval, sub_seq_len)
        i = i + 1

    r = 1
    while r <= rank:
        butter_fly_num = 1 << (rank - r)
        butter_fly_size = N/butter_fly_num

        for i in range(butter_fly_num):
            for j in range(butter_fly_size/2):
                even = outseq[i*butter_fly_size + j]
                odd = outseq[i*butter_fly_size + j + butter_fly_size/2]
                outseq[i*butter_fly_size + j] = even + odd * (np.e**(-2j*np.pi*j/butter_fly_size))
                outseq[i*butter_fly_size + j + butter_fly_size/2] = even + odd * (np.e**(-2j*np.pi*(j + butter_fly_size/2)/butter_fly_size))
        r = r+1

    return outseq

def ifft(seq_in):
    N = len(seq_in)
    rank = get_rank(N)

    sub_seq_len =  N >> rank
    num_of_odd_seqs = interval = 1 << rank
    outseq = []
    i = 0;
    while i < num_of_odd_seqs:
        seq_start = bit_reverse(i, rank)

        outseq = outseq + idft(seq_in[seq_start:], interval, sub_seq_len)
        i = i + 1

    r = 1
    while r <= rank:
        butter_fly_num = 1 << (rank - r)
        butter_fly_size = N/butter_fly_num

        for i in range(butter_fly_num):
            for j in range(butter_fly_size/2):
                even = outseq[i*butter_fly_size + j]/2
                odd = outseq[i*butter_fly_size + j + butter_fly_size/2]/2
                outseq[i*butter_fly_size + j] = even + odd * (np.e**(2j*np.pi*j/butter_fly_size))
                outseq[i*butter_fly_size + j + butter_fly_size/2] = even + odd * (np.e**(2j*np.pi*(j + butter_fly_size/2)/butter_fly_size))
        r = r+1

    return outseq

s1 = []
N = 6
for i in range (N):
    s1.append(complex(np.random.random(), np.random.random()))
S1 = list(np.fft.fft(s1))
S2 =  fft(s1)

for i in range(N):
    a = S1[i]-S2[i]
    print "%lf, %lf"%(a.real, a.imag)
print "############################"

s1 = []
N = 1536
for i in range (N):
    s1.append(complex(np.random.random(), np.random.random()))
S1 = list(np.fft.fft(s1))
S2 =  fft(s1)
sxx = ifft(list(np.fft.fft(s1)))
for i in range(N):
    a = S1[i]-S2[i]
    b = sxx[i] - s1[i]
    print "%lf, %lf- %lf, %lf"%(a.real, a.imag, b.real, b.imag)
