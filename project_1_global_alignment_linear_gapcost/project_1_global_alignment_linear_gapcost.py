import pandas #pretty print result 2d-array # too slow?
#import json
#import numpy as np # overkill

# Author: Carl M. Kobel 2018

#   ~ todo ~
# * cli?
# * optimization? (at least the stack is too big in multiple backtracking)


class Pairwise_alignment:
    '''with linear gap cost'''

    def __init__(self, B, A):
        
        # Constants
        self.A = self.encode(A)
        self.B = self.encode(B)

        self.result = [[None for i in range(len(self.B) + 1)]\
                       for i in range(len(self.A) + 1)]
        print(pandas.DataFrame(self.result))

        
        self.gap_cost = -5
        
        self.score_matrix = [[10,  2,  5,  2], # A
                             [ 2, 10,  2,  5], # C
                             [ 5,  2, 10,  2], # G
                             [ 2,  5,  2, 10]] # T
                           #   A   C   G   T

    # Helper methods

    def encode(self, input):
        mapping = {'A': 0, 'C': 1, 'G': 2, 'T':3}
        return [mapping[i] for i in str(input).upper()]


    def decode(self, input):
        demapping = {'0': 'A', '1': 'C', '2': 'G', '3': 'T', '-': '-'}
        return ''.join([demapping[str(i)] for i in input])


    # Core methods
    
    def dyn_score(self, i, j):
        #print(f'{i},{j}  ', end = '') # debug

        # Has it already been calculated?
        if self.result[i][j] != None:
            return self.result[i][j]

        # if not, calculate it..
        else:
            candidates = []

            if (i > 0) and (j > 0): # Diagonally
                candidates.append(self.dyn_score(i-1, j-1) + self.score_matrix[self.A[i-1]][self.B[j-1]]) #?)
            if (i > 0) and (j >= 0): # Left
                candidates.append(self.dyn_score(i-1, j) + self.gap_cost)
            if (i >= 0) and (j > 0): # Up
                candidates.append(self.dyn_score(i, j-1) + self.gap_cost)
            if (i == 0) and (j == 0): # Base case
                candidates.append(0) # ?

            self.result[i][j] = max(candidates)
            return self.result[i][j]

    def compute(self):
        # Pretty print everything
        print(f'\\n'
              f'input ({len(self.A)}x{len(self.B)})\n'
              #f'A:{self.A}'
              f'A ({self.decode(self.A)}) vertically\n'
              f'B ({self.decode(self.B)}) horizontally\n'
              f'\n'
              f'score ({self.dyn_score(len(self.A), len(self.B))})\n'
              f'{pandas.DataFrame(self.result)}\n')


    def backtrack(self, method = 'single'):

        def rec_backtrack_single(i, j):
            """ Recursive backtrack. """

            #print(i, j, sep = ',', end = ' ')

            if i > 0 and j > 0 and self.result[i][j] == (self.result[i-1][j-1] + self.score_matrix[self.A[i-1]][self.B[j-1]]):
                string_a, string_b = rec_backtrack_single(i - 1, j - 1)
                return string_a + str(self.A[i-1]), string_b + str(self.B[j-1])

            elif i > 0 and j >= 0 and self.result[i][j] == (self.result[i - 1][j] + self.gap_cost):
                string_a, string_b = rec_backtrack_single(i - 1, j)
                return string_a + str(self.A[i - 1]), string_b + '-'

            elif i >= 0 and j > 0 and self.result[i][j] == (self.result[i][j-1] + self.gap_cost):
                string_a, string_b = rec_backtrack_single(i, j - 1)
                return string_a + '-', string_b + str(self.B[j-1])

            elif i == 0 and j == 0:
                return '', ''

        pri_list = [] # faster than returning?
        def rec_backtrack_multiple(i, j, string_A, string_B):
            """ Recursive backtrack. 
                multiple, heavy stack"""

            #print(i, j, sep = ',', end = ' ')

            if i > 0 and j > 0 and self.result[i][j] == (self.result[i-1][j-1] + self.score_matrix[self.A[i-1]][self.B[j-1]]):
                rec_backtrack_multiple(i - 1, j - 1, string_A + str(self.A[i-1]), string_B + str(self.B[j-1]))

            if i > 0 and j >= 0 and self.result[i][j] == (self.result[i - 1][j] + self.gap_cost):
                rec_backtrack_multiple(i - 1, j, string_A + str(self.A[i - 1]), string_B + '-')

            if i >= 0 and j > 0 and self.result[i][j] == (self.result[i][j-1] + self.gap_cost):
                rec_backtrack_multiple(i, j - 1, string_A + '-', string_B + str(self.B[j-1]))

            if i == 0 and j == 0:
                pri_list.append((self.decode(string_A[::-1]), self.decode(string_B[::-1])))


        if method == 'single':
            print('\n\nSingle solution:')
            backtracked_A, backtracked_B = rec_backtrack_single(len(self.A), len(self.B))
            print(f'{self.decode(backtracked_B)}\n{self.decode(backtracked_A)}')

        if method == 'multiple':
            print('\n\nMultiple solutions:')
            rec_backtrack_multiple(len(self.A), len(self.B), '','') 
            print(pri_list) # not exactly a nice way to print it..


o = Pairwise_alignment('CGTGTCAAGTCT', 'ACGTCGTAGCTAGG')

o.compute()

o.backtrack('single') # single | multiple
