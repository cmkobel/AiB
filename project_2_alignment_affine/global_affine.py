
from Bio import SeqIO

# Author: Carl Mathias Kobel 2018

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
                      'substitution_matrix': [[int(elem) for elem in list[1:]] for list in raw[1:]]}
            return rv['alphabet'], rv['substitution_matrix']
        def get_sequences(input_file):
            fasta_seqs = SeqIO.parse(input_file,'fasta')
            try:
                seqa, seqb = (str(i.seq) for i in fasta_seqs)
            except ValueError:
                print(f'Fasta-file {input_file} must contain exactly two sequences.')
            return(seqa, seqb)
        def pprint(input):
            for i in input:
                print(*i, sep = '\t')


        
        # set global variables # ought to make these upper-case.
        self.SLOPE = a
        self.INTERCEPT = b
        self.ALPHABET, self.SUBSTITUTION_MATRIX = phylip_like_parser(phylip_file) # Make the output from phylip-like-parser() global.
        self.A, self.B = (self.encode(i) for i in get_sequences(fasta_file)) # Make the two sequences global.
        
        self.result = [[None for i in range(len(self.B) + 1)]\
                       for i in range(len(self.A) + 1)]
        self.vector = [[None for i in range(len(self.B) + 1)]\
                       for i in range(len(self.A) + 1)]



        # run selected settings algorithms
        print(f'''substitution_matrix = 
{pprint(self.SUBSTITUTION_MATRIX)}

alphabet: {self.ALPHABET}

type of
    gapcost:    g(x) = {self.SLOPE}x + {self.INTERCEPT}
    backtrack:  {backtrack_type}

input ({len(self.A)}x{len(self.B)})
A ({self.decode([i for i in map(str, self.A)], join = True)}) vertically
B ({self.decode([i for i in map(str, self.B)], join = True)}) horizontally
''')



        print('affine score:', self.affine())
        print(f'result =\n{pprint(self.result)}')
        

        print(f'\nvector =\n{pprint(self.vector)}\n')

        if backtrack_type == 'single':
            print('an optimal alignment:')
            for i in self.backtrack_affine(backtrack_type):
                print(self.decode(i, join = True))



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





    def affine(self): # g(x) = ax + b
        print('i j')
        print('___')
        def rec(i, j):
            """ This function seems to work perfectly, but I'm not sure about using '3' as sign for moving diagonally. """
            
            # Glem definitionen og skriv noget der virker!

            # Has it already been calculated?
            if self.result[i][j] != None and self.vector[i][j] != None:
                return self.result[i][j], self.vector[i][j]
            
            
            # if not, calculate it.
            else:
                #print(i, j) # 0,0   1,0
                cand = [] # list of candidates
                if (i > 0) and (j >= 0): #1:  means we can subtract from i (move vertically) | overalt på nær top række
                    if rec(i-1, j)[1] == 1: # true if downwards gap was started in prior cell
                    #if self.vector[i-1][j] == 1:
                        cand.append((rec(i-1, j)[0] + self.SLOPE, 1)) # continue gap
                    else:
                        cand.append((rec(i-1, j)[0] + self.SLOPE + self.INTERCEPT, 1)) # start new gap

                if (i >= 0) and (j > 0): #2: means we can subtract from j (move horizontally) | overalt på nær venstre kolonne
                    if rec(i, j-1)[1] == 2:
                    #if self.vector[i][j-1] == 2:
                        cand.append((rec(i, j-1)[0] + self.SLOPE, 2))
                    else:
                        cand.append((rec(i, j-1)[0] + self.SLOPE + self.INTERCEPT, 2))
                
                if (i > 0) and (j > 0): # 0: move diagonally | overalt på nær top række og venstre kolonne
                    cand.append((rec(i-1, j-1)[0] + self.SUBSTITUTION_MATRIX[self.A[i-1]][self.B[j-1]], 3)) # ingen gapcost ved diagonal bevægelse
                
                
                if (i == 0) and (j == 0): # Base case
                    cand.append((0, 3)) # ?

                self.result[i][j], self.vector[i][j] = min(cand)
                #print(min(cand), cand)

                return self.result[i][j], self.vector[i][j]


        def new_iterative(len_A, len_B):
            """ This function works perfectly. I don't know if it has problems with overlapping gap openings, because I don't have data to test it. 
            3   diagonal
            2   vertical
            1   horizontal
            0   vertical and horizontal
            """

            for i in range(len_A+1):
                for j in range(len_B+1):
                    #print(i, j, 'new_iterative')
                    cand = []                    
                    
                    if i > 0 and j >= 0: # Horizontal
                        if self.vector[i-1][j] == 1:
                            cand.append((self.result[i-1][j] + self.SLOPE, 1)) #
                        else:
                            cand.append((self.result[i-1][j] + self.SLOPE + self.INTERCEPT, 1)) #
                    
                    if i >= 0 and j > 0: # Vertical
                        if self.vector[i][j-1] == 2:
                            cand.append((self.result[i][j-1] + self.SLOPE, 2)) # 
                        else:
                            #print(self.result)
                            cand.append((self.result[i][j-1] + self.SLOPE + self.INTERCEPT, 2)) # 

                    if i > 0 and j > 0: # Diagonal
                        cand.append((self.result[i-1][j-1] + self.SUBSTITUTION_MATRIX[self.A[i-1]][self.B[j-1]], 3))

                    if i == 0 and j == 0:
                        cand.append((0, 3)) # start of table, add 0, 3

                    # as a zero in the vector matrix means that both a 
                    cand.sort() # minimum is the first element now
                    if len(cand) > 1:
                        #if cand[0][1] < 3 and cand[1][1] < 3: # both vector 
                        if cand[0][0] == cand[1][0] and (cand[0][1] + cand[1][1] == 3): # both vertical and horizontal is possible
                            print(cand)
                            cand[0] = (cand[0][0], 0) # change one of them into a zero for the vector matrix
                            print(cand, 'e')
                    self.result[i][j], self.vector[i][j] = cand[0]



        #return rec(len(self.A), len(self.B))[0] # [0] ?

        return new_iterative(len(self.A), len(self.B))



    def backtrack_affine(self, backtrack_type = 'single'):
        """Needs to be adjusted the new vector symbols"""
        
        string_A = []
        string_B = []

        def single(i ,j):
            #3   diagonal
            #2   vertical
            #1   horizontal
            #0   vertical and horizontal


            if i == 0 and j == 0:
                return '', ''
            elif self.vector[i][j] == 3: # diagonal
                string_a, string_b = single(i - 1, j - 1)
                return string_a + str(self.A[i-1]), string_b + str(self.B[j-1])
            elif self.vector[i][j] == 2: # vertical
                string_a, string_b = single(i - 1, j)
                return string_a + str(self.A[i - 1]), string_b + '-'
            elif self.vector[i][j] <= 1: # horizontal
                string_a, string_b = single(i, j - 1)
                return string_a + '-', string_b + str(self.B[j-1])



        return single(len(self.A), len(self.B))


o = Global_Affine(phylip_file = 'substitution_matrix.phylip-like',
                  fasta_file = 'case2.fasta', # 24, 22, 29, 395
                  backtrack_type = 'none', # none (default) | single | multiple (not implemented yet)
                  a = 5,
                  b = 5) # default: 0
