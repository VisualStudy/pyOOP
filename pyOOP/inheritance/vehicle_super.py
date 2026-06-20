class Vehicle:
    def __init__(self, name):
        self.name = name
        print("Vehicle 생성자 실행")

class Car(Vehicle):
    def __init__(self, name, fuel):
        super().__init__(name)
        self.fuel = fuel
        print("Car 생성자 실행")

car = Car("자동차", "경유")

print(car.name)
print(car.fuel)