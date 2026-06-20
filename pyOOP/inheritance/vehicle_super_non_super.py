class Vehicle:
    def __init__(self, make, model, color, price):
        self.make = make
        self.model = model
        self.color = color
        self.price = price
        print("부모 초기화 메서드 발동!")

    def setMake(self, make):
        self.make = make

    def getMake(self):
        return self.make

class Truck(Vehicle):
    def __init__(self, make, model, color, price, payload):
        super().__init__(make, model, color, price)
        self.payload = payload

    def setPayload(self, payload):
        self.payload = payload

    def getPayload(self):
        return self.payload

dump = Truck("라바라타국", "부릉이", "빨강", "10억", "20톤")
weight = dump.getPayload()
print(weight)
