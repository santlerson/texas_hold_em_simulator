from strategy import Strategy

class MyStrategy(Strategy):
    def __init__(self, player_id):
        self.player_id = player_id

    def get_bet(self, round_id, balances, bets,
                small_blind_index, big_blind_index,
                players_in_game, community_cards,
                hole_cards, folded):
        (rank1, _), (rank2, _) = hole_cards
        if rank1 == rank2:
            return balances[self.player_id]
        else:
            return 0

    def inform_result(self, round_id: int, balances,
                      holes_cards,
                      community_cards,
                      bets):
        pass