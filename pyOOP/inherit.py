class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("동물이 소리를 냅니다.")

class Dog(Animal):
    def speak(self):
        print(f"{self.name}가 멍멍 짓습니다.")

dog = Dog("밀크")

dog.speak()