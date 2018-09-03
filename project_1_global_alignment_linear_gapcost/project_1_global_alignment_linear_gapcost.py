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
        self.A = self.encode(A.upper())
        self.B = self.encode(B.upper())

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
        return [int(i.replace('A', '0')\
                     .replace('C', '1')\
                     .replace('G', '2')\
                     .replace('T', '3')) for i in input]

    def decode(self, input):
        return ''.join(str(i).replace('0', 'A')\
                             .replace('1', 'C')\
                             .replace('2', 'G')\
                             .replace('3', 'T') for i in input)


    def drop_None(self, input):
        return [i for i in input if i != None]
        # use enumerate instead?


    def idx_of_max(self, input):
        ''' Get indices of the maximum values in the input list '''
        return [index for (index, value) in enumerate(input) if value == max(input)]


    # core methods
    

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

    def complete(self):
        # Pretty print everything
        print(f'''\
input ({len(self.A)}x{len(self.B)})
A ({self.decode(self.A)}) vertically
B ({self.decode(self.B)}) horizontally

score ({self.dyn_score(len(self.A), len(self.B))})
{pandas.DataFrame(self.result)}
''')

    def backtrack(self):


        def rec_backtrack(track, i, j):
            ''' Recursive backtrack.
            * Add option to save aligned string instead of track '''

            track[i+j] = (i, j) # enter newly found position into track
            print('i, j:', i, j)


            candidates = []

            if i > 0 and j > 0: 
                candidates.append(self.result[i-1][j-1]) # diagonal
            if i > 0 and j >= 0:
                candidates.append(self.result[i-1][j]) # up
            if i >= 0 and j > 0:
                candidates.append(self.result[i][j-1]) # left
            else: #
                print(track) # base case

            for candidate in self.idx_of_max(candidates): #"lc later"
                print('candidates (list, idx):', candidates, candidate)
                possibilities = [(i-1, j-1), (i-1, j), (i, j-1)]
                print('possibilities', possibilities[candidate])
                rec_backtrack(track, possibilities[candidate][0], possibilities[candidate][1])
                    
             
        empty_track = [None for i in range(len(self.A) + len(self.B) + 1)] # An empty list with the length of the track
        i, j = len(self.A), len(self.B) # Starting pointers, start in the bottom right corner
        
        rec_backtrack(empty_track, i, j)


o = Pairwise_alignment('ACG', 'CGTG')

o.complete()

o.backtrack()