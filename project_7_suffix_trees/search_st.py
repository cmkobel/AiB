from st import suffixtree
from parsers import parse_fasta, parse_fastq
#import sys # for argv



for genome in parse_fasta('data/seqs.fasta'):
    
    for read in parse_fastq('data/reads.fastq'):

        st = suffixtree(genome['sequence'])

        for match in st.find_positions(read['sequence']):

            print(f"\
{read['sequence']}\t\
0\t{genome['title']}\t\
{match}\t\
0\t\
{len(read['sequence'])}M\t\
*\t\
0\t\
0\t\
{read['sequence']}\t\
{len(read['sequence'])*'~'}")



