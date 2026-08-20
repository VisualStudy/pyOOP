import numpy as np

arr = np.array([[10, 20, 30], [40, 50, 60], [70, 80, 90]])

print(arr[0, 0])
print(arr[1, 2])
print(arr[2, 1])

# 슬라이싱
print("--------------------")

print(arr[0]) # 0번째 행 전체
print(arr[:, 1]) # 모든 행에서 인덱스 1번째 열
print(arr[1:, :2]) # 인덱스 1번째 행부터 끝 행까지에서 2번 열 이전까지의 열 슬라이싱
