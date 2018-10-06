
center_string = ['A', 'C', 'T']

aligned_pairs = [[['A', 'C', '-', 'T'],
                  ['A', '-', 'T', 'T']],
                 [['A', '-', 'C', 'T'],
                  ['A', 'T', 'G', 'T']]]


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
print(dash_list)


rv = '-' * dash_list[0]
for key, value in enumerate(center_string):
    rv += ' ' * dash_list[1+key]
    rv += center_string[key]

print(rv)




