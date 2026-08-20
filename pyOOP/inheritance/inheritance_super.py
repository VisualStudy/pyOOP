class Person:
    def __init__(self, name):
        self.name = name
        print("Person의 __init__ 실행")

    def introduce(self):
        print(f"안녕하세요. 제 이름은 {self.name}입니다.")

class Student(Person):
    def __init__(self, name, student_id, major):
        # 부모 클래스 Person의 __init__ 실행
        super().__init__(name)

        # Student만의 추가 속성
        self.student_id = student_id
        self.major = major

        print("Student의 __init__ 실행")

    def introduce(self):
        # 부모 클래스의 introduce() 먼저 실행
        super().introduce()

        # Student만의 소개 내용 추가
        print(f"학번은 {self.student_id}이고, 전공은 {self.major}입니다.")

    def study(self):
        print(f"{self.name}이/가 {self.major} 공부를 합니다.")

student = Student("지은", "20260001", "간호학")

print()

student.introduce()

print()

student.study()