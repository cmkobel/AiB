# Author: Carl M. Kobel 2019
# Does support multiline fasta files.



def parse_fasta(input_file):
    with open(input_file) as file:
        raw = [i.strip() for i in file]

    header_lines = [_i for _i, i in enumerate(raw) if i[0:1] == ">"] # alle linjenumre hvor der er en header.
    end_lines = [i-1 for i in header_lines[1:]] + [len(raw)] # linjetal minus en, fra anden header til slut, plus sidste linje.

    for start, end in zip(header_lines, end_lines):
        rv = {}
        rv['title'] = raw[start][1:].strip()
        rv['sequence'] = ''.join(raw[start+1:end])
        yield rv



if __name__ == "__main__":
    for reference in parse_fasta('data/ref.fa'):
        print(reference['title'])
        print('\t', reference['sequence'])
        print()
