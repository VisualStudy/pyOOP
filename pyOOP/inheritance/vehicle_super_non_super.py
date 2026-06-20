class Vehicle:
    def __init__(self, make, model, color, price):
        self.make = make
        self.model = model
        self.color = color
        self.price = price

    def setMake(self, make):
        self.make = make

    def getMake(self):
        return self.make

class Truck(Vehicle):
    def __init__(self, make, model, color, price, payload):
        super().__init(make, model, color, price)
        self.payload = payload

    def setPayload(self, payload):
        self.payload = payload

    def getPayload(self):
        return self.payload