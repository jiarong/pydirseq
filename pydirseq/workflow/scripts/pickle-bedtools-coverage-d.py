#!/usr/bin/env python

import sys
import os
try:
    import cPickle as pickle
except ImportError as e:
    import pickle
from collections import defaultdict


header_gff = ['contig', 'source', 'type', 'start', 'end', 'score', 'strand', 'phase', 'attribute']
header = header_gff + ['position', 'depth']

def main():
    if len(sys.argv) != 3:
        mes = '[INFO] Usage: python {} <SS.bedtools_coverage_d.tsv> <file.pickle>\n'
        sys.stderr.write(mes.format(os.path.basename(sys.argv[0])))
        sys.exit(1)

    tab = sys.argv[1]
    outfile = sys.argv[2]
    if tab == '-':
        tab = '/dev/stdin'

    d = defaultdict(lambda: defaultdict(int))

    with open(tab) as fh:
        for line in fh:
            if line.startswith('#'):
                continue

            #lst = line.rstrip().rsplit('\t')
            #key_str = '\t'.join(tup)
            #pos = int(lst[9])
            #depth = int(lst[10])

            key_str, pos, depth = line.rstrip().rsplit('\t', 2)
            d[key_str][int(pos)] = int(float(depth))

    d = dict(d)  # make lambda pickle-able
    with open(outfile, 'wb') as fwb:
        pickle.dump(d, fwb)

if __name__ == '__main__':
    main()
