class FirstClass: # 클래스 작성
    def __init__(self, name, age, grade): # 초기화 메서드. 사실상 생성자 취급
       self.name = name
       self.age = age
       self.grade = grade

    def intro(self, greeting):
        print(f"{greeting}, 이름은 {self.name}이고 나이는 {self.age}살이며 학점은 {self.grade}입니다.")

p1 = FirstClass("david", 40, 4.5) # 개체 생성

# 출력
print(p1.name)
print(p1.age)
print(p1.grade)

p1.intro("안녕하세요!")

print("구분선----------------------------\n")

list = [10, "x", 30, "y"] # 리스트 작성
print(list[0])
print(list[1])
print(list[-1])
print(list[:])            # 슬라이싱은 새로운 리스트 생성과 동일: [ ]와 " " 같이 출력
print(list[:2])
print(list[1:])
print(list[::2])
print(list[1:2:2])
print(list[1::2])
print(list)