# =========================
# 1. SINGLETON
# =========================

class BankConfig:
    """
    Singleton class.

    Only one BankConfig object will exist
    throughout the entire program.
    """

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

            # Shared bank-wide settings
            cls._instance.interest_rate = 0.06
            cls._instance.overdraft_limit = 1000

        return cls._instance


# =========================
# 2. OBSERVER CLASSES
# =========================

class SMSAlert:
    """
    Observer.

    Receives notifications when
    an account changes.
    """

    def update(self, event):

        print(
            f"[SMS ALERT] {event}"
        )


class AuditLog:
    """
    Observer.

    Records account events.
    """

    def update(self, event):

        print(
            f"[AUDIT LOG] {event}"
        )


# =========================
# 3. BASE ACCOUNT CLASS
# =========================

class Account:
    """
    Base Account class.

    Responsibility:
    - Store account information
    - Manage balance
    - Deposit money
    - Withdraw money
    - Notify observers
    """

    def __init__(
        self,
        owner,
        number,
        balance=0
    ):

        self.owner = owner
        self.account_number = number

        # Private balance
        self.__balance = balance

        # List of observers
        self._observers = []

    # -------------------------
    # PROPERTY
    # -------------------------

    @property
    def balance(self):

        return self.__balance

    # -------------------------
    # DEPOSIT
    # -------------------------

    def deposit(self, amount):

        if amount <= 0:

            raise ValueError(
                "Amount must be positive."
            )

        self._change_balance(amount)

        self._notify(
            f"{self.owner} deposited "
            f"{amount} ETB."
        )

    # -------------------------
    # WITHDRAW
    # -------------------------

    def withdraw(self, amount):

        if amount <= 0:

            raise ValueError(
                "Amount must be positive."
            )

        if amount > self.balance:

            raise ValueError(
                "Insufficient funds."
            )

        self._change_balance(-amount)

        self._notify(
            f"{self.owner} withdrew "
            f"{amount} ETB."
        )

    # -------------------------
    # INTERNAL BALANCE CHANGE
    # -------------------------

    def _change_balance(self, amount):

        self.__balance += amount

    # -------------------------
    # OBSERVER: SUBSCRIBE
    # -------------------------

    def subscribe(self, observer):

        self._observers.append(observer)

    # -------------------------
    # OBSERVER: NOTIFY
    # -------------------------

    def _notify(self, event):

        for observer in self._observers:

            observer.update(event)


# =========================
# 4. SAVINGS ACCOUNT
# =========================

class SavingsAccount(Account):
    """
    SavingsAccount inherits from Account.

    It adds interest functionality.
    """

    def __init__(
        self,
        owner,
        number,
        balance=0
    ):

        super().__init__(
            owner,
            number,
            balance
        )

        # Get shared configuration
        config = BankConfig()

        self.interest_rate = (
            config.interest_rate
        )

    def apply_interest(self):

        interest = (
            self.balance *
            self.interest_rate
        )

        self.deposit(interest)

        print(
            f"Interest applied: "
            f"{interest:.2f} ETB"
        )


# =========================
# 5. CURRENT ACCOUNT
# =========================

class CurrentAccount(Account):
    """
    CurrentAccount inherits from Account.

    It allows overdrafts.
    """

    def __init__(
        self,
        owner,
        number,
        balance=0
    ):

        super().__init__(
            owner,
            number,
            balance
        )

        # Get shared configuration
        config = BankConfig()

        self.overdraft_limit = (
            config.overdraft_limit
        )

    def withdraw(self, amount):

        if amount <= 0:

            raise ValueError(
                "Amount must be positive."
            )

        # Example:
        #
        # balance = 500
        # overdraft_limit = 1000
        #
        # The account can go down to -1000.
        #
        # -1000 is allowed.
        # -1001 is not allowed.

        if (
            self.balance - amount
            < -self.overdraft_limit
        ):

            raise ValueError(
                "Overdraft limit exceeded."
            )

        self._change_balance(-amount)

        self._notify(
            f"{self.owner} withdrew "
            f"{amount} ETB."
        )


# =========================
# 6. ACCOUNT FACTORY
# =========================

class AccountFactory:
    """
    Factory Pattern.

    Creates the correct account object
    based on the account type.
    """

    _account_types = {

        "normal": Account,

        "savings": SavingsAccount,

        "current": CurrentAccount

    }

    @classmethod
    def create(
        cls,
        account_type,
        owner,
        number,
        balance=0
    ):

        account_class = (
            cls._account_types.get(
                account_type
            )
        )

        if account_class is None:

            raise ValueError(
                f"Unknown account type: "
                f"{account_type}"
            )

        return account_class(
            owner,
            number,
            balance
        )


# =========================
# 7. STATEMENT SERVICE
# =========================

class StatementService:
    """
    Responsible only for printing
    account information.

    This follows SRP.
    """

    @staticmethod
    def print_statement(account):

        print()
        print(
            f"Owner: "
            f"{account.owner}"
        )

        print(
            f"Account Number: "
            f"{account.account_number}"
        )

        print(
            f"Balance: "
            f"{account.balance:.2f} ETB"
        )

        if isinstance(
            account,
            SavingsAccount
        ):

            print(
                f"Interest Rate: "
                f"{account.interest_rate * 100}%"
            )

        elif isinstance(
            account,
            CurrentAccount
        ):

            print(
                f"Overdraft Limit: "
                f"{account.overdraft_limit} ETB"
            )


# =========================
# 8. CREATE ACCOUNTS
# =========================

accounts = []

number_of_accounts = int(
    input(
        "Enter the number of accounts "
        "to create: "
    )
)


for i in range(
    number_of_accounts
):

    print()
    print(
        f"Creating Account "
        f"{i + 1}"
    )

    print(
        "-" * 30
    )

    owner = input(
        "Enter account owner name: "
    )

    number = input(
        "Enter account number: "
    )

    balance = float(
        input(
            "Enter initial balance: "
        )
    )

    account_type = input(
        "Enter account type "
        "(normal/savings/current): "
    ).lower()

    try:

        # Factory creates the correct object
        account = AccountFactory.create(
            account_type,
            owner,
            number,
            balance
        )

        # Add observers
        account.subscribe(
            SMSAlert()
        )

        account.subscribe(
            AuditLog()
        )

        # Store account
        accounts.append(account)

        print(
            "Account created successfully!"
        )

    except ValueError as error:

        print(
            f"Error: {error}"
        )


# =========================
# 9. ACCOUNT OPERATIONS
# =========================

for account in accounts:

    print()
    print("=" * 40)

    print(
        "CURRENT ACCOUNT INFORMATION"
    )

    print("=" * 40)

    StatementService.print_statement(
        account
    )

    print()

    action = input(
        f"What do you want to do with "
        f"{account.owner}'s account? "
        "(deposit/withdraw/interest/none): "
    ).lower()

    try:

        # -------------------------
        # DEPOSIT
        # -------------------------

        if action == "deposit":

            amount = float(
                input(
                    "Enter deposit amount: "
                )
            )

            account.deposit(
                amount
            )

            print(
                "Deposit successful!"
            )

        # -------------------------
        # WITHDRAW
        # -------------------------

        elif action == "withdraw":

            amount = float(
                input(
                    "Enter withdrawal amount: "
                )
            )

            # We no longer need:
            #
            # if isinstance(account, CurrentAccount)
            #
            # Every account has withdraw().
            # Each account handles its own rules.

            account.withdraw(
                amount
            )

            print(
                "Withdrawal successful!"
            )

        # -------------------------
        # APPLY INTEREST
        # -------------------------

        elif action == "interest":

            if isinstance(
                account,
                SavingsAccount
            ):

                account.apply_interest()

            else:

                print(
                    "Only savings accounts "
                    "earn interest."
                )

        # -------------------------
        # NO ACTION
        # -------------------------

        elif action == "none":

            print(
                "No action performed."
            )

        else:

            print(
                "Invalid action."
            )

    except ValueError as error:

        print(
            f"Error: {error}"
        )

    print()

    print(
        "UPDATED ACCOUNT"
    )

    print(
        "-" * 40
    )

    StatementService.print_statement(
        account
    )


# =========================
# 10. DISPLAY ALL ACCOUNTS
# =========================

print()
print()
print(
    "ALL ACCOUNTS"
)

print(
    "-" * 40
)


for account in accounts:

    StatementService.print_statement(
        account
    )

    print(
        "-" * 40
    )