gap_cost = 0       
score_matrix = [[1, 0, 0, 0], # a
                [0, 1, 0, 0], # c
                [0, 0, 1, 0], # t
                [0, 0, 0, 1]] # g
               # a  c  t  g 


def encode(input):
    return [int(i.replace('a', '0')\
                 .replace('c', '1')\
                 .replace('t', '2')\
                 .replace('g', '3')) for i in input]


A = encode('acgatgat')
B = encode('acgatgac')


def score(i, j):
    v1 = v2 = v3 = 0

    if (i > -1) and (j > -1):
        v1 = score(i-1, j-1) + score_matrix[A[i]][B[j]]
    if (i > -1) and (j >= -1):
        v2 = score(i-1, j) + gap_cost
    if (i >= -1) and (j > -1):
        v3 = score(i, j-1) + gap_cost

    return max([v1, v2, v3])


print(f'''\
A:  {A}
B:  {B}

score: {score(len(A)-1, len(B)-1)}
''')