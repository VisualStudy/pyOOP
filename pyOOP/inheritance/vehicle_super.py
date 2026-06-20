class Vehicle:
    def __init__(self, name):
        self.name = name

class Car(Vehicle):
    def __init__(self, name, fuel):
        super().__init__(name)
        self.fuel = fuel

car = Car("자동차", "경유")

print(car.name)
print(car.fuel)