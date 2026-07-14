class Account:
    def __init__(self, owner, number, balance=0):
        self.owner = owner
        self.account_number = number
        self.__balance = balance

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Must be positive")
        self.__balance += amount

acc = Account(
"Almaz", "CBE-1001", 1500)
acc.deposit(500)
print(f" Owner: {acc.owner}, Account: {acc.account_number}, Balance: {acc.balance}")    