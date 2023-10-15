from strategy import Strategy

class MyStrategy(Strategy):
    def __init__(self, player_id):
        self.player_id = player_id

    def get_bet(self, round_id, balance, bets,
                big_blind_index, community_cards, hole_cards, folded):
        (rank1, _), (rank2, _) = hole_cards
        if rank1 == rank2== 14:
            return balance - bets[self.player_id]
        else:
            return 0

    def inform_result(self, round_id, balance, hole_cards, community_cards,
                      bets):
        pass