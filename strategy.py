from abc import abstractmethod
from typing import Tuple

class Strategy:
    @abstractmethod
    def get_bet(self, round_id: int, balance: int, bets: Tuple[int],
                big_blind_index: int, community_cards: Tuple[Tuple[int]], hole_cards: Tuple[Tuple[int]], folded: Tuple[bool]):
        pass

    @abstractmethod
    def inform_result(self, round_id: int, balance: int, hole_cards: Tuple[Tuple[Tuple[int]]], community_cards: Tuple[Tuple[int]],
                      bets: Tuple[int]):
        pass

