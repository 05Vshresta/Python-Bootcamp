class Bank:
    def __init__(self):
        self.__balance = 10000  #private variable

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited Amount : {amount}.")
        else:
            print(f"Invalid deposit amount. Please enter a positive value.")

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            print("Insufficient funds.")
    def display_balance(self):
        print(f"Current balance: {self.__balance}")
            
Account = Bank()
Account.deposit(5000)
Account.withdraw(2000)
Account.display_balance()