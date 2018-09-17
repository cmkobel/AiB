import pandas #pretty print result 2d-array # performance issues!
from Bio import SeqIO

# Author: Carl M. Kobel 2018

#   ~ todo ~
# * cli?
# * optimization? (at least the stack is too big in multiple backtracking)
# make an encode function that takes a list

# 1. Mandatory
class Global_Affine:
    def __init__(self, phylip_file, fasta_file, backtrack_type, a, b = 0): # b is zero for linear gapcost
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
        self.SLOPE = a
        self.INTERCEPT = b
        self.ALPHABET, self.SCORE_MATRIX = phylip_like_parser(phylip_file) # Make the output from phylip-like-parser() global.
        self.A, self.B = (self.encode(i) for i in get_sequences(fasta_file)) # Make the two sequences global.
        
        self.result = [[None for i in range(len(self.B) + 1)]\
                       for i in range(len(self.A) + 1)]
        self.vector = [[None for i in range(len(self.B) + 1)]\
                       for i in range(len(self.A) + 1)]


        # run selected settings algorithms
        print(f'''type of
    gapcost:    g(x) = {a}x + {b}
    backtrack:  {backtrack_type}

input ({len(self.A)}x{len(self.B)})
A ({self.decode([i for i in map(str, self.A)], join = True)}) vertically
B ({self.decode([i for i in map(str, self.B)], join = True)}) horizontally

''')



        print('affine score:', self.dyn_affine())
        print(pandas.DataFrame(self.result))

        print(f'\nvector\n{pandas.DataFrame(self.vector)}')

        self.backtrack_affine(backtrack_type)



    def encode(self, input):
        mapping = {letter: index for index, letter in enumerate(self.ALPHABET)}
        return [mapping[i] for i in str(input).upper()]
    def decode(self, input, join = False):
        demapping = {str(index): letter for index, letter in enumerate(self.ALPHABET)}
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
                    candidates.append(recursive(i-1, j-1) + self.SCORE_MATRIX[self.A[i-1]][self.B[j-1]]) #?)
                if (i > 0) and (j >= 0): # Left
                    candidates.append(recursive(i-1, j) + self.SLOPE)
                if (i >= 0) and (j > 0): # Up
                    candidates.append(recursive(i, j-1) + self.SLOPE)
                if (i == 0) and (j == 0): # Base case
                    candidates.append(0) # ?

                self.result[i][j] = min(candidates)
                return self.result[i][j]

        return recursive(len(self.A), len(self.B))


    def dyn_affine(self): # g(x) = ax + b

        def recursive(i, j):
            # Glem definitionen og skriv noget der virker!

        	# Has it already been calculated?
            if self.result[i][j] != None and self.vector[i][j] != None:
                return self.result[i][j], self.vector[i][j]
            
            # if not, calculate it.
            else:
                candidates = []
                if (i > 0) and (j > 0): # 0: Diagonally
                    candidates.append((recursive(i-1, j-1)[0] + self.SCORE_MATRIX[self.A[i-1]][self.B[j-1]], 0)) # ingen gapcost her
                if (i > 0) and (j >= 0): #1:  up
                    if self.vector[i-1][j] == 1:
                        candidates.append((recursive(i-1, j)[0] + self.SLOPE, 1)) # continue gap
                    else:
                        candidates.append( (recursive(i-1, j)[0] + self.SLOPE + self.INTERCEPT, 1)) # start new gap

                if (i >= 0) and (j > 0): #2: left
                    if self.vector[i][j-1] == 2:
                        candidates.append((recursive(i, j-1)[0] + self.SLOPE, 2))
                    else:
                        candidates.append((recursive(i, j-1)[0] + self.SLOPE + self.INTERCEPT, 2))
                if (i == 0) and (j == 0): # Base case
                    candidates.append((0, 3)) # ?

                self.result[i][j], self.vector[i][j] = min(candidates)

                return self.result[i][j], self.vector[i][j]
        
        return recursive(len(self.A), len(self.B))[0] # [0] ?



    def backtrack_affine(self, backtrack_type = 'single'):
        print('backtracking:')
        
        def single(i ,j):
            """ code copied from linear """
            if i > 0 and j > 0 and self.result[i][j] == (self.result[i-1][j-1] + self.SCORE_MATRIX[self.A[i-1]][self.B[j-1]]):
                string_a, string_b = single(i - 1, j - 1)
                return string_a + str(self.A[i-1]), string_b + str(self.B[j-1])
            elif i > 0 and j >= 0 and self.result[i][j] == (self.result[i - 1][j] + self.SLOPE):
                string_a, string_b = single(i - 1, j)
                return string_a + str(self.A[i - 1]), string_b + '-'
            elif i >= 0 and j > 0 and self.result[i][j] == (self.result[i][j-1] + self.SLOPE):
                string_a, string_b = single(i, j - 1)
                return string_a + '-', string_b + str(self.B[j-1])
            elif i == 0 and j == 0:
                return '', ''


        return single(len(self.A), len(self.B))

            


o = Global_Affine('score_matrix.phylip-like',
                  'case2.fasta',
                  backtrack_type = 'single', # none (default) | single | multiple
                  a = 5,
                  b = 5) # default: 0


