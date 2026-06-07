import numpy as np

arr = np.arange(1, 10).reshape(3, 3)

print(arr)
print(arr[1])
print(arr[:, 2])
print(arr[arr % 2 == 1])
print(arr * 10)