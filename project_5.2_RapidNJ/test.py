import numpy as np




a = np.arange(0, 9).reshape(3, 3)
print(a)


np.fill_diagonal(a, 100)

print(a)
