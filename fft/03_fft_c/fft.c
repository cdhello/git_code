//gcc dft.c -lm
#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct _complex {
    double real;
    double imag;
}complex;

int dft(complex seq_in[], unsigned int in_interval, complex seq_out[], unsigned int N) {
    unsigned int i;
    unsigned int k;
    double angle;
    double real;
    double imag;
    complex x;

    memset(seq_out, 0, sizeof(complex) * N);

    for (k = 0; k < N; k++) {
        for (i = 0; i < N; i++) {
            angle = -2 * M_PI *k * i/N;
            real = cos(angle);
            imag = sin(angle);
            x = seq_in[i * in_interval];

            seq_out[k].real += x.real * real - x.imag * imag;
            seq_out[k].imag += x.real * imag + x.imag * real;
        }
    }

    return 0;
}

int idft(complex seq_in[], unsigned int in_interval, complex seq_out[], unsigned int N) {
    unsigned int i;
    unsigned int k;
    double angle;
    double real;
    double imag;
    complex x;

    memset(seq_out, 0, sizeof(complex) * N);

    for (i = 0; i < N; i++) {
        for (k = 0; k < N; k++) {
            angle = 2 * M_PI * k * i/N;
            real = cos(angle);
            imag = sin(angle);
            x = seq_in[k * in_interval];

            seq_out[i].real += x.real * real - x.imag * imag;
            seq_out[i].imag += x.real * imag + x.imag * real;
        }

        seq_out[i].real = seq_out[i].real / N;
        seq_out[i].imag = seq_out[i].imag / N;
    }

    return 0;
}

unsigned int get_rank(unsigned int N) {
    unsigned int rank = 0;
    while (! ((N>>rank) & 1)) {
        rank ++;
    }
    return rank;
}

unsigned int bit_reverse(unsigned int n, unsigned int LEN) {
    unsigned int res = 0;
    unsigned int i;

    for (i = 0; i < LEN; i++) {
        res += (((n >> i) & 1) << (LEN -1 - i));
    }

    return res;
}

int fft(complex seq_in[], complex seq_out[], unsigned int N) {
    unsigned int rank = get_rank(N);
    unsigned int dft_seq_len;
    unsigned int num_of_dft_seqs;
    unsigned int dft_elem_interval;
    unsigned int i, k, r, j;

    unsigned int butterfly_num;
    unsigned int butterfly_size;
    unsigned int butterfly_size_half;

    complex even;
    complex odd;

    double angle;
    double real;
    double imag;
    double cosine;
    double sine;

    dft_seq_len =  N >> rank;
    num_of_dft_seqs = dft_elem_interval = (1 << rank);

    memset(seq_out, 0, sizeof(complex) * N);
    for (i = 0; i < num_of_dft_seqs; i++) {
        dft(&seq_in[bit_reverse(i, rank)], dft_elem_interval, &seq_out[i * dft_seq_len], dft_seq_len);
    }

    for (r = 1; r <= rank; r++) {
        butterfly_num = 1 << (rank - r);
        butterfly_size = N/butterfly_num;
        butterfly_size_half = butterfly_size >> 1;

        for (i = 0; i < butterfly_num; i++) {
            for (j = 0; j < butterfly_size_half; j++){

                even = seq_out[i*butterfly_size + j];
                odd = seq_out[i*butterfly_size + j + butterfly_size_half];
                angle = -2* M_PI * j / butterfly_size;
                cosine = cos(angle);
                sine = sin(angle);
                real = odd.real * cosine - odd.imag * sine;
                imag = odd.real * sine + odd.imag * cosine;

                //outseq[i*butterfly_size + j] = even + odd * (np.e**(-2j*np.pi*j/butterfly_size));
                seq_out[i*butterfly_size + j].real = even.real + real;
                seq_out[i*butterfly_size + j].imag = even.imag + imag;

                //outseq[i*butterfly_size + j + butterfly_size_half] = even + odd * (np.e**(-2j*np.pi*(j + butterfly_size_half)/butterfly_size));
                //-2*pi*(j + butterfly_size_half)/butterfly_size = -2*pi*j/butterfly_size - 2*pi * butterfly_size_half/butterfly_size
                //                                               = -2*pi*j/butterfly_size - pi
                //cos(a - pi) = -cos(a) and sin(a - pi) = -sin(a)
                seq_out[i*butterfly_size + j + butterfly_size_half].real = even.real - real;
                seq_out[i*butterfly_size + j + butterfly_size_half].imag = even.imag - imag;
            }
        }
    }
    return 0;
}

int ifft(complex seq_in[], complex seq_out[], unsigned int N) {
    unsigned int rank = get_rank(N);
    unsigned int dft_seq_len;
    unsigned int num_of_dft_seqs;
    unsigned int dft_elem_interval;
    unsigned int i, k, r, j;

    unsigned int butterfly_num;
    unsigned int butterfly_size;
    unsigned int butterfly_size_half;

    complex even;
    complex odd;

    double angle;
    double real;
    double imag;
    double cosine;
    double sine;

    dft_seq_len =  N >> rank;
    num_of_dft_seqs = dft_elem_interval = (1 << rank);

    memset(seq_out, 0, sizeof(complex) * N);
    for (i = 0; i < num_of_dft_seqs; i++) {
        idft(&seq_in[bit_reverse(i, rank)], dft_elem_interval, &seq_out[i * dft_seq_len], dft_seq_len);
    }

    for (r = 1; r <= rank; r++) {
        butterfly_num = 1 << (rank - r);
        butterfly_size = N/butterfly_num;
        butterfly_size_half = butterfly_size >> 1;

        for (i = 0; i < butterfly_num; i++) {
            for (j = 0; j < butterfly_size_half; j++){

                even = seq_out[i*butterfly_size + j];
                odd = seq_out[i*butterfly_size + j + butterfly_size_half];
                angle = 2* M_PI * j / butterfly_size;
                cosine = cos(angle);
                sine = sin(angle);
                real = odd.real * cosine - odd.imag * sine;
                imag = odd.real * sine + odd.imag * cosine;

                seq_out[i*butterfly_size + j].real = (even.real + real)/2;
                seq_out[i*butterfly_size + j].imag = (even.imag + imag)/2;

                seq_out[i*butterfly_size + j + butterfly_size_half].real = (even.real - real)/2;
                seq_out[i*butterfly_size + j + butterfly_size_half].imag = (even.imag - imag)/2;
            }
        }
    }
    return 0;
}

#define N 4096
complex seq_k[N];
complex seq_t[N];
int main(int argc, char *argv[])
{
    int i;
    int fft_size = N;
    FILE *fp = NULL;

    if (argc > 1) {
        sscanf(argv[1], "%u", &fft_size);
    }

    printf("fft_size = %u\r\n", fft_size);

    srand(time(0));
    for (i = 0; i < fft_size; i++) {
        seq_t[i].real = (double)rand();
        seq_t[i].imag = (double)rand();
    }

    fp = fopen("t.txt", "w");
    for (i = 0; i < fft_size; i++) {
        fprintf(fp, "real = %lf, imag = %lf\r\n", seq_t[i].real, seq_t[i].imag);
    }
    fclose(fp);

    fft(seq_t, seq_k, fft_size);
    //dft(seq_t, 1, seq_k, fft_size);
    fp = fopen("k.txt", "w");
    for (i = 0; i < fft_size; i++) {
        fprintf(fp, "real = %lf, imag = %lf\r\n", seq_k[i].real, seq_k[i].imag);
    }
    fclose(fp);

    ifft(seq_k, seq_t, fft_size);
    //idft(seq_k, 1, seq_t, fft_size);
    fp = fopen("t2.txt", "w");
    for (i = 0; i < fft_size; i++) {
        fprintf(fp, "real = %lf, imag = %lf\r\n", seq_t[i].real, seq_t[i].imag);
    }
    fclose(fp);

    return 0;
}
