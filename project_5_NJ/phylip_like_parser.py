def parse(input_file):
    """ Parses a phylip like file into a dict with all the contents present. """
    with open(input_file, 'r') as file:
        raw = [line.strip().split() for line in file]
        rv = {'N': raw[0],
              'taxa': [i[0] for i in raw[1:]],
              'dissimilarity_matrix': [[float(elem) for elem in list[1:]] for list in raw[1:]]}
    return rv