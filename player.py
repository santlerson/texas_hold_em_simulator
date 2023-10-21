from strategy import Strategy

class Player:
    def __init__(self, strategy: Strategy, balance: int):
        self.strategy: Strategy = strategy
        self.balance: int = balance


    def get_strategy(self)->Strategy:
        return self.strategy

    def get_balance(self)->int:
        return self.balance

    def decrement_balance(self, amount):
        self.balance -= amount

    def increment_balance(self, amount):
        self.balance += amount


