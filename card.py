(CLUB, HEART, SPADE, DIAMOND) = range(4)
SYMBOLS = {
    CLUB: '♣',
    HEART: '♥',
    SPADE: '♠',
    DIAMOND: '♦',
}

(J,Q,K) = (11,12,13)

A = 14

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f'{self.rank}{SYMBOLS[self.suit]}'

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __lt__(self, other):
        return self.rank < other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __ge__(self, other):
        return self.rank >= other.rank

    def rank_equals(self, other: 'Card'):
        return self.rank == other.rank

    def suit_equals(self, other: 'Card'):
        return self.suit == other.suit

    def is_predecessor_of(self, other: 'Card'):
        return self.rank + 1 == other.rank or self.rank == A and other.rank == 2

    def get_tuple(self):
        return self.rank, self.suit

