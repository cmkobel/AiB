import pandas #pretty print result 2d-array # too slow?
from Bio import SeqIO
#import json

# Author: Carl M. Kobel 2018


#   ~ todo ~
# * cli?
# * optimization? (at least the stack is too big in multiple backtracking)

# 1. Mandatory
class Global_Alignment:
    def __init__(self, phylip_file, fasta_file, gapcost_type, backtrack_type, a, b = 0): # b is zero for linear gapcost
        def phylip_like_parser(input_file):
            with open(input_file, 'r') as file:
                raw = [line.strip().split() for line in file]
                rv = {'alphabet_len': raw[0], # alphabet isn't used for anything, is it?
                      'alphabet': [i[0] for i in raw[1:]],
                      'score_matrix': [[int(elem) for elem in list[1:]] for list in raw[1:]]}
            return rv['alphabet'], rv['score_matrix']

        def get_sequences(input_file):
            fasta_seqs = SeqIO.parse(input_file,'fasta')
            try:
                seqa, seqb = (str(i.seq) for i in fasta_seqs)
            except ValueError:
                print(f'Fasta-file {input_file} must contain exactly two sequences.')
            return(seqa, seqb)

        self.b = b # intercept
        self.a = a # slope
        self.alphabet, self.score_matrix = phylip_like_parser(phylip_file) # Make the output from phylip-like-parser() global.
        self.A, self.B = (self.encode(i) for i in get_sequences(fasta_file)) # Make the two sequences global.
        self.result = [[None for i in range(len(self.B) + 1)]\
                       for i in range(len(self.A) + 1)]
        self.vector = [[None for i in range(len(self.B) + 1)]\
                       for i in range(len(self.A) + 1)]

        self.compute(gapcost_type)



    # Helper methods
#    def oencode(self, input):
#        mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
#        return [mapping[i] for i in str(input).upper()]
#    def odecode(self, input):
#        demapping = {'0': 'A', '1': 'C', '2': 'G', '3': 'T', '-': '-'}
#        return ''.join([demapping[str(i)] for i in input])

    def encode(self, input):
        mapping = {key: num for num, key in enumerate(self.alphabet)}
        return [mapping[i] for i in str(input).upper()]
    def decode(self, input, join = False):
        demapping = {num: key for num, key in enumerate(self.alphabet)}
        if join:
            return ''.join([demapping[i] for i in input])
        else:
            return [demapping[i] for i in input]


    # Core methods
    def dyn_linear(self, i, j):
        #print(f'{i},{j}  ', end = '') # debug

        # Has it already been calculated?
        if self.result[i][j] != None:
            return self.result[i][j]

        # if not, calculate it..
        else:
            candidates = []
            if (i > 0) and (j > 0): # Diagonally
                candidates.append(self.dyn_linear(i-1, j-1) + self.score_matrix[self.A[i-1]][self.B[j-1]]) #?)
            if (i > 0) and (j >= 0): # Left
                candidates.append(self.dyn_linear(i-1, j) + self.a)
            if (i >= 0) and (j > 0): # Up
                candidates.append(self.dyn_linear(i, j-1) + self.a)
            if (i == 0) and (j == 0): # Base case
                candidates.append(0) # ?

            self.result[i][j] = min(candidates)
            return self.result[i][j]


    def dyn_affine(self, i, j): # g(x) = ax + b
        # Glem definitionen og skriv noget der virker!

    	# Has it already been calculated?
        if self.result[i][j] != None and self.vector[i][j] != None:
            return self.result[i][j], self.vector[i][j]
        
        # if not, calculate it.
        else:
            candidates = []
            if (i > 0) and (j > 0): # 0: Diagonally
                candidates.append((self.dyn_affine(i-1, j-1)[0] + self.score_matrix[self.A[i-1]][self.B[j-1]], 0)) # ingen gapcost her
            if (i > 0) and (j >= 0): #1:  up
                if self.vector[i-1][j] == 1:
                    candidates.append((self.dyn_affine(i-1, j)[0] + self.a, 1)) # continue gap
                else:
                    candidates.append( (self.dyn_affine(i-1, j)[0] + self.a + self.b, 1)) # start new gap

            if (i >= 0) and (j > 0): #2: left
                if self.vector[i][j-1] == 2:
                    candidates.append((self.dyn_affine(i, j-1)[0] + self.a, 2))
                else:
                    candidates.append((self.dyn_affine(i, j-1)[0] + self.a + self.b, 2))
            if (i == 0) and (j == 0): # Base case
                candidates.append((0, 3)) # ?

            self.result[i][j], self.vector[i][j] = min(candidates)

            return self.result[i][j], self.vector[i][j]



    def compute(self, method = 'linear'):
        if method == 'linear':
            score = self.dyn_linear(len(self.A), len(self.B))
        elif method == 'affine':
            score = self.dyn_affine(len(self.A), len(self.B))[0]
        # Pretty print everything
        print(f'''\n
input ({len(self.A)}x{len(self.B)})
A ({self.decode(self.A, join = True)}) vertically
B ({self.decode(self.B, join = True)}) horizontally


result
{pandas.DataFrame(self.result)}
best alignment = {score}

vector
{pandas.DataFrame(self.vector)}''')



    def backtrack_linear(self, method = 'single'):

        def single(i, j):
            """ Recursive backtrack. """

            #print(i, j, sep = ',', end = ' ')

            if i > 0 and j > 0 and self.result[i][j] == (self.result[i-1][j-1] + self.score_matrix[self.A[i-1]][self.B[j-1]]):
                string_a, string_b = single(i - 1, j - 1)
                return string_a + str(self.A[i-1]), string_b + str(self.B[j-1])
            elif i > 0 and j >= 0 and self.result[i][j] == (self.result[i - 1][j] + self.a):
                string_a, string_b = single(i - 1, j)
                return string_a + str(self.A[i - 1]), string_b + '-'
            elif i >= 0 and j > 0 and self.result[i][j] == (self.result[i][j-1] + self.a):
                string_a, string_b = single(i, j - 1)
                return string_a + '-', string_b + str(self.B[j-1])
            elif i == 0 and j == 0:
                return '', ''


        pri_list = [] # faster than returning?
        def multiple(i, j, string_A, string_B):
            """ Recursive backtrack. 
                multiple, heavy stack"""

            #print(i, j, sep = ',', end = ' ')

            if i > 0 and j > 0 and self.result[i][j] == (self.result[i-1][j-1] + self.score_matrix[self.A[i-1]][self.B[j-1]]):
                multiple(i - 1, j - 1, string_A + str(self.A[i-1]), string_B + str(self.B[j-1]))
            if i > 0 and j >= 0 and self.result[i][j] == (self.result[i - 1][j] + self.a):
                multiple(i - 1, j, string_A + str(self.A[i - 1]), string_B + '-')
            if i >= 0 and j > 0 and self.result[i][j] == (self.result[i][j-1] + self.a):
                multiple(i, j - 1, string_A + '-', string_B + str(self.B[j-1]))
            if i == 0 and j == 0:
                pri_list.append((self.decode(string_A[::-1], join = True), self.decode(string_B[::-1], join = True)))


        if method == 'single':
            print('\n\nSingle solution:')
            backtracked_A, backtracked_B = single(len(self.A), len(self.B))
            print(f'{self.decode(backtracked_B)}\n{self.decode(backtracked_A)}')

        if method == 'multiple':
            print('\n\nMultiple solutions:')
            multiple(len(self.A), len(self.B), '','') 
            #print(pri_list) # not exactly a nice way to print it..
            for i, (j, k) in enumerate(pri_list):
                print(f'{i}: (A)\t{j}\n{i}: (B)\t{k}\n')


    def backtrack_affine(self):
        pass


o = Global_Alignment('score_matrix.phylip-like',
                     'case2.fasta',
                     gapcost_type = 'affine', # linear | affine
                     backtrack_type = 'single', # none (default) | single | multiple
                     a = 5,
                     b = 5) # default: 0

# o.compute('affine') # linear | affine
# o.backtrack('single') # single | multiple