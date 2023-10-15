from itertools import combinations
from hand import Hand

class Hole:
    def __init__(self, cards):
        self.cards = tuple(cards)

    def best_hand(self, river):
        combs = combinations(self.cards + river, 5)
        hands = [Hand(comb) for comb in combs]
        return max(hands)
    
    def get_cards_tuples(self):
        return [card.get_tuple() for card in self.cards]



