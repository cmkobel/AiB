SM = [[0, 5, 2, 5], # Substitution Matrix
      [5, 0, 5, 2],
      [2, 5, 0, 5],
      [5, 2, 5, 0]]
ALPHABET = ['A', 'C', 'G', 'T']
GAP = 5

center_string = ['A', 'C', 'T']

aligned_pairs = [
[['A', 'C', 'T'], ['A', 'T', 'T']], [['-', 'A', 'C', 'T'], ['A', 'A', 'G', 'G']]
                ]




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
    print('msa', msa)
    for i, i_val in enumerate(aligned_pairs): # for hvert par ..
        lag = 0
        for j, j_val in enumerate(center_string): # .. gå igennem hver position i den paddede centerstreng
            #print(j, i_val[0][j-lag], j_val, end = ' ' * 4)
            print(i, j)
            if i_val[0][j-lag] != j_val:
                msa[i+1][j] = '-'
                lag += 1
            else:
                msa[i+1][j] = i_val[1][j-lag]
                if j-lag+1 == len(i_val[1]): # hvis vi har skrevet det sidste element, så sørg for at vi ikke går over range i S^i
                    lag += 1 
    return msa

# debug printing:
msa = align_multiple(center_string, aligned_pairs)
print('\n\nfinal msa:')
for i, i_val in enumerate(msa):
    print(i, end = ') ')
    for j in i_val:
        print(f'{j}  ', end = '')
    print()


print('\ncomb')
sum_list = [0 for i in range(len(center_string))] # just to validate the values one column at a time. In the end, a sum value can just be sum += value
grand_total = 0
cols = len(center_string)
rows = len(msa)
for i in range(cols): # kolonner i msa
    for j in range(rows):
        for k in range(rows):
            if j < k:
                first = msa[j][i]
                second = msa[k][i]
                print(i,' ', j, k, first, second)
                sum = 0
                if first == '-' and second == '-':
                    continue
                elif first == '-' or second == '-':
                    sum += GAP
                else:
                    sum += SM[ALPHABET.index(first)][ALPHABET.index(second)]
                sum_list[i] += sum
                grand_total += sum
    
    print()

print(sum_list)
print(grand_total)



