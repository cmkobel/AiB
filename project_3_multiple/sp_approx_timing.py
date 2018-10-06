import sp_approx
import time

for i in range(10, 210, 10):
    
    replicates = 10
    mean_time_list = [None for i in range(replicates)]
    mean_score = 0
    for j in range(replicates):
        t0 = time.time()
        o = sp_approx.SP_approx(f'data/testseqs/testseqs_{i}_3.fasta')
        csi = o.center_string_index()
        score = o.build_alignment(csi)[1]
        t1 = time.time()
        mean_time_list[j] = t1-t0
        mean_score = score



    print(f'{i}, {sum(mean_time_list)/replicates}, {mean_score}')
    