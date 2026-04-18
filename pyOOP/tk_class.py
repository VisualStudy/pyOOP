class World:
    def __init__(self, people, country):
        self.popular = people
        self.nation = country

    def announce(self):
        print(f"우리 세계의 인구 수는 {self.popular}명입니다.")
        print(f"우리 나라의 이름은 {self.nation}입니다.")

earth = World(10000000, "보헤미아")

earth.announce()