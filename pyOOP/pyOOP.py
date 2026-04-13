class FirstClass: # 클래스 작성
    def __init__(self, name, age, grade): # 초기화 메서드. 사실상 생성자 취급
       self.name = name
       self.age = age
       self.grade = grade

    def intro(self, greeting):
        print(f"이름은 {self.name}이고 나이는 {self.age}살이며 학점은 {self.grade}입니다.")

p1 = FirstClass("david", 40, 4.5) # 개체 생성

# 출력
print(p1.name)
print(p1.age)
print(p1.grade)

p1.intro("안녕하세요!")