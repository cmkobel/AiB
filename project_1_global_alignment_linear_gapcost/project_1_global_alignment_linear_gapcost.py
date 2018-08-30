from pandas import DataFrame #pretty print result 2d-array

gap_cost = -1
score_matrix = [[2, 0, 0, 0], # A
                [0, 2, 0, 0], # C
                [0, 0, 2, 0], # G
                [0, 0, 0, 2]] # T
               # A  C  G  T


def encode(input):
    return [int(i.replace('A', '0')\
                 .replace('C', '1')\
                 .replace('G', '2')\
                 .replace('T', '3')) for i in input]

def decode(input):
    return ''.join(str(input).replace('0', 'A')\
                             .replace('1', 'C')\
                             .replace('2', 'G')\
                             .replace('3', 'T')) # join gør intet


A = encode('A'.upper())
B = encode('A'.upper())

result = [[None for i in range(len(B) + 1)]\
             for i in range(len(A) + 1)]

def c_max(list, drop_None = True):
    rv = list[0]
    for i in list[1:]:
        if i != None:
            if i > rv: rv = i
    return rv

def dyn_score(i, j):
    print(f'i, j = {i}, {j}')

    # Has it already been calculated?
    if result[i][j] != None:
        return result[i][j]

    # if not, calculate it.
    else:
        v1 = v2 = v3 = v4 = -1000 #?

        if (i > 0) and (j > 0): # Diagonally
            v1 = dyn_score(i-1, j-1) + score_matrix[A[i-1]][B[j-1]] #?
        if (i > 0) and (j >= 0): # Horizontally
            v2 = dyn_score(i-1, j) + gap_cost
        if (i >= 0) and (j > 0): # Vertically
            v3 = dyn_score(i, j-1) + gap_cost
        if (i == 0) and (j == 0): # base case
            v4 = 0

        result[i][j] = c_max([v1, v2, v3, v4])
        return result[i][j]

print(f'''\
input:
A:  {A} ({decode(B)})
B:  {B}

score: {dyn_score(len(A), len(B))}

{DataFrame(result)}
''')



         

