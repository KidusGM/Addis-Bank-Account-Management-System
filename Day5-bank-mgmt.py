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

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Must be positive")

        if self.balance - amount < -self.overdraft_limit:
            raise ValueError("Overdraft limit exceeded")

        self._change_balance(-amount)    

    def _change_balance(self, amount):
        self.__balance += amount

    def statment(self):
        print(
            f"Owner: {self.owner}, "
            f"Account: {self.account_number}, "
            f"Balance: {self.balance}"
        )


class saving_accounts(Account):
    def __init__(
        self,
        owner,
        number,
        balance=0,
        interest_rate=0.06
    ):
        super().__init__(owner, number, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Must be positive")

        if self.balance - amount < -self.overdraft_limit:
            raise ValueError("Overdraft limit exceeded")

        self._change_balance(-amount)     

    def statment(self):
        print(
            f"Owner: {self.owner}, "
            f"Account: {self.account_number}, "
            f"Balance: {self.balance}, "
            f"Interest_Rate: {self.interest_rate}"
        )


class current_aacounts(Account):
    def __init__(
        self,
        owner,
        number,
        balance=0,
        overdraft_limit=1000
    ):
        super().__init__(owner, number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Must be positive")

        if self.balance - amount < -self.overdraft_limit:
            raise ValueError("Overdraft limit exceeded")

        self._change_balance(-amount) 

    def statment(self):
        print(
            f"Owner: {self.owner}, "
            f"Account: {self.account_number}, "
            f"Balance: {self.balance}, "
            f"Overdraft_Limit: {self.overdraft_limit}"
        )


account = []

number_of_accounts = int(
    input("Enter the number of accounts to create: ")
)

for i in range(number_of_accounts):

    owner = input(
        f"Enter the name of the account owner "
        f"for account {i + 1}: "
    )

    number = input(
        f"Enter the account number "
        f"for account {i + 1}: "
    )

    balance = float(
        input(
            f"Enter the initial balance "
            f"for account {i + 1}: "
        )
    )

    account_type = input(
        "Enter account type (normal/savings/current): "
    ).lower()

    if account_type == "savings":

        acc = saving_accounts(
            owner,
            number,
            balance
        )

    elif account_type == "current":

        acc = current_aacounts(
            owner,
            number,
            balance
        )

    else:

        acc = Account(
            owner,
            number,
            balance
        )

    account.append(acc)


for acc in account:
    acc.statment()

    action = input(
        f"\nWhat do you want to do with {acc.owner}'s account? "
        "(deposit/withdraw/none): "
    ).lower()

    if action == "deposit":

        amount = float(input("Enter deposit amount: "))
        acc.deposit(amount)

        print("Deposit successful!")

    elif action == "withdraw":

        if isinstance(acc, current_aacounts):

            amount = float(input("Enter withdrawal amount: "))
            acc.withdraw(amount)

            print("Withdrawal successful!")

        else:

            print("This account type does not support withdrawal.")

    print("\nUpdated Account:")
    acc.statment()
print("\nAll Accounts")
print("-" * 40)

for acc in account:
    acc.statment()