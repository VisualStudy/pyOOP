class Secret:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def name_get(self):
        return self.__name

    def name_set(self, name):
        self.__name = name

    def age_get(self):
        return self.__age

    def age_set(self, age):
        self.__age = age

a1 = Secret("byum", 21)

print(a1.age_get())
# private 접근 불가: print(a1.__age)