from strategy import Strategy

class MyStrategy(Strategy):
    def __init__(self, player_id, blind_period, initial_big_blind, initial_small_blind, blind_base):
        self.setup(player_id, blind_period, initial_big_blind, initial_small_blind, blind_base)

    def get_bet(self, round_id, balances, bets,
                small_blind_index, big_blind_index,
                players_in_game, community_cards,
                hole_cards, folded):
        return balances[self.player_id]

    def inform_result(self, round_id: int, balances,
                      holes_cards,
                      community_cards,
                      bets):
        pass
