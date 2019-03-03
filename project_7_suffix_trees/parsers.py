# Author: Carl M. Kobel 2019
import json


def parse_fasta(input_file):
    """ # Does support multiline fasta files. """
    with open(input_file) as file:
        raw = [i.strip() for i in file]

    header_lines = [_i for _i, i in enumerate(raw) if i[0:1] == ">"] # alle linjenumre hvor der er en header.
    end_lines = [i-1 for i in header_lines[1:]] + [len(raw)] # linjetal minus en, fra anden header til slut, plus sidste linje.



    for start, end in zip(header_lines, end_lines):
        #print(start, end)
        rv = {}
        rv['title'] = raw[start][1:].strip()
        rv['sequence'] = ''.join(raw[start+1:end+1])
        yield rv


if __name__ == "__main__":


    for genome in parse_fasta('data/seqs_mut.fasta'):
        #print('genome:', genome['sequence'])
        print(json.dumps(genome))

    if not False:
        for reference in parse_fasta('data/ref.fa'):
            print(reference['title'])
            print('\t', reference['sequence'])
            print()


def parse_fastq(input_file):
    """
    Generator.
    Returns a dictionary with keys: [title, sequence, description, quality].
    A new dictionary will be returned for each entry in a fastq-file.
    
    ~ TODO ~
    * support multiline. ?
    """

    with open(input_file) as file:
        for line in file:
            if line[0:1] == '@':
                title = line[1:].strip()
                
                sequence = file.__next__().strip()
                
                description = file.__next__().strip()
                if description[0:1] != '+':
                    raise ValueError('description-row did not start with a + symbol. Every forth row from the 3rd must start with a + symbol.')

                quality = file.__next__().strip()
                if len(quality) != len(sequence):
                    raise ValueError(f'{title}: length of sequence ({len(sequence)}) is not equal to length of quality ({len(quality)}).')

                rv = {}
                
                rv['title'] = title
                rv['sequence'] = sequence
                rv['description'] = description
                rv['quality'] = quality

                yield rv



if __name__ == "__main__":
    for i in parse_fastq('data/exact_samples.fq'):
        print('>>>>', i['sequence'])
