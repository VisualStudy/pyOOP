def facto(num):
    if num == 0 or num == 1:
        print("1")
        return 1

    print(f"{num}", end=" * ")
    return num * facto(num - 1)

n = int(input("Enter a number: "))

print(f"The factorial of {n} is: {facto(n)}")