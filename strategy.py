from abc import abstractmethod
from typing import Tuple, Union


class Strategy:
    @abstractmethod
    def get_bet(self, round_id: int, balances: Tuple[int], bets: Tuple[int],
                small_blind_index: int, big_blind_index: int,
                players_in_game: Tuple[bool], community_cards: Tuple[Tuple[int]],
                hole_cards: Tuple[Tuple[int]], folded: Tuple[bool]):
        """
        Place bet according to input parameters (and perhaps some internal state), note: function will still be
        called after you have folded in subsequent rounds of betting (so you can learn your opponents' behaviours),
        in such a case the return value will be ignored
        :param round_id: Number representing the round of the game (incremental)
        :param balances: All players current balances after all bets during this round are subtracted.
        This is the maximal amount any player can bet on their next turn.
        :param bets: Amounts each player currently has in the pot
        :param small_blind_index: Index of the player who is the small blind for this round
        :param big_blind_index: Index of the player who is the big blind for this round
        :param players_in_game: Tuple of booleans representing whether each player is still in the game (True) or not
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
    def inform_result(self, round_id: int, balances: Tuple[int],
                      holes_cards: Union[Tuple[Union[Tuple[Tuple[int]], None]], None],
                      community_cards: Tuple[Tuple[int]],
                      bets: Tuple[int]):
        """
        Inform the strategy of the result of the round
        :param round_id: Number representing the round of the game (incremental)
        :param balances: All players current balances after all bets during this round are subtracted and winnings are
        added
        :param holes_cards: Cards in everyone's personal hands (each card represented by a tuple of (rank, suit)) where rank is
        an integer from 2-14 (2-A) and suit is an integer from 0-3 (CHSD). Folded players or players who are not
        in the game will have None in their place. In the event that a round ends with no showdown (all but one player
        folds) this will be None
        :param community_cards: Cards on the table currently showing (each card represented by a tuple of (rank, suit))
        where rank is an integer from 2-14 (2-A) and suit is an integer from 0-3 (CHSD)
        :param bets: Amounts each player has in the pot as of the end of the round
        :return: None
        """

        pass

