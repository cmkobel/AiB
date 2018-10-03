# Author: Carl M. Kobel 2018

# Implements the exact algorithm for computing an optimal MSA of 3 sequences and its score (described on page 408 in BA, or in section 16.6.1 in Gusfield's book).

class SP_exact_3:
    def __init__(self, A, B, C):
        self.ALPHABET = ['A', 'C', 'G', 'T']
        self.A = self.encode(A)
        self.B = self.encode(B)
        self.C = self.encode(C)
        self.GAP = 5
        self.T = [[[None for i in range(len(self.C)+1)] for i in range(len(self.B)+1)] for i in range(len(self.A)+1)]
        self.P = [[[None for i in range(len(self.C)+1)] for i in range(len(self.B)+1)] for i in range(len(self.A)+1)]

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
        """ Super pretty printer of 3-dimensional arrays """
        rv = '''
0-- C
|\\
| B
A
'''
        
        for i in range(len(self.A)+1):
            for j in range(len(self.B)+1):
                if i < len(self.A):
                    rv += '\n'
                    if j >= 1:
                        rv += '|'
                    if j >= 2:
                        rv += j * ' '
                else:
                    rv += '\n' + j* ' '
                for k in range(len(self.C)+1):
                    rv += str(input[i][j][k])
                    if (j == 0 or j == len(self.B)) and k < len(self.C):
                        rv += ' ' + '.' * ((len(self.B) + len(self.C))-1) + ' '
                    else:
                        rv += ' ' + ' ' * (len(self.B) + len(self.C))
        return rv



    def align(self, trace = False): # todo gives an error if False
        """ Non-recursive, because that is why.
        Assuming linear gapcost.
        backtracking er implementeret direkte her. Genvej, nemmere end at lave en backtrack algo ved siden af. Get it over with.
        """
        for i in range(len(self.A)+1):
            for j in range(len(self.B)+1):
                for k in range(len(self.C)+1):
                    T_cand = [] # T_candidates list
                    P_cand = []
                    if i == 0 and j == 0 and k == 0: # origo
                        T_cand.append(0)
                        if trace: P_cand.append(0)
                    
                    if i > 0 and j > 0 and k > 0: # diag (no gap)
                        T_cand.append(self.T[i-1][j-1][k-1] + self.SM[self.A[i-1]][self.B[j-1]] + self.SM[self.B[j-1]][self.C[k-1]] + self.SM[self.A[i-1]][self.C[k-1]])
                        if trace: P_cand.append(1)
                    
                    if i > 0 and j > 0 and k >= 0: # gap in C
                        T_cand.append(self.T[i-1][j-1][k] + self.SM[self.A[i-1]][self.B[j-1]] + self.GAP + self.GAP)
                        if trace: P_cand.append(2)
                    if i > 0 and j >= 0 and k > 0: # gap in B
                        T_cand.append(self.T[i-1][j][k-1] + self.GAP + self.SM[self.A[i-1]][self.C[k-1]] + self.GAP)
                        if trace: P_cand.append(3)
                    if i >= 0 and j > 0 and k > 0: # gap in A
                        T_cand.append(self.T[i][j-1][k-1] + self.GAP + self.GAP + self.SM[self.B[j-1]][self.C[k-1]])
                        if trace: P_cand.append(4)
                    
                    if i > 0 and j >= 0 and k >= 0: # gap in B, C
                        T_cand.append(self.T[i-1][j][k] + self.GAP + self.GAP)
                        if trace: P_cand.append(5)
                    if i >= 0 and j > 0 and k >= 0: # gap in A, C
                        T_cand.append(self.T[i][j-1][k] + self.GAP + self.GAP)
                        if trace: P_cand.append(6)
                    if i >= 0 and j >= 0 and k > 0: # gap in A, B
                        T_cand.append(self.T[i][j][k-1] + self.GAP + self.GAP)
                        if trace: P_cand.append(7)
                    
                    #print(f'T at {i, j, k}: {self.T}')
                    #print(f'T_cand at {i, j, k}: {T_cand}')

                    selected = min(T_cand)
                    self.T[i][j][k] = selected
                    if trace:
                        self.P[i][j][k] = P_cand[T_cand.index(selected)] # find the index of the selected value, and select the P_cand value at the same index (corresponding direction.
                        #print(f'{i, j, k}: {selected} @ {T_cand.index(selected)} in {T_cand}') # for debug.
        return self.T


    def backtrack(self):

        def single(i, j, k): # use the self.P 3d-array (code reuse)
            # Base case
            if i == 0 and j == 0 and k == 0: # end reached. return.
                return '', '', ''
            # Moving diagonally
            if self.P[i][j][k] == 1:
                string_a, string_b, string_c = single(i-1, j-1, k-1)
                return string_a + str(self.A[i-1]), string_b + str(self.B[j-1]), string_c + str(self.C[k-1])
            # Gap in one string
            if self.P[i][j][k] == 2:
                string_a, string_b, string_c = single(i-1, j-1, k)
                return string_a + str(self.A[i-1]), string_b + str(self.B[j-1]), string_c + '-'
            if self.P[i][j][k] == 3:
                string_a, string_b, string_c = single(i-1, j, k-1)
                return string_a + str(self.A[i-1]), string_b + '-', string_c + str(self.C[k-1])
            if self.P[i][j][k] == 4:
                string_a, string_b, string_c = single(i, j-1, k-1)
                return string_a + '-', string_b + str(self.B[j-1]), string_c + str(self.C[k-1])
            # Gap in two strings
            if self.P[i][j][k] == 5:
                string_a, string_b, string_c = single(i-1, j, k)
                return string_a + str(self.A[i-1]), string_b + '-', string_c + '-'
            if self.P[i][j][k] == 6:
                string_a, string_b, string_c = single(i, j-1, k)
                return string_a + '-', string_b + str(self.B[j-1]), string_c + '-'
            if self.P[i][j][k] == 7:
                string_a, string_b, string_c = single(i, j, k-1)
                return string_a + '-', string_b + '-', string_c + str(self.C[k-1])

        return single(len(self.A), len(self.B), len(self.C))





o = SP_exact_3('GTTCCGAAAGGCTAGCGCTAGGCGCC',
               'ATGGATTTATCTGCTCTTCG',
               'TGCATGCTGAAACTTCTCAACCA')

o = SP_exact_3('GTTCCGAAAGGCTAGCGCTAGGCGCCAAGCGGCCGGTTTCCTTGGCGACGGAGAGCGCGGGAATTTTAGATAGATTGTAATTGCGGCTGCGCGGCCGCTGCCCGTGCAGCCAGAGGATCCAGCACCTCTCTTGGGGCTTCTCCGTCCTCGGCGCTTGGAAGTACGGATCTTTTTTCTCGGAGAAAAGTTCACTGGAACTG',
               'ATGGATTTATCTGCTCTTCGCGTTGAAGAAGTACAAAATGTCATTAACGCTATGCAGAAAATCTTAGAGTGTCCCATCTGTCTGGAGTTGATCAAGGAACCTGTCTCCACAAAGTGTGACCACATATTTTGCAAATTTTGCATGCTGAAACTTCTCAACCAGAAGAAAGGGCCTTCACAGTGTCCTTTATGTAAGAATGA',
               'CGCTGGTGCAACTCGAAGACCTATCTCCTTCCCGGGGGGGCTTCTCCGGCATTTAGGCCTCGGCGTTTGGAAGTACGGAGGTTTTTCTCGGAAGAAAGTTCACTGGAAGTGGAAGAAATGGATTTATCTGCTGTTCGAATTCAAGAAGTACAAAATGTCCTTCATGCTATGCAGAAAATCTTGGAGTGTCCAATCTGTTT')

print(f"""
A ({o.A})
B ({o.B})
C ({o.C}) {''.join([o.decode(str(i), join = True) for i in o.C])}

align:
""")
o.align(trace = True)

#{o._3dprint(o.P)}
"""
"""
#present the aligned strings.
for i in o.backtrack(): print(o.decode(i, join = True)[::1])