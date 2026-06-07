import numpy as np

arr = np.arange(12)

print(arr)
print(arr.reshape(3, 4))
print(arr.reshape(4, 3))
print(arr.reshape(2, -1))