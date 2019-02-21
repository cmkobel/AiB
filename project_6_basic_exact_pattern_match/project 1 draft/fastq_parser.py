# Author: Carl M. Kobel 2019

# ~ TODO ~
# * support multiline.


def parse_fastq(input_file):
    """
    Generator.
    Returns a dictionary with keys: [title, sequence, description, quality].
    A new dictionary will be returned for each entry in a fastq-file.
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
