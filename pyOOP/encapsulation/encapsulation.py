class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"{amount}원 입금 완료")
        else:
            print("입금액은 0보다 커야 합니다.")

    def withdraw(self, amount):
        if amount <= 0:
            print("출금액은 0보다 커야 합니다.")
        elif amount > self.__balance:
            print("잔액이 부족합니다.")
        else:
            self.__balance -= amount
            print(f"{amount}원 출금 완료")

    def get_balance(self):
        return self.__balance

account = BankAccount("지은", 10000)

account.deposit(5000)
account.withdraw(3000)

print(account.get_balance())