from pandas import DataFrame #pretty print result 2d-array
#import numpy as np # overkill

# Author: Carl M. Kobel 2018

#   ~ todo ~
# * backtracking with multiple results (recursively?) (doable manually..)
# * linear gap cost (not affine!) 
# * cli?
# * optimization?


def encode(input):
    return [int(i.replace('A', '0')\
                 .replace('C', '1')\
                 .replace('G', '2')\
                 .replace('T', '3')) for i in input]

def decode(input):
    return ''.join(str(i).replace('0', 'A')\
                         .replace('1', 'C')\
                         .replace('2', 'G')\
                         .replace('3', 'T') for i in input)


# Constants
A = encode('CGTGTCAAGTCT'.upper())
B = encode('ACGTCGTAGCTAGG'.upper())
gap_cost = -5
result = [[None for i in range(len(B) + 1)]\
                for i in range(len(A) + 1)]

# vector = [[None for i in range(len(B) + 1)]\
#                 for i in range(len(A) + 1)]

score_matrix = [[10,  2,  5,  2], # A
                [ 2, 10,  2,  5], # C
                [ 5,  2, 10,  2], # G
                [ 2,  5,  2, 10]] # T
               #  A   C   G   T


# Helper methods
def drop_None(input):
    return [i for i in input if i != None]

def dyn_score(i, j):
    #print(f'{i},{j}  ', end = '')

    # Has it already been calculated?
    if result[i][j] != None:
        return result[i][j]

    # if not, calculate it..
    else:
        v0 = v1 = v2 = v3 = None #?

        if (i > 0) and (j > 0): # Diagonally
            v0 = dyn_score(i-1, j-1) + score_matrix[A[i-1]][B[j-1]] #?
        if (i > 0) and (j >= 0): # Left
            v1 = dyn_score(i-1, j) + gap_cost
        if (i >= 0) and (j > 0): # Up
            v2 = dyn_score(i, j-1) + gap_cost
        if (i == 0) and (j == 0): # Base case
            v3 = 0

        candidates = [v0, v1, v2, v3]
        result[i][j] = max(drop_None(candidates))
        #vector[i][j] = candidates.index(result[i][j])
        return result[i][j]


# Pretty print everything
print(f'''\


input ({len(A)}x{len(B)})
A ({decode(A)}) vertically
B ({decode(B)}) horizontally

score ({dyn_score(len(A), len(B))})
{DataFrame(result)}

''')