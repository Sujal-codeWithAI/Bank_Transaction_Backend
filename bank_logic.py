
class Account:
    def __init__(self, pin, balance=1000):
        self._pin = pin
        self._balance = balance

    def check_pin(self, input_pin):
        return self._pin == input_pin

    def deposit(self, amount):
        if amount <= 0:
            return False, "Cannot deposit zero or negative amount."
        self._balance += amount
        return True, f"Deposited {amount}. New balance: {self._balance}"

    def withdraw(self, amount):
        if amount <= 0:
            return False, "Cannot withdraw zero or negative amount."
        if amount > self._balance:
            return False, "Insufficient balance."
        self._balance -= amount
        return True, f"Withdrew {amount}. New balance: {self._balance}"

    def get_balance(self):
        return self._balance
