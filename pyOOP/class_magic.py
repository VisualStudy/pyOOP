class Plant:
    def __init__(self, name = "식물이", height = 0):
        self.name = name
        self.height = height

    def __str__(self):
        return "나는 식물!"

    def growth(self, rain):
        if rain == True:
            self.height += 1
            print(f"키가 자라서 {self.height}가 되었다!")

p1 = Plant("다육이", 10)

print(p1.name)