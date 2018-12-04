def parse(input_file):
    """ Parses a phylip like file into a dict with all the contents present. """
    with open(input_file, 'r') as file:
        raw = [line.strip().split() for line in file] # Read in the complete file.
        rv = {'N': raw[0][0],
              'taxa': [i[0] for i in raw[1:]], # Each first element in each list (read leftmost column).
              'dissimilarity_matrix': [[float(elem) for elem in list[1:]] for list in raw[1:]]}

        # Sanity checks.
        if len(rv['taxa']) != int(rv['N']):
            raise ValueError(f"The height of the dissimilarity matrix ({len(rv['taxa'])}) doesn\'t match the number specified in the file ({int(rv['N'])}).")

        if len(rv['dissimilarity_matrix'][0]) != int(rv['N']):
            raise ValueError(f"The width of the dissimilarity matrix ({len(rv['dissimilarity_matrix'][0])}) doesn\'t match the number specified in the file ({int(rv['N'])}).")




    return rv


if __name__ == '__main__':
    # Short test.

    print(parse('data/custom_distance_matrices/14_Adeno_E3_CR1.phy'))
#   print(parse('data/custom_distance_matrices/29_Adeno_E3_CR1.phy'))
