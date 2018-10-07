import sp_exact_3
import time

for i in range(10, 210, 10):
    
    replicates = 10
    mean_time_list = [None for i in range(replicates)]
    mean_score = 0
    for j in range(replicates):
        t0 = time.time()
        

        o = sp_exact_3.SP_exact_3(f'data/testseqs/testseqs_{i}_3.fasta')
        #score = o.align(trace = False)[len(o.A)][len(o.B)][len(o.C)]
        score = o.align(trace = False)#[-1][-1][-1]#[len(o.A)][len(o.B)][len(o.C)]



        t1 = time.time()
        mean_time_list[j] = t1-t0
        mean_score = score



    print(f'{i}, {sum(mean_time_list)/replicates}, {mean_score}')
    