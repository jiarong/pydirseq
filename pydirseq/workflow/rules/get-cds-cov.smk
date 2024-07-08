
Bam = config['args']['bam']
Gff = config['args']['gff']
#Bam=/users/PAA0034/gjr/lab/jiarong/project/mobile-gene/metat/nova-only.wkdir/714E11014metaG_FD_JGI/final_bam/final.bam
#Gff=/users/PAA0034/gjr/lab/jiarong/project/mobile-gene/metat/nova-only.wkdir/714E11014metaG_FD_JGI/annotate/combined_reference.gff
Output = config['args']['output']
Read1_flag='-F128'             #account for read1 in pair, as well as single reads mapping
Read2_flag='-f128'
Sam_filter_flags='-F0x100 -F0x800'
#Bedtools_type_flag='-hist'
#Bedtools_type_flag='-count'  # default
Bedtools_type_flag='-d'
Scriptdir= dirs['scripts']
Resultdir= dirs['results']
Logdir = dirs['logs']

Lab='SS'

rule prep_gff:
    input:
        gff = Gff,
        bam = Bam
    output: 
        gff = f'{Resultdir}/{Lab}.sorted.gff',
        lenfile = f'{Resultdir}/{Lab}.contig2len.tsv'
    log: os.path.join(dirs['logs'], 'prep_gff.log')
    shell:
        '''
	cd {Resultdir}
        sed '/^##FASTA$/,$d' {Gff} > {Lab}.no_fasta.gff
        samtools idxstats {Bam} |cut -f1,2 |grep -v '^*' > {Lab}.contig2len.tsv
        grep -v '^#' {Lab}.no_fasta.gff |cut -f1 |sort |uniq |grep -vFw -f /dev/stdin {Lab}.contig2len.tsv |cut -f1 > {Lab}.contig.feature_less.list
        awk -v FS=$'\t' -v OFS=$'\t' '{{print $1, "dirseq", "misc_RNA", "1", "2", ".", "+", "0", "ID="$1"_dummy_feature"}}' {Lab}.contig.feature_less.list > {Lab}.contig.feature_less.add_dummy_feature.gff
        cat {Lab}.contig.feature_less.add_dummy_feature.gff {Lab}.no_fasta.gff | bedtools sort -i /dev/stdin -faidx {Lab}.contig2len.tsv > {Lab}.sorted.gff
        '''

rule get_cov_dict_f1: 
    input:
        bam = Bam,
        lenfile = f'{Resultdir}/{Lab}.contig2len.tsv',
        gff = f'{Resultdir}/{Lab}.sorted.gff'
    output: f'{Resultdir}/{Lab}.f1.d.pickle'
    shell:
        '''
	cd {Resultdir}
        samtools view {Sam_filter_flags} -u {Read1_flag} {input.bam} | bedtools coverage -sorted -g {input.lenfile} -b /dev/stdin -a {input.gff} -s {Bedtools_type_flag} |  python {Scriptdir}/pickle-bedtools-coverage-d.py - {Lab}.f1.d.pickle
        '''

rule get_cov_dict_f2: 
    input:
        bam = Bam,
        lenfile = f'{Resultdir}/{Lab}.contig2len.tsv',
        gff = f'{Resultdir}/{Lab}.sorted.gff'
    output: f'{Resultdir}/{Lab}.f2.d.pickle'
    shell:
        '''
	cd {Resultdir}
        samtools view {Sam_filter_flags} -u {Read2_flag} {input.bam} | bedtools coverage -sorted -g {input.lenfile} -b /dev/stdin -a {Lab}.sorted.gff -s {Bedtools_type_flag} | python {Scriptdir}/pickle-bedtools-coverage-d.py - {Lab}.f2.d.pickle
        '''

rule get_cov_dict_r1: 
    input:
        bam = Bam,
        lenfile = f'{Resultdir}/{Lab}.contig2len.tsv',
        gff = f'{Resultdir}/{Lab}.sorted.gff'
    output: f'{Resultdir}/{Lab}.r1.d.pickle'
    shell:
        '''
	cd {Resultdir}
        samtools view {Sam_filter_flags} -u {Read1_flag} {input.bam} | bedtools coverage -sorted -g {input.lenfile} -b /dev/stdin -a {input.gff} -S {Bedtools_type_flag} | python {Scriptdir}/pickle-bedtools-coverage-d.py - {Lab}.r1.d.pickle
        '''

rule get_cov_dict_r2:
    input:
        bam = Bam,
        lenfile = f'{Resultdir}/{Lab}.contig2len.tsv',
        gff = f'{Resultdir}/{Lab}.sorted.gff'
    output: f'{Resultdir}/{Lab}.r2.d.pickle'
    shell:
        '''
	cd {Resultdir}
        samtools view {Sam_filter_flags} -u {Read2_flag} {input.bam} | bedtools coverage -sorted -g {input.lenfile} -b /dev/stdin -a {input.gff} -S {Bedtools_type_flag} | python {Scriptdir}/pickle-bedtools-coverage-d.py - {Lab}.r2.d.pickle
        '''

rule merge_cov_forward:
    input:
        f1 = f'{Resultdir}/{Lab}.f1.d.pickle',
        r2 = f'{Resultdir}/{Lab}.r2.d.pickle'
    output: f'{Resultdir}/{Lab}.forward.tsv'
    shell:
        '''
	cd {Resultdir}
        python {Scriptdir}/merge-bedtools-coverage-d.py {input.f1} {input.r2} > {output}
        '''

rule merge_cov_reverse:
    input:
        f2 = f'{Resultdir}/{Lab}.f2.d.pickle',
        r1 = f'{Resultdir}/{Lab}.r1.d.pickle'
    output: f'{Resultdir}/{Lab}.reverse.tsv'
    shell:
        '''
	cd {Resultdir}
        python {Scriptdir}/merge-bedtools-coverage-d.py {input.f2} {input.r1} > {output}
        '''

rule merge_cov_both:
    input:
        f1 = f'{Resultdir}/{Lab}.f1.d.pickle',
        r2 = f'{Resultdir}/{Lab}.r2.d.pickle',
        f2 = f'{Resultdir}/{Lab}.f2.d.pickle',
        r1 = f'{Resultdir}/{Lab}.r1.d.pickle'
    output: f'{Resultdir}/{Lab}.both.tsv'
    shell:
        '''
	cd {Resultdir}
        python {Scriptdir}/merge-bedtools-coverage-d.py {input.f1} {input.r2} {input.f2} {input.r1} > {output}
        '''

rule finalize:
    input:
        f = f'{Resultdir}/{Lab}.forward.tsv',
        r = f'{Resultdir}/{Lab}.reverse.tsv',
        both = f'{Resultdir}/{Lab}.both.tsv'
    #output: f'{Resultdir}/{Lab}.final.tsv'
    output: touch('{Resultdir}/done.get_cds_cov')
    shell:
        '''
	cd {Resultdir}
        python {Scriptdir}/merge-bedtools-coverage-forward-reverse.py {input.f} {input.r} {input.both} > {Lab}.final.tsv
        # clean up
        # rm -f {Lab}.*.pickle $Lab.no_fasta.gff {Lab}.contig2len.tsv {Lab}.contig.feature_less.list {Lab}.contig.feature_less.add_dummy_feature.gff  {Lab}.sorted.gff
        '''

