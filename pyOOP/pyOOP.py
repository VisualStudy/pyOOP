class FirstClass: # 클래스 작성
    def __init__(self, name, age, grade): # 초기화 메서드. 사실상 생성자 취급
       self.name = name
       self.age = age
       self.grade = grade

p1 = FirstClass("david", 40, 4.5) # 개체 생성

# 출력
print(p1.name)
print(p1.age)
print(p1.grade)