[![DOI](https://zenodo.org/badge/825543365.svg)](https://zenodo.org/doi/10.5281/zenodo.12683196)

# pydirseq

pydirseq provides gene-wise coverage for metaT and metaG reads mapped genomes/contigs

# Installation
```
git clone git@github.com:jiarong/pydirseq.git
cd pydirseq
mamba env create -f requirements.yaml
conda activate pydirseq
python -m pip install -e .
```

# Usage

## Example
```
# input files required:
#   1) bam file from read mapping to genome/contigs
#   2) gff file from ORF prediction tools such as prodigal
pydirseq run --bam data/final.bam --gff data/combined_reference.gff all
```
See the final outupt file at `pydirseq.out/results/SS.final.tsv`.


## Full help
```
$ pydirseq run -h
Usage: pydirseq run [OPTIONS] [SNAKE_ARGS]...

  Run pydirseq

Options:
  --bam PATH                    Input bam file  [required]
  --gff PATH                    Input gff file  [required]
  --output PATH                 Output directory  [default: pydirseq.out]
  --configfile TEXT             Custom config file [default:
                                (outputDir)/config.yaml]
  --threads INTEGER             Number of threads to use  [default: 1]
  --profile TEXT                Snakemake profile to use
  --use-conda / --no-use-conda  Use conda for Snakemake rules  [default: use-
                                conda]
  --conda-prefix PATH           Custom conda env directory
  --snake-default TEXT          Customise Snakemake runtime args  [default:
                                --printshellcmds, --nolock, --show-failed-
                                logs]
  -h, --help                    Show this message and exit.

  CLUSTER EXECUTION:
  pydirseq run ... --profile [profile]
  For information on Snakemake profiles see:
  https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles

  RUN EXAMPLES:
  Required:           pydirseq run --bam [file] --gff [file]
  Specify threads:    pydirseq run ... --threads [threads]
  Disable conda:      pydirseq run ... --no-use-conda
  Change defaults:    pydirseq run ... --snake-default="-k --nolock"
  Add Snakemake args: pydirseq run ... --dry-run --keep-going --touch
  Specify targets:    pydirseq run ... all | print_targets
  Available targets:
      all             Run everything (default)
      print_targets   List available targets
```

# Cite
Citation is to be added
