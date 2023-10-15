from abc import abstractmethod
from typing import Tuple

class Strategy:
    @abstractmethod
    def get_bet(self, round_id: int, balance: int, bets: Tuple[int],
                small_blind_index: int, community_cards: Tuple[Tuple[int]], hole_cards: Tuple[Tuple[int]], folded: Tuple[bool]):
        """
        Place bet according to input parameters (and perhaps some internal state), note: function will still be
        called after you have folded in subsequent rounds of betting (so you can learn your opponents' behaviours),
        in such a case the return value will be ignored
        :param round_id: Number representing the round of the game (incremental)
        :param balance: Your current balance (meaning at the beginning of the round not including this round's bets)
        :param bets: Amounts each player currently has in the pot
        :param small_blind_index: Index of the player who is the small blind (big blind is small_blind_index + 1 (mod
        number of players)))
        :param community_cards: Cards on the table currently showing (each card represented by a tuple of (rank, suit))
        where rank is an integer from 2-14 (2-A) and suit is an integer from 0-3 (CHSD)
        :param hole_cards: Cards in your personal hand (each card represented by a tuple of (rank, suit)) where rank is
        an integer from 2-14 (2-A) and suit is an integer from 0-3 (CHSD)
        :param folded: Tuple of booleans representing whether each player has folded (True) or not (False)
        :return: Amount of money to add to the pot in this round of betting (in addition to the current bet)
        must be at least as much as to bring your total bet up to the current highest bet, or to make you go "all in"
        """
        pass

    @abstractmethod
    def inform_result(self, round_id: int, balance: int, holes_cards: Tuple[Tuple[Tuple[int]]], community_cards: Tuple[Tuple[int]],
                      bets: Tuple[int]):
        """
        Inform the strategy of the result of the round
        :param round_id: Number representing the round of the game (incremental)
        :param balance: Your current balance (at the end of the round including this round's bets and setting the pot)
        :param holes_cards: Cards in everyone's personal hands (each card represented by a tuple of (rank, suit)) where rank is
        an integer from 2-14 (2-A) and suit is an integer from 0-3 (CHSD)
        :param community_cards: Cards on the table currently showing (each card represented by a tuple of (rank, suit))
        where rank is an integer from 2-14 (2-A) and suit is an integer from 0-3 (CHSD)
        :param bets: Amounts each player has in the pot as of the end of the round
        :return: None
        """

        pass

