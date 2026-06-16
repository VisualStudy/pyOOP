import numpy as np

MyList = [10, "A", 30, 'B' ,50]
MyArray = np.array([10, 20, 30, 40, 50])

MyList1 = MyList * 2
print(MyList1)

# MyList2 = MyList + 1
MyList2 = MyList + [1]
print(MyList2)

MyArray1 = MyArray * 10
print(MyArray1)

MyArray2 = MyArray + 5
print(MyArray2)