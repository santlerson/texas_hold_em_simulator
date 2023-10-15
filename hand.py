from typing import List
from functools import cache
from card import Card, A, J, Q, K

HAND_TYPE_COUNT = 9
HAND_TYPES = range(HAND_TYPE_COUNT)
(STRAIGHT_FLUSH, FOUR_OF_A_KIND, FULL_HOUSE, FLUSH, STRAIGHT, THREE_OF_A_KIND, TWO_PAIR, ONE_PAIR, HIGH_CARD) = HAND_TYPES

class Hand:
    def __init__(self, cards: List[Card]):
        self.cards = tuple(sorted(cards))
        self.reverse_cards = tuple(reversed(self.cards))

    def __repr__(self):
        return f'Hand({self.cards})'

    @cache
    def get_of_a_kinds(self, include_ones=False) -> dict:
        of_a_kinds = {}
        for card in self.cards:
            of_a_kinds[card.rank] = of_a_kinds.get(card.rank, 0) + 1
        for rank, count in list(of_a_kinds.items()):
            if count == 1 and not include_ones:
                del of_a_kinds[rank]
        return of_a_kinds

    @cache
    def get_sorted_of_a_kind_ranks(self):
        return tuple(sorted(self.get_of_a_kinds(include_ones=True).keys(), reverse=True,
                            key=lambda rank: (self.get_of_a_kinds(include_ones=True)[rank], rank)))

    @cache
    def is_pair(self) -> bool:
        return 2 in self.get_of_a_kinds().values()

    @cache
    def is_two_pair(self) -> bool:
        return 2 in self.get_of_a_kinds().values() and len(self.get_of_a_kinds()) == 2

    @cache
    def is_three_of_a_kind(self) -> bool:
        return 3 in self.get_of_a_kinds().values()

    @cache
    def is_straight(self) -> bool:
        return all(self.cards[i].is_predecessor_of(self.cards[i+1]) for i in range(len(self.cards)-1)) or \
                  self.cards[-1].rank == A and self.cards[0].rank == 2 and all(self.cards[i].is_predecessor_of(
                                                                                self.cards[i+1])
                                                                               for i in range(len(self.cards)-2))

    @cache
    def is_flush(self) -> bool:
        return all(self.cards[i].suit_equals(self.cards[i+1]) for i in range(len(self.cards)-1))

    @cache
    def is_full_house(self) -> bool:
        return 2 in self.get_of_a_kinds().values() and 3 in self.get_of_a_kinds().values()

    @cache
    def is_four_of_a_kind(self) -> bool:
        return 4 in self.get_of_a_kinds().values()

    @cache
    def is_straight_flush(self) -> bool:
        return self.is_straight() and self.is_flush()

    hand_type_functions = [is_straight_flush, is_four_of_a_kind, is_full_house, is_flush, is_straight,
                           is_three_of_a_kind, is_two_pair, is_pair, lambda self: True]

    @cache
    def get_hand_type(self) -> int:
        for hand_type in HAND_TYPES:
            if self.hand_type_functions[hand_type](self):
                return hand_type
        raise Exception('No hand type found')


    def __lt__(self, other):
        if (self.get_hand_type()) != (other.get_hand_type()):
            return (self.get_hand_type()) > (other.get_hand_type())
        elif self.get_hand_type() in {STRAIGHT_FLUSH, STRAIGHT, FLUSH, HIGH_CARD}:
            return self.reverse_cards < other.reverse_cards
        elif self.get_hand_type() in {FOUR_OF_A_KIND, FULL_HOUSE, THREE_OF_A_KIND, ONE_PAIR, TWO_PAIR}:
            return self.get_sorted_of_a_kind_ranks() < other.get_sorted_of_a_kind_ranks()
        raise Exception('No hand type found')


    def __gt__(self, other):
        return other < self

    def __le__(self, other):
        return not other < self

    def __ge__(self, other):
        return not self < other

    def is_equivalent(self, other):
        return (not self < other) and (not other < self)

    def __hash__(self):
        return hash(self.cards)











