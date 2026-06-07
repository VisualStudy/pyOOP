class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name}이/가 먹습니다.")

    def sleep(self):
        print(f"{self.name}이/가 잡니다.")

class Dog(Animal):
    def bark(self):
        print(f"{self.name}이/가 멍멍 짓습니다.")

dog = Dog("초코")

dog.eat()
dog.sleep()
dog.bark()