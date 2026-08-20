import numpy as np

arr = np.array([1, 2, 3, 4, 5, 6])

print(arr.reshape(2, -1))
# -1은 알아서 개수 맞게 만들어 달라는 의미