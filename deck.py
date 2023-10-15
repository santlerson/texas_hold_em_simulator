from card import Card
import random


class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for rank in range(2, 15) for suit in range(4)]
        random.shuffle(self.cards)

    def draw(self, n=1):
        return [self.cards.pop() for _ in range(n)]