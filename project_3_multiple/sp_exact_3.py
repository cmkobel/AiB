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
        self.P = [[[None for i in range(len(self.C))] for i in range(len(self.B))] for i in range(len(self.A))]

        #           A  C  G  T 
        self.SM = [[0, 5, 2, 5], # Substitution Matrix
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
                if i < len(self.A)-1:
                    if j >= 0:
                        rv += '\n'
                    if j >= 1:
                        rv += '|'

                    if j >= 2:
                        rv += j * ' '
                else:
                    rv += '\n' + j* ' '
                for k in range(len(self.C)):
                    rv += str(input[i][j][k])
                    if (j == 0 or j == len(self.B)) and k < len(self.C)-1:
                        rv += ' ' + '.' * ((len(self.B) + len(self.C)) - 1) + ' '
                    else:
                        rv += ' ' + ' ' * (len(self.B) + len(self.C))
        return rv



    def align(self, fill_P = False): # todo gives an error if False
        """ Non-recursive, who gives a duck?
        I'm assuming this is linear gapcost? 
        regner med at implementere backtracking direkte her. Genvej, nemmere end at lave en backtrack algo ved siden af. Get it over with.
        """
        for i in range(len(self.A)):
            for j in range(len(self.B)):
                for k in range(len(self.C)):
                    T_cand = [] # T_candidates list
                    arrow = []

                    if i == 0 and j == 0 and k == 0:
                        T_cand.append(0) # Det der skal stå i T?
                        if fill_P: arrow.append(0)
                    if i > 0 and j > 0 and k > 0: # diag
                        T_cand.append(self.T[i-1][j-1][k-1] + self.SM[self.A[i]][self.B[j]] + self.SM[self.B[j]][self.C[k]] + self.SM[self.A[i]][self.C[k]])
                        if fill_P: arrow.append(1)
                    if i > 0 and j > 0 and k >= 0:
                        T_cand.append(self.T[i-1][j-1][k] + self.SM[self.A[i]][self.B[j]] + self.GAP + self.GAP)
                        if fill_P: arrow.append(2)
                    if i > 0 and j >= 0 and k > 0:
                        T_cand.append(self.T[i-1][j][k-1] + self.GAP + self.SM[self.A[i]][self.C[k]] + self.GAP)
                        if fill_P: arrow.append(3)
                    if i >= 0 and j > 0 and k > 0:
                        T_cand.append(self.T[i][j-1][k-1] + self.GAP + self.GAP + self.SM[self.B[j]][self.C[k]])
                        if fill_P: arrow.append(4)
                    if i > 0 and j >= 0 and k >= 0:
                        T_cand.append(self.T[i-1][j][k] + self.GAP + self.GAP)
                        if fill_P: arrow.append(5)
                    if i >= 0 and j > 0 and k >= 0:
                        T_cand.append(self.T[i][j-1][k] + self.GAP + self.GAP)
                        if fill_P: arrow.append(6)
                    if i >= 0 and j >= 0 and k > 0:
                        T_cand.append(self.T[i][j][k-1] + self.GAP + self.GAP)
                        if fill_P: arrow.append(7)
                    #print(f'T at {i, j, k}: {self.T}')
                    #print(f'T_cand at {i, j, k}: {T_cand}')

                    best = min(T_cand)
                    self.T[i][j][k] = best
                    if fill_P:
                        self.P[i][j][k] = arrow[T_cand.index(best)]
                        print(f'{i, j, k}: {best} @ {T_cand.index(best)} in {T_cand}')
        return self.T


    def backtrack(self):
        def osingle(i, j):
            """ Recursive backtrack. """


            # old
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

            #new 
            if i > 0 and j > 0 and k > 0 and self.T[i][j][k] == (self.T[i-1][j-1][k-1] + self.SM[self.A[i]][self.B[j]] + self.SM[self.B[j]][self.C[k]] + self.SM[self.A[i]][self.C[k]]):
                pass


            # det her bliver simpelthen for langhåret. Nu implementerer jeg hele lortet i align(), og så må jeg abstrahere fra en dårlige kørselstid på en anden måde.

        for i in range(len(self.A)):
            for j in range(len(self.B)):
                for k in range(len(self.C)):
                    pass



o = SP_exact_3('AAA', 'AAA', 'AAA')
print(f"""
A ({o.A})
B ({o.B})
C ({o.C}) {''.join([o.decode(str(i), join = True) for i in o.C])}

align:
{o._3dprint(o.align(fill_P = False))}

{o._3dprint(o.P)}






""")
#lazittest trashmsaster