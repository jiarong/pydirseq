#!/usr/bin/env python

import sys
import os
try:
    import cPickle as pickle
except ImportError as e:
    import pickle
import numpy as np

"""

https://bedtools.readthedocs.io/en/latest/content/tools/coverage.html//bedtools.readthedocs.io/en/latest/content/tools/coverage.html

cat A.bed
chr1  0   100
chr1  100 200
chr2  0   100

$ cat B.bed
chr1  10  20
chr1  20  30
chr1  30  40
chr1  100 200

$ bedtools coverage -a A.bed -b B.bed
chr1  0   100  3  30  100 0.3000000
chr1  100 200  1  100 100 1.0000000
Chr2  0   100  0  0   100 0.0000000

---------------
cat A.bed
chr1  0   100 b1  1  +
chr1  100 200 b2  1  -
chr2  0   100 b3  1  +

$ cat B.bed
chr1  10  20  a1  1  -
chr1  20  30  a2  1  -
chr1  30  40  a3  1  -
chr1  100 200 a4  1  +

$ bedtools coverage  -a A.bed -b B.bed -hist
chr1  0   100 b1  1  +  0  70  100  0.7000000
chr1  0   100 b1  1  +  1  30  100  0.3000000
chr1  100 200 b2  1  -  1  100 100  1.0000000
chr2  0   100 b3  1  +  0  100 100  1.0000000
all   0   170 300 0.5666667
All   1   130 300 0.4333333

-------------

cat A.bed
chr1  0  10

$ cat B.bed
chr1  0  5
chr1  3  8
chr1  4  8
chr1  5  9

$ bedtools coverage -a A.bed -b B.bed -d
chr1  0  10  B  1  1
chr1  0  10  B  2  1
chr1  0  10  B  3  1
chr1  0  10  B  4  2
chr1  0  10  B  5  3
chr1  0  10  B  6  3
chr1  0  10  B  7  3
chr1  0  10  B  8  3
chr1  0  10  B  9  1
Chr1  0  10  B  10 0

"""
#ATT: "bedtools coverage -d" produce huge tables
# dirseq headers: contig, type, start, end, strand, forward_average_coverage, reverse_average_coverage, annotation, ID

def trimmed_mean_calc(lst):
    #arr = np.array(lst)
    #up_lim = np.percentile(arr, 90)
    #low_lim = np.percentile(arr, 10)
    #arr1 = arr[(arr>=low_lim) & (arr<up_lim)]

    lst_sorted = sorted(lst)
    size = len(lst)
    trimmed_size = int(size * 0.1)
    lst_sorted_trimmed = lst_sorted[trimmed_size: -1*trimmed_size]
    return np.mean(lst_sorted_trimmed)
    

def main():
    if len(sys.argv) < 2:
        mes = '[INFO] python {} <SS.f1.tsv> <SS.r2.tsv> ..\n'
        sys.stderr.write(mes.format(os.path.basename(sys.argv[0])))
        sys.exit(1)

    tabs = sys.argv[1:]

    lis = []
    for tab in tabs:
        with open(tab, 'rb') as fh:
            d = pickle.load(fh)
            lis.append(d)

    d1 = lis[0]
    for d in lis[1:]:
        for l1 in d:
            #print(l1)
            for l2 in d[l1]:
                d1[l1][l2] += d[l1][l2]

    mes = 'gene_id\tcontig\ttype\tstart\tend\tstrand\taverage_depth\tmedian_depth\ttrimmed_mean_depth\tcoverage\n'
    sys.stdout.write(mes)
    for l1 in d1:
        #print(list(d1[l1].values()))
        arr = np.array(list(d1[l1].values()))
        average_depth = np.mean(arr)
        median_depth = np.median(arr)
        trimmed_mean_depth = trimmed_mean_calc(arr)
        coverage = sum(arr >= 1)/len(arr)
        
        contig, tool, type, start, end, score, strand, phase, attr = l1.split('\t')
        _d = dict([i.split('=', 1) for i in attr.strip('"').rstrip(';').split(';')])
        gene_id = _d['ID']
        mes = f'{gene_id}\t{contig}\t{type}\t{start}\t{end}\t{strand}\t{average_depth}\t{median_depth}\t{trimmed_mean_depth}\t{coverage}\n'
        sys.stdout.write(mes)
        
        #for l2 in d1[l1]:
        #    mes = f'{l1}\t{l2}\t{d1[l1][l2]}\n'
        #    sys.stdout.write(mes)

if __name__ == '__main__':
    main()
