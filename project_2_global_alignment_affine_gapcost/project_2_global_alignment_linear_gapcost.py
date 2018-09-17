import pandas #pretty print result 2d-array # performance issues!
from Bio import SeqIO

# Author: Carl M. Kobel 2018

#   ~ todo ~
# * cli?
# * optimization? (at least the stack is too big in multiple backtracking)
# * make the finals upper. Do this when everything is working, so as not to change more things at one time.
# * lad være med at printe andre steder i __init__()
# make an encode function that takes a list.

# 1. Mandatory
class Global_Linear:
    def __init__(self, phylip_file, fasta_file, backtrack_type, slope = 0): # b is zero for linear gapcost
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


        
        # set global variables # ought to make these upper-case.
        self.a = slope # intercept 
        self.alphabet, self.score_matrix = phylip_like_parser(phylip_file) # Make the output from phylip-like-parser() global.
        self.A, self.B = (self.encode(i) for i in get_sequences(fasta_file)) # Make the two sequences global.
        self.result = [[None for i in range(len(self.B) + 1)]\
                       for i in range(len(self.A) + 1)]


        # run selected scoring algorithms
        print(f'''
type of
    gapcost:    {self.a}
    backtrack:  {backtrack_type}

input ({len(self.A)}x{len(self.B)})
A ({self.decode([i for i in map(str, self.A)], join = True)}) vertically
B ({self.decode([i for i in map(str, self.B)], join = True)}) horizontally

''')


        
        print('linear score:', self.dyn_linear())
        print(pandas.DataFrame(self.result))

        if backtrack_type == 'single':
            print('\nsingle solution:')
            output = self.backtrack_linear(backtrack_type)
        elif backtrack_type == 'multiple':
            print('\n\nmultiple solutions:')
            output = self.backtrack_linear(backtrack_type)

        for i, (j, k) in enumerate(output):
            print(f'{i}: (A)\t{j}\n{i}: (B)\t{k}\n')



    def encode(self, input):
        mapping = {letter: index for index, letter in enumerate(self.alphabet)}
        return [mapping[i] for i in str(input).upper()]
    def decode(self, input, join = False):
        demapping = {str(index): letter for index, letter in enumerate(self.alphabet)}
        demapping['-'] = '-'
        if join:
            return ''.join([demapping[i] for i in input])
        else:
            return [demapping[i] for i in input]


    def dyn_linear(self):

        def recursive(i, j):
        #print(f'{i},{j}  ', end = '') # debug

            # Has it already been calculated?
            if self.result[i][j] != None:
                return self.result[i][j]

            # if not, calculate it..
            else:
                candidates = []
                if (i > 0) and (j > 0): # Diagonally
                    candidates.append(recursive(i-1, j-1) + self.score_matrix[self.A[i-1]][self.B[j-1]]) #?)
                if (i > 0) and (j >= 0): # Left
                    candidates.append(recursive(i-1, j) + self.a)
                if (i >= 0) and (j > 0): # Up
                    candidates.append(recursive(i, j-1) + self.a)
                if (i == 0) and (j == 0): # Base case
                    candidates.append(0) # ?

                self.result[i][j] = min(candidates)
                return self.result[i][j]

        return recursive(len(self.A), len(self.B))



    def backtrack_linear(self, backtrack_type = 'single'):

        pri_list = [] # collects strings

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


        if backtrack_type == 'single':
            pri_list = [[self.decode(i) for i in j] for j in [single(len(self.A), len(self.B))]]
        elif backtrack_type == 'multiple':
            multiple(len(self.A), len(self.B), '', '')

        return pri_list





o = Global_Linear('score_matrix.phylip-like',
                     'case4.fasta',
                     backtrack_type = 'multiple', # none (default) | single | multiple
                     slope = 5) # default: 0


