myList = [10, 20, 30]
value = myList

value[1] = 50

print(myList)

value.sort()

print(value)

value2 = list(value)

value2[1] = 90

print(value)
print(value2)

value3 = sorted(value2)
value3[2] = 999
print(value2)
print(value3)