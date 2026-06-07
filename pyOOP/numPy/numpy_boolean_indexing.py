import numpy as np

arr = np.array([10, 20, 30, 40, 50])

print(arr > 30)
# 결과: [False False False  True  True]

# 다시 배열에 넣어 값 뽑기
print(arr[arr > 30])
# 이때 파이썬의 and, or 사용 불가: & 등 사용