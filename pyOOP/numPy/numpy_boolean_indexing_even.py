import numpy as np

arr = np.array([3, 6, 9, 12, 15, 18])

print(arr[arr % 2 == 0])