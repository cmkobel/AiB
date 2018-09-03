import pandas #pretty print result 2d-array # too slow
#import json
#import numpy as np # overkill

# Author: Carl M. Kobel 2018

#   ~ todo ~
# * backtracking with multiple results (recursively?) (doable manually..)
# * linear gap cost (not affine!) 
# * cli?
# * optimization?


class Pairwise_alignment:
    '''with linear gap cost'''

    def __init__(self, A, B):
        
        # Constants
        self.A = self.encode(A)
        self.B = self.encode(B)

        self.gap_cost = -5
        self.result = [[None for i in range(len(self.B) + 1)]\
                       for i in range(len(self.A) + 1)]

        # vector = [[None for i in range(len(B) + 1)]\
        #                 for i in range(len(A) + 1)]

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


    def drop_None(self, input):
        return [i for i in input if i != None]
        # use enumerate instead?


    def idx_of_max(self, input):
        ''' Get indices of the maximum values in the input list '''
        return [index for (index, value) in enumerate(input) if value == max(input)]


    # Core methods
    def dyn_score(self, i, j):
        #print(f'{i},{j}  ', end = '') # debug

        # Has it already been calculated?
        if self.result[i][j] != None:
            return self.result[i][j]

        # if not, calculate it..
        else:
            v0 = v1 = v2 = v3 = None #?

            if (i > 0) and (j > 0): # Diagonally
                v0 = self.dyn_score(i-1, j-1) + self.score_matrix[self.A[i-1]][self.B[j-1]] #?
            if (i > 0) and (j >= 0): # Left
                v1 = self.dyn_score(i-1, j) + self.gap_cost
            if (i >= 0) and (j > 0): # Up
                v2 = self.dyn_score(i, j-1) + self.gap_cost
            if (i == 0) and (j == 0): # Base case
                v3 = 0

            candidates = [v0, v1, v2, v3]
            self.result[i][j] = max(self.drop_None(candidates))
            #vector[i][j] = candidates.index(result[i][j])
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


    def backtrack(self):

        def rec_backtrack(i, j):
            """
            Recursive backtrack.

            """

            print('i,j', i, j)

            if i > 0 and j > 0 and self.result[i][j] == (self.result[i-1][j-1] + self.score_matrix[self.A[i-1]][self.B[j-1]]):
                string_a, string_b = rec_backtrack(i - 1, j - 1)
                return string_a + str(self.A[i-1]), string_b + str(self.B[j-1])

            elif i > 0 and j >= 0 and self.result[i][j] == (self.result[i - 1][j] + self.gap_cost):
                string_a, string_b = rec_backtrack(i - 1, j)
                return string_a + str(self.A[i - 1]), string_b + '-'

            elif i >= 0 and j > 0 and self.result[i][j] == (self.result[i][j-1] + self.gap_cost):
                string_a, string_b = rec_backtrack(i, j - 1)
                return string_a + '-', string_b + str(self.B[j-1])

            elif i == 0 and j == 0:
                return '', ''



        backtrackedA, backtrackedB = rec_backtrack(len(self.A), len(self.B))
        print('\nSolution')
        print(f'{self.decode(backtrackedB)}\n{self.decode(backtrackedA)}')





o = Pairwise_alignment('CGTGTCAAGTCT', 'ACGTCGTAGCTAGG')

o.compute()

o.backtrack()