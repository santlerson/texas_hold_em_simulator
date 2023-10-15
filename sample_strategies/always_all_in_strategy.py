from strategy import Strategy

class MyStrategy(Strategy):
    def __init__(self, player_id):
        self.player_id = player_id

    def get_bet(self, round_id, balance, bets,
                small_blind_index, community_cards, hole_cards, folded):
        return balance - bets[self.player_id]

    def inform_result(self, round_id, balance, holes_cards, community_cards,
                      bets):
        pass
