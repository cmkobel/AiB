# Author: Carl M. Kobel 2018

# Implements the 2-approximation algorithm for any number of sequences
#(described in Section 8.2.2 in BA, or in Section 14.6.2 in Gusfield's book).

"""
Procedure
    · Compute pairwise edit distances to find ind the center string
        · Det er vel bare alle mulige kombinationer af strenge, og så tage den bedste.
        · Genbrug kode fra tidligere.
    · Align alle par: S1 - Si over alle i+1 ... n

"""


class SP_approx:
    def encode(self, input):
        """ Take a string 'ACGT', returns a list of numbers [0, 1, 2, 3]"""
        mapping = {letter: index for index, letter in enumerate(self.ALPHABET)}
        return [mapping[i] for i in str(input).upper()]
   
    def decode(self, input, join = False):
        """ Takes a string '0123-' or ['0','1','2','3', '-'] returns a list of letters ['A', 'C'..] or 'AC' if join is true
        """
        demapping = {str(index): letter for index, letter in enumerate(self.ALPHABET)}
        demapping['-'] = '-' # add the gap 'letter'
        if join:
            return ''.join([demapping[i] for i in input])
        else:
            return [demapping[i] for i in input]
    

    def __init__(self, sequences):
        self.ALPHABET = ['A', 'C', 'G', 'T']
        self.SEQUENCES = [self.encode(i) for i in sequences]
        self.GAP = 5
        
        #           A  C  G  T 
        self.SM = [[0, 5, 2, 5], # A
                   [5, 0, 5, 2], # C
                   [2, 5, 0, 5], # G
                   [5, 2, 5, 0]] # T

        

    def levenshtein_dist(self, seq_A, seq_B):
        """ Takes two sequences A and B, and returns the levenshtein distance. 
        Actually, it is not defined exactly as the levenshtein distance, because it has a gap parameter, but it 
        calculates something that is equivalent to it for the used range of inputs."""
        
        #gap, sm = self.GAP, self.SM
        gap = 1
        sm = [[0, 1, 1, 1], # Substitution Matrix
              [1, 0, 1, 1],
              [1, 1, 0, 1],
              [1, 1, 1, 0]]

        result = [[None for i in range(len(seq_B)+1)] for i in range(len(seq_A)+1)]
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

        rv = score(len(seq_A), len(seq_B))
        #print('o', result) # debug
        return rv

    def align(self):
        """ remember that levenshtein is a special case of align with a special SM """


    def backtrack(self):
        """ self plagiarize """
        pass

        
    def center_string_index(self):
        def distance_matrix():
            """ To find center string
            Takes O(n^2) for the k(k-1) pairs of strings
            Makes something that looks like the table in the bottom of page 411
            """
            m = len(self.SEQUENCES)
            rv = [[0 for i in range(m)] for i in range(m)]
            for i in range(0, m):
                for j in range(1, m):
                    if i < j:
                        score = self.levenshtein_dist(self.SEQUENCES[i], self.SEQUENCES[j])
                        #print(i,j, score) 
                        rv[i][j] = score
                        rv[j][i] = score # fill the table symmetrically, makes it easier to later calculate the sums.
            #print('dist matrix', rv) # debug
            return rv

        # Calculate the score sums of distances to other strings, for each string.
        sums = [sum(i) for i in distance_matrix()]
        #print('sums', sums) # debug

        # Find the index of the minimum sum. That is the index of the center string.
        min_idx = sums.index(min(sums))
        #print('idx', min_idx) # debug

        return min_idx

    def max_num_gaps(self, string):
        return 1
        #return 5

    def build_alignment(self):
        """ Represents pairwise alignment of all pairs of strings Sc Si for all n>1 """

        def pad(input, g):
            """ Inserts g gaps around all letters in the input """
            rv = g * '-'
            for i in input:
                rv += i + g * '-'
            input = rv
            return rv
            
        
        center_star = ['A', 'C', 'T']
        print(center_star)

        # Pad the center star with dashes
        center_star = pad(center_star, self.max_num_gaps('all_pairs_of_pairwise_alignments()'))
        

        pairwise_alignments = [[['A', 'C', '-', 'T'],
                       ['A', '-', 'T', 'T']],
                      [['A', 'C', '-', 'T'],
                       ['A', 'T', 'G', 'T']]]
        
        print(center_star)

        complete_alignment = list()
        for n_i, i in enumerate(pairwise_alignments):
            for n_j, j in enumerate(i[1]):
                print(n_i, n_j, j)
                complete_alignment[i][j]



        # s
        
        rv = [[]]






    def calculate_sum_of_pairs_score_of_alignments(self):
        """ final distance calculation
        how to do it ? """
        pass


seq_set_sole = [
    'AGTAATGG',
    'TTTAATGA',
    'AAGAAATGG',
    'ATAAAATGG',
]

#seq_set_simple = ['ACT']

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




o = SP_approx(seq_set_sole)

# test encoded strings
#for n, i in enumerate(o.SEQUENCES): 
#    print(f'seq_{n}: {i}')


# test levenshtein_dist
#print(o.levenshtein_dist(o.SEQUENCES[0], o.SEQUENCES[1]))

# test center index identification
#print('csi', o.center_string_index())

o.build_alignment()