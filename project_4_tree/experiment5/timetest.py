import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import rfdist
import time

print(f'i, iplusone, time, distance')
for i in range(2, 395):



    replicates = 10
    time_sum = 0
    for j in range(replicates):


        t0 = time.time()
        o = rfdist.Robinson_Foulds_distance(f'inc_newick/out_{i}.new',
                                            f'inc_newick/out_{i+1}.new')
        score = o.distance
        t1 = time.time()

        time_sum += t1-t0


    print(f'{i}, {i+1}, {time_sum / replicates}, {score}')
    time_sum = 0
    