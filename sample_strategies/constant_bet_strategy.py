from strategy import Strategy

BET = 5
class MyStrategy(Strategy):
    def __init__(self, player_id):
        self.player_id = player_id

    def get_bet(self, round_id, balance, bets,
                big_blind_index, community_cards, hole_cards, folded):
        return BET

    def inform_result(self, round_id, balance, hole_cards, community_cards,
                      bets):
        pass