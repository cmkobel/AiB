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
        """ Takes a string '0123-' or ['0','1','2','3', '-'] returns a list of letters ['A', 'C'..] or 'AC' if join is true """
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
        

    def align(self, seq_A, seq_B, substitution_matrix = None, gap = None):
        """ Takes two sequences A and B, and returns the levenshtein distance. 
        Actually, it is not defined exactly as the levenshtein distance, because it has a gap parameter, but it 
        calculates something that is equivalent to it for the used range of inputs."""
        
        #gap, sm = self.GAP, self.SM
        if substitution_matrix == None:
            substitution_matrix = self.SM
        if gap == None:
            gap = self.GAP
        

        result = [[None for i in range(len(seq_B)+1)] for i in range(len(seq_A)+1)]
        def score(i, j):
            if result[i][j] != None:
                return result[i][j]
            else:
                candidates = []
                if (i > 0) and (j > 0): candidates.append(score(i-1, j-1) + substitution_matrix[seq_A[i-1]][seq_B[j-1]])
                if (i > 0) and (j >= 0): candidates.append(score(i-1, j) + gap)
                if (i >= 0) and (j > 0): candidates.append(score(i, j-1) + gap)
                if (i == 0) and (j == 0): candidates.append(0)
                result[i][j] = min(candidates)
                return result[i][j]

        score(len(seq_A), len(seq_B))
        #print('o', result) # debug
        return result


    def levenshtein_distance(self, seq_A, seq_B):
        substitution_matrix = [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
        gap = 1
        return self.align(seq_A, seq_B, substitution_matrix, gap)[len(seq_A)][len(seq_B)]


    def backtrack(self, seq_A, seq_B, T):
        """ Returns a list with the alignment of two strings seq_A and seq_B """
        def recursive(i, j):
            #print(i, j, sep = ',', end = ' ')
            if i > 0 and j > 0 and T[i][j] == (T[i-1][j-1] + self.SM[seq_A[i-1]][seq_B[j-1]]):
                string_a, string_b = recursive(i - 1, j - 1)
                return string_a + str(seq_A[i-1]), string_b + str(seq_B[j-1])
            elif i > 0 and j >= 0 and T[i][j] == (T[i - 1][j] + self.GAP):
                string_a, string_b = recursive(i - 1, j)
                return string_a + str(seq_A[i - 1]), string_b + '-'
            elif i >= 0 and j > 0 and T[i][j] == (T[i][j-1] + self.GAP):
                string_a, string_b = recursive(i, j - 1)
                return string_a + '-', string_b + str(seq_B[j-1])
            elif i == 0 and j == 0:
                return '', ''
        return list(recursive(len(seq_A), len(seq_B)))


    def center_string_index(self):
        def distance_matrix():
            """ Retuns the index of the center string Sc
            Takes O(n^2) for the k(k-1) pairs of strings
            Makes something that looks like the table in the bottom of page 411
            """
            m = len(self.SEQUENCES)
            rv = [[0 for i in range(m)] for i in range(m)]
            for i in range(0, m):
                for j in range(1, m):
                    if i < j:
                        score = self.levenshtein_distance(self.SEQUENCES[i], self.SEQUENCES[j])
                        #print(i,j, score) 
                        rv[i][j], rv[j][i] = score, score # fill the table symmetrically, makes it easier to later calculate the sums.
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
        """ Counts the maximum number of consecutive gaps in pairs of alignments """
        return 1
        #return 5


    def build_alignment(self, center_string_index):
        """ Represents pairwise alignment of all pairs of strings Sc Si for all n>1.
        """

        m = len(self.SEQUENCES)
        aligned_pairs = []
        for i in range(m):
            if i != center_string_index:
                aligned_pairs.append( o.backtrack(self.SEQUENCES[center_string_index], self.SEQUENCES[i], self.align(self.SEQUENCES[center_string_index], self.SEQUENCES[i])) )


        center_string = [i for i in map(str, self.SEQUENCES[center_string_index])]
        center_string = self.decode(center_string)
        #print('center-string',center_string) # debug ba
        
        aligned_pairs = [[self.decode(i) for i in j] for j in aligned_pairs]
        #print('al', aligned_pairs) # debug ba




        def count_gaps_in_center_string(center_string, aligned_pairs):
            gap_at_idx = [[0 for i in range(len(aligned_pairs))] for i in range(len(center_string)+1)] # note: transposed!! ..bad idea I guess.
            for pair_idx, pair in enumerate(aligned_pairs):
                cum_sum = 0
                for i_idx, i_value in enumerate(pair[0]):
                    if i_value == '-':
                        gap_at_idx[i_idx - cum_sum][pair_idx] += 1
                        cum_sum += 1

            ##print('gap_at_idx:', gap_at_idx) # debug # debug ba

            rv = [0 for i in range(len(center_string)+1)]
            for i_idx, i in enumerate(gap_at_idx):
                rv[i_idx] = max(i)

            return rv


        dash_list = count_gaps_in_center_string(center_string, aligned_pairs)
        #print('dash_list:', dash_list) # debug ba

        def expand_center_string_with_gaps(center_string, dash_list):
            rv = '-' * dash_list[0]
            for idx, letter in enumerate(center_string):
                rv += letter
                rv += '-' * dash_list[idx+1]
            return [i for i in rv]

        center_string = expand_center_string_with_gaps(center_string, dash_list)
        #print('cs', center_string) # debug ba

        """
        Så, nu er center strengen udvidet med gaps så meget som den behøver.
        Nu kan vi gå i gang med at lave vores multiple alignment.
        """



        def align_multiple(center_string, aligned_pairs):
            msa = [center_string] + [[None for i in range(len(center_string))] for i in range(len(aligned_pairs))] # alloker fuld størrelse af msa
            #print('msa', msa) # debug ba
            for i, i_val in enumerate(aligned_pairs): # for hvert par ..
                lag = 0
                for j, j_val in enumerate(center_string): # .. gå igennem hver position i den paddede centerstreng
                    ##print(j, i_val[0][j-lag], j_val, end = ' ' * 4) # debug ba
                    #print(i, j) # debug ba
                    if i_val[0][j-lag] != j_val:
                        msa[i+1][j] = '-'
                        lag += 1
                    else:
                        msa[i+1][j] = i_val[1][j-lag]
                        if j-lag+1 == len(i_val[1]): # hvis vi har skrevet det sidste element, så sørg for at vi ikke går over range i S^i
                            lag += 1 
            return msa

        # ## debug printing: # debug ba
        msa = align_multiple(center_string, aligned_pairs)
        # #print('\n\nfinal msa:') # debug ba
        # for i, i_val in enumerate(msa):
        #     #print(i, end = ') ') # debug ba
        #     for j in i_val:
        #         #print(f'{j}  ', end = '') # debug ba
        #     #print() # debug ba
       


        #print('\ncomb') # debug ba
        sum_list = [0 for i in range(len(center_string))] # just to validate the values one column at a time. In the end, a sum value can just be sum += value
        grand_total = 0
        cols = len(center_string)
        rows = len(msa)
        for i in range(cols): # kolonner i msa
            for j in range(rows):
                for k in range(rows):
                    if j < k:
                        first = msa[j][i]
                        second = msa[k][i]
                        #print(i,' ', j, k, first, second) # debug ba
                        sum = 0
                        if first == '-' and second == '-':
                            continue
                        elif first == '-' or second == '-':
                            sum += self.GAP
                        else:
                            sum += self.SM[self.ALPHABET.index(first)][self.ALPHABET.index(second)]
                        sum_list[i] += sum
                        grand_total += sum
            
            #print() # debug ba

        #print(sum_list) # debug ba
        #print(grand_total) # debug ba

        return msa, grand_total












    def calculate_sum_of_pairs_score_of_alignments(self):
        """ final distance calculation
        I'm not sure how to do it. """
        pass


seq_set_sole = [
    'AGTAATGG',
    'TTTAATGA',
    'AAGAAATGG',
    'ATAAAATGG',
]

seq_set_sole_short = [
    'ACT',
    'ATT',
    'AAGG',
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


# # test align
# seqs = o.SEQUENCES[0], o.SEQUENCES[1]
# alignment_table = o.align(seqs[0], seqs[1])
# print(alignment_table)
# print('---')
# print(o.backtrack(seqs[0], seqs[1], alignment_table))


# test center index identification
csi = o.center_string_index()
#print('csi', csi)

# test building alignment
print(o.build_alignment(csi))