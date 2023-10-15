from strategy import Strategy


class MyStrategy(Strategy):
    def __init__(self, player_id):
        super().__init__(player_id)

    def get_bet(self, round_id, balance, bets,
                big_blind_index, community_cards, hole_cards, folded):
        return balance - bets[self.player_id]

    def inform_result(self, round_id, balance, hole_cards, community_cards,
                      bets):
        pass