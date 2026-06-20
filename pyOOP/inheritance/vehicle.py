class Vehicle:
    def __init__(self, name):
        self.name = name

    def move(self):
        print(f"{self.name} 이동!")

class Car(Vehicle):
    def honk(self):
        print("빵빵!")

car = Car("붕붕")
car.move()
car.honk()