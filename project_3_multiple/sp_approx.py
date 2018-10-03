# Author: Carl M. Kobel 2018

# Implements the 2-approximation algorithm for any number of sequences (described in Section 8.2.2 in BA, or in Section 14.6.2 in Gusfield's book).

"""
Procedure
    · Compute pairwise edit distances to find ind the center string
        · Det er vel bare alle mulige kombinationer af strenge, og så tage den bedste.
        · Genbrug kode fra tidligere.
    · Align alle par: S1 - Si over alle i+1 ... n




"""


class SP_approx:
    def __init__(self, sequences):
        self.SEQUENCES = sequences
        self.ALPHABET = ['A', 'C', 'G', 'T']
        self.GAP = 5

        #           A  C  G  T 
        self.SM = [[0, 5, 2, 5], # Substitution Matrix
                   [5, 0, 5, 2],
                   [2, 5, 0, 5],
                   [5, 2, 5, 0]]

    def encode(self, input):
        """ Take a string 'ACGT', returns a list of numbers [0, 1, 2, 3]"""
        mapping = {letter: index for index, letter in enumerate(self.ALPHABET)}
        return [mapping[i] for i in str(input).upper()]
    def decode(self, input, join = False):
        """ Takes a string '0123-', returns a list of letters ['A', 'C'..] or 'AC' if join is true"""
        demapping = {str(index): letter for index, letter in enumerate(self.ALPHABET)}
        demapping['-'] = '-' # add the gap 'letter'
        if join:
            return ''.join([demapping[i] for i in input])
        else:
            return [demapping[i] for i in input]

        

    def calculate_all_pairwise_distances(self):
        """ To find center string
        Takes O(n^2) for the k(k-1) pairs of strings

        """
        # Til det skal jeg nok bruge noget kode der giver cost af to strenge. Kig i uge 1 eller 2
                pass


    def align_pairs_S1_Si(self):
        pass

    def calculate_sum_of_pairs_score_of_alignments(self):
        pass


sequence_set_1 = ('AGTAATGG',
                  'TTTAATGA',
                  'AAGAAATGG',
                  'ATAAAATGG')

o = SP_approx(sequence_set_1)