class FirstClass: # 클래스 작성
    def __init__(self, name, age, grade): # 초기화 메서드. 사실상 생성자 취급
       self.name = name
       self.age = age
       self.grade = grade

    def age_get(self):
        return self.age

    def age_set(self, age):
        if age >= 0:
            self.age = age

    def intro(self, greeting):
        print(f"{greeting}, 이름은 {self.name}이고 나이는 {self.age}살이며 학점은 {self.grade}입니다.")

p1 = FirstClass("david", 40, 4.5) # 개체 생성

# 출력
print(p1.name)
print(p1.age)
print(p1.grade)

p1.intro("안녕하세요!")

print("구분선-----------------------------------")

# 접근자(getter)와 설정자(setter)
print(p1.age_get()) # 접근자(getter)는 메서드이므로 절대로 소괄호를 빼먹으면 안 된다!
p1.age_set(10)
print(p1.age)
print(p1.age_get())

# 인스턴스 변수 직접 접근
print("인스턴스 변수 직접 접근")
p1.age = 15
print(p1.age)
print(p1.age_get())

# 관습상 private 멤버 변수를 지닌 클래스
class secret:
    def __init__(self, name, age):
        self._name = name
        self._age = age
        self._dummy = 10 # 인스턴스 변수

    def age_set(self, age):
        self._age = age

    def age_get(self):
        return self._age

    def name_get(self):
        return self._name

print("구분선-------------------------------------")
kingsman = secret("에그시", 20)
print(kingsman.age_get())
print(kingsman.name_get())
kingsman.age_set(30)
print(kingsman._age)
print(kingsman.age_get())

x = kingsman.age_get()
print(x)

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