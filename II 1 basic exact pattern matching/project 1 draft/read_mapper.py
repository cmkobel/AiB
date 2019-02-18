from dollarsign import dollarsign_matches
from fasta_parser import parse_fasta
from fastq_parser import parse_fastq

reads_file = 'data/reads.fastq'
refs_file = 'data/ref.fa'

# reads (fastq) in outer loop
for read in parse_fastq(reads_file):
    print(read)

    for reference in parse_fasta()