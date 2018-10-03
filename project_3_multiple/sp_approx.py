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
        #self.SEQUENCES = sequences
        self.ALPHABET = ['A', 'C', 'G', 'T']
        self.GAP = 5

        #           A  C  G  T 
        self.SM = [[0, 5, 2, 5], # Substitution Matrix
                   [5, 0, 5, 2],
                   [2, 5, 0, 5],
                   [5, 2, 5, 0]]


        
        


        def encode(input):
            """ Take a string 'ACGT', returns a list of numbers [0, 1, 2, 3]"""
            mapping = {letter: index for index, letter in enumerate(self.ALPHABET)}
            return [mapping[i] for i in str(input).upper()]
        
        self.SEQUENCES = [encode(i) for i in sequences]

    def decode(self, input, join = False):
        """ Takes a string '0123-', returns a list of letters ['A', 'C'..] or 'AC' if join is true
        todo: make a decode function that iterates through a list as well, so you have decode_string() this and decode_list() new."""
        demapping = {str(index): letter for index, letter in enumerate(self.ALPHABET)}
        demapping['-'] = '-' # add the gap 'letter'
        if join:
            return ''.join([demapping[i] for i in input])
        else:
            return [demapping[i] for i in input]


    def pair_score(self, seq_A, seq_B):
        """ Takes two sequences A and B, and returns the score of optimal alignment """
        gap, sm = self.GAP, self.SM
        result = [[None for i in range(len(seq_B) + 1)] for i in range(len(seq_A) + 1)]
        
        def score(i, j):
            if result[i][j] != None:
                return result[i][j]
            else:
                candidates = []
                if (i > 0) and (j > 0): candidates.append(score(i-1, j-1) + sm[seq_A[i-1]][seq_B[j-1]])
                if (i > 0) and (j >= 0): candidates.append(score(i-1, j) + gap)
                if (i >= 0) and (j > 0): candidates.append(score(i, j-1) + gap)
                if (i == 0) and (j == 0): candidates.append(0)
                result[i][j] = min(candidates)
                return result[i][j]
        return(score(len(seq_A), len(seq_B)))

        

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


seq_set_from_book_8_2_2 = ['AGTAATGG',
                           'TTTAATGA',
                           'AAGAAATGG',
                           'ATAAAATGG']

seq_set_case1_fasta = ['acgtgtcaacgt',
                       'acgtcgtagcta'] # 22

seq_set_case2_fasta = ['aataat', 
                       'aagg'] # 14

seq_set_case3_fasta = ['tccagaga',
                       'tcgat'] # 20

seq_set_case4_fasta = ['ggcctaaaggcgccggtctttcgtaccccaaaatctcggcattttaagataagtgagtgttgcgttacactagcgatcta\
ccgcgtcttatacttaagcgtatgcccagatctgactaatcgtgcccccggattagacgggcttgatgggaaagaacagc\
tcgtctgtttacgtataaacagaatcgcctgggttcgc',
                       'gggctaaaggttagggtctttcacactaaagagtggtgcgtatcgtggctaatgtaccgcttctggtatcgtggcttacg\
gccagacctacaagtactagacctgagaactaatcttgtcgagccttccattgagggtaatgggagagaacatcgagtca\
gaagttattcttgtttacgtagaatcgcctgggtccgc'] # 325




o = SP_approx(seq_set_case4_fasta)

# debug
#for n, i in enumerate(o.SEQUENCES):
#    print(f'seq_{n}: {i}')
print(o.pair_score(o.SEQUENCES[0], o.SEQUENCES[1]))

