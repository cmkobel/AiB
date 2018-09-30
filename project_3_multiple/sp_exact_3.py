# Author: Carl M. Kobel 2018

# Implements the exact algorithm for computing an optimal MSA of 3 sequences and its score (described on page 408 in BA, or in section 16.6.1 in Gusfield's book).

class SP_exact_3:
    def __init__(self, A, B, C):
        self.ALPHABET = ['A', 'C', 'G', 'T']
        self.A = self.encode(A)
        self.B = self.encode(B)
        self.C = self.encode(C)
        self.GAP = 5
        self.T = [[[None for i in range(len(self.C))] for i in range(len(self.B))] for i in range(len(self.A))]

        #           A  C  G  T 
        self.SM = [[0, 5, 2, 5],
                   [5, 0, 5, 2],
                   [2, 5, 0, 5],
                   [5, 2, 5, 0]]



    def encode(self, input):
        """ Take a string 'ACGT', returns a list of numbers [0, 1, 2, 3]"""
        mapping = {letter: index for index, letter in enumerate(self.ALPHABET)}
        return [mapping[i] for i in str(input).upper()]
    def decode(self, input, join = False):
        """ Takes a string '0123-', returns a list of letters ['A', 'C'..] or 'AC' if join is true"""
        demapping = {str(index): letter for index, letter in enumerate(self.ALPHABET)}
        demapping['-'] = '-' # add the gap 'letter'
        if join:
            return ''.join([demapping[i] for i in input])
        else:
            return [demapping[i] for i in input]
    
    def _3dprint(self, input):
        rv = '''
0-- C
|\\
| B
A
'''
        
        for i in range(len(self.A)):
            for j in range(len(self.B)):
                rv += '\n' + j * ' '
                for k in range(len(self.C)):
                    rv += str(input[i][j][k]) + ' ' + ' ' * (len(self.B) + len(self.C))
        return rv





    def align(self):
        """ I'm assuming this is liner gapcost? """
        for i in range(len(self.A)):
            for j in range(len(self.B)):
                for k in range(len(self.C)):
                    cand = [] # candidates list

                    if i == 0 and j == 0 and k == 0:
                        cand.append(0) # Det der skal stå i T?

                    if i > 0 and j > 0 and k > 0: # diag
                        cand.append(self.T[i-1][j-1][k-1] + self.SM[self.A[i]][self.B[j]] + self.SM[self.B[j]][self.C[k]] + self.SM[self.A[i]][self.C[k]])

                    if i > 0 and j > 0 and k >= 0:
                        cand.append(self.T[i-1][j-1][k] + self.SM[self.A[i]][self.B[j]] + self.GAP + self.GAP)

                    if i > 0 and j >= 0 and k > 0:
                        cand.append(self.T[i-1][j][k-1] + self.GAP + self.SM[self.A[i]][self.C[k]] + self.GAP)

                    if i >= 0 and j > 0 and k > 0:
                        cand.append(self.T[i][j-1][k-1] + self.GAP + self.GAP + self.SM[self.B[j]][self.C[k]])

                    if i > 0 and j >= 0 and k >= 0:
                        cand.append(self.T[i-1][j][k] + self.GAP + self.GAP)

                    if i >= 0 and j > 0 and k >= 0:
                        cand.append(self.T[i][j-1][k] + self.GAP + self.GAP)

                    if i >= 0 and j >= 0 and k > 0:
                        cand.append(self.T[i][j][k-1] + self.GAP + self.GAP)

                    #print(f'T at {i, j, k}: {self.T}')
                    #print(f'cand at {i, j, k}: {cand}')

                    self.T[i][j][k] = min(cand)
        return self.T





o = SP_exact_3('AAATCG', 'GGGGG', 'GGGGG')
print(f"""
A ({o.A})
B ({o.B})
C ({o.C}) {''.join([o.decode(str(i), join = True) for i in o.C])}

align:
{o._3dprint(o.align())}






""")
