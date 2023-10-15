class Community:
    def __init__(self, cards):
        self.cards = tuple(cards)
        self.stage = 0

    @staticmethod
    def from_deck(deck):
        return Community(deck.draw(5))

    def advance_stage(self):
        self.stage += 1

    def get_cards(self):
        if self.stage==0:
            return tuple()
        else:
            return self.cards[:3+self.stage-1]

    def get_card_tuples(self):
        return [card.get_tuple() for card in self.get_cards()]

