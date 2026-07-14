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
owner = input("Enter the name of the account owner: ")
number = input("Enter the account number: ")
balance = float(input("Enter the initial balance: "))

acc = Account(
owner, number, balance)
print("account Title: Addis Bank Account Management System")
print(f" Owner: {acc.owner}, Account: {acc.account_number}, Balance: {acc.balance}")    