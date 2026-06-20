class People:
    def __init__(self, name, age, gender, weight, height):
        self.name = name
        self.age = age
        self.gender = gender
        self.weight = weight
        self.height = height

    def intro(self):
        print(f"반갑다. 내 이름은 {self.name}. 나이는 {self.age}이며 {self.gender}다! 내 몸무게는 {self.weight}, 내 키는 {self.height}!")

class Ys(People):
    def __init__(self, name, age, gender, weight, height, grade, power=10):
        super().__init__(name, age, gender, weight, height)
        self.grade = grade
        self.power = power

    def intro(self):
        print(f"반갑다. 내 이름은 {self.name}. 나이는 {self.age}이며 {self.gender}다! 내 몸무게는 {self.weight}, 내 키는 {self.height}! 내 학점은 {self.grade}이고 내 힘은 {self.power}다!")

tjddb = Ys("앱스타인", 29, "남자", "99", "196", 3.9)

tjddb.intro()

