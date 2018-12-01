import numpy as np



N = np.array([[1,0,3], [2,2,3]])

print(N)

ind = np.unravel_index(np.argmin(N, axis=None), N.shape)


print(ind[1])