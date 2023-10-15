from strategy import Strategy

class Player:
    def __init__(self, strategy, balance):
        self.strategy = strategy
        self.balance = balance


    def get_strategy(self):
        return self.strategy

    def get_balance(self):
        return self.balance

    def decrement_balance(self, amount):
        self.balance -= amount

    def increment_balance(self, amount):
        self.balance += amount


