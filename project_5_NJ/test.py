import numpy as np



def right_top_coordinates(dim):
    j_start = 1
    for i in range(dim-1):
        for j in range(dim)[j_start::]:
            yield((i, j))
        j_start += 1


li = list(right_top_coordinates(4))

print(li)



