
center_string = ['A', 'C', 'T']

aligned_pairs = [[['A', 'C', '-', 'T'],
                  ['A', '-', 'T', 'T']],
                 [['A', '-', 'C', 'T'],
                  ['-', 'T', 'G', 'T']]]


def count_gaps_in_center_string(center_string, aligned_pairs):
    gap_at_idx = [[0 for i in range(len(aligned_pairs))] for i in range(len(center_string)+1)] # note: transposed!!
    for pair_idx, pair in enumerate(aligned_pairs):
        cum_sum = 0
        for i_idx, i_value in enumerate(pair[0]):
            if i_value == '-':
                gap_at_idx[i_idx - cum_sum][pair_idx] += 1
                cum_sum += 1

    #print('gap_at_idx:', gap_at_idx) # debug

    rv = [0 for i in range(len(center_string)+1)]
    for i_idx, i in enumerate(gap_at_idx):
        rv[i_idx] = max(i)

    return rv


dash_list = count_gaps_in_center_string(center_string, aligned_pairs)
print('dash_list:', dash_list)


def expand_center_string_with_gaps(center_string, dash_list):
    rv = '-' * dash_list[0]
    for idx, letter in enumerate(center_string):
        rv += letter
        rv += '-' * dash_list[idx+1]
    return [i for i in rv]

center_string = expand_center_string_with_gaps(center_string, dash_list)
print('cs', center_string)

"""
Så, nu er center strengen udvidet med gaps så meget som den behøver.
Nu kan vi gå i gang med at lave vores multiple alignment.
"""

def align_multiple(center_string, aligned_pairs):
    msa = [center_string] + [[None for i in range(len(center_string))] for i in range(len(aligned_pairs))] # alloker fuld størrelse af msa
    for i, i_val in enumerate(aligned_pairs): # for hvert par ..
        j_offset = 0
        for j, j_val in enumerate(center_string): # .. gå igennem hver position i den paddede centerstreng
            print(j, i_val[0][j-j_offset], j_val, end = ' ' * 5)
            if i_val[0][j-j_offset] != j_val:
                msa[i+1][j-j_offset] = '-'
                j_offset += 1
            else:
                msa[i+1][j] = i_val[1][j-j_offset]
    return msa




msa = align_multiple(center_string, aligned_pairs)
print('\nfinal msa:')
for i, i_val in enumerate(msa):
    print(i, end = ') ')
    for j in i_val:
        print(f'{j}  ', end = '')
    print()

sum_list = [0 for i in range(len(center_string))]
for i in msa:





