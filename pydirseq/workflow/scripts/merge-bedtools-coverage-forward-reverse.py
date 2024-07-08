#!/usr/bin/env python

import sys
import os
import pandas as pd

COLS = ['gene_id', 'contig', 'type', 'start', 'end', 'strand', 'average_depth', 
        'median_depth', 'trimmed_mean_depth', 'coverage']

def main():
    if len(sys.argv) != 3:
        mes = '[INFO] Usage: python {} <bedtools_coverage.forward.tsv> <bedtools_coverage.reverse.tsv>\n'
        sys.stderr.write(mes.format(os.path.basename(sys.argv[0])))
        sys.exit(1)

    f1 = sys.argv[1]
    f2 = sys.argv[2]

    df1 = pd.read_csv(f1, sep='\t', header=0) 
    df2 = pd.read_csv(f2, sep='\t', header=0)


    df_merged = df1.merge(df2, on=COLS[:6], how='outer', suffixes=['_forward', '_reverse'])
    df_merged.to_csv('/dev/stdout', sep='\t', header=True, index=False, na_rep='NA')

if __name__ == '__main__':
    main()
