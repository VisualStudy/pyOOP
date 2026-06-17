import numpy as np

# 리스트 like 정의 부분
MyList = [10, "A", 30, 'B' ,50]
MyArray = np.array([10, 20, 30, 40, 50])

print("리스트")

MyList1 = MyList * 2
print(MyList1)

# MyList2 = MyList + 1
MyList2 = MyList + [1]
print(MyList2)

MyList3 = MyList + [1, 2]
print(MyList3)
# MyList4 = MyList * [1, 2]

print("numpy 배열")

MyArray1 = MyArray * 10
print(MyArray1)

MyArray2 = MyArray + 5
print(MyArray2)

MyArray3 = MyArray * [10]
print(MyArray3)

MyArray4 = MyArray + [5]
print(MyArray4)