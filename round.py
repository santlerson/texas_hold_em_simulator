from deck import Deck
from typing import Tuple, List
from community import Community
from hole import Hole
from player import Player
from strategy import Strategy


class GameParameters:
    def __init__(self, starting_balance=1000, big_blind=lambda round_number: 10, small_blind=lambda round_number: 5):
        self.starting_balance = starting_balance
        self.big_blind = big_blind
        self.small_blind = small_blind

    def get_big_blind(self, round_number):
        return self.big_blind(round_number)

    def get_small_blind(self, round_number):
        return self.small_blind(round_number)

STAGES = range(4)
(PREFLOP, FLOP, TURN, RIVER) = STAGES
class Round:
    def __init__(self, round_id, players: Tuple[Player], game_parameters: GameParameters, small_blind_index, big_blind_index):
        self.big_blind_index = big_blind_index
        self.small_blind_index = small_blind_index
        self.bets = [0 for _ in players]
        self.round = round_id
        self.game_parameters = game_parameters
        self.deck = Deck()
        self.holes: List[Hole] = [Hole(self.deck.draw(2)) for _ in players]
        self.community = Community.from_deck(self.deck)
        self.players: Tuple[Player] = players
        self.bets[self.big_blind_index] = min(game_parameters.get_big_blind(round_id), players[self.big_blind_index].get_balance())
        self.bets[self.small_blind_index] = min(game_parameters.get_small_blind(round_id), players[self.small_blind_index].get_balance())
        self.stage = PREFLOP
        self.folded = [False for _ in players]


    def play(self):
        cards_tuple = self.community.get_card_tuples()
        while self.stage < len(STAGES) and len([i for i in range(len(self.players)) if not self.folded[i]]) > 1:
            cards_tuple = self.community.get_card_tuples()
            i = self.small_blind_index
            betting_done = False
            while any([(not self.folded[j]) and
                       (self.bets[j] < min(max(self.bets),self.players[j].get_balance()))
                       for j in range(len(self.players))]) or i != self.small_blind_index or not betting_done:
                betting_done = True
                player = self.players[i]
                bet = player.get_strategy().get_bet(self.round, self.game_parameters.starting_balance, tuple(self.bets),
                                     self.big_blind_index, cards_tuple, self.holes[i].get_cards_tuples(), tuple(self.folded))
                minimum_bet = min(max(self.bets) - self.bets[i], player.get_balance()-self.bets[i])
                if not isinstance(bet, int) or bet < minimum_bet or bet + self.bets[i] > player.get_balance() or\
                        self.folded[i]:
                    self.folded[i] = True
                else:
                    self.bets[i] += bet
                i = (i + 1) % len(self.players)
            self.stage += 1
            self.community.advance_stage()
        hands = [hole.best_hand(self.community.get_cards()) for hole in self.holes]
        # argsorted_hands = sorted(range(len(hands)), key=lambda x: hands[x], reverse=True)
        for player, bet in zip(self.players, self.bets):
            player.decrement_balance(bet)
        # copy_bets = self.bets.copy()
        unique_betting_values_buckets = sorted([(bet, len([j for j in range(len(self.bets)) if self.bets[j] >= bet]))
                                         for bet in set(self.bets)])
        unique_betting_values = [bet for bet, _ in unique_betting_values_buckets]
        payouts = [bet - previous_bet for bet, previous_bet in
                   zip(unique_betting_values, [0] + unique_betting_values[:-1])]
        for j, (payout, (betting_value, count)) in enumerate(zip(payouts, unique_betting_values_buckets)):
            potential_access = [i for i, bet in enumerate(self.bets) if bet >= betting_value and not self.folded[i]]
            sorted_potential_access = sorted(potential_access, key=lambda x: hands[x], reverse=True)
            winner_count = 1
            for i, _ in enumerate(sorted_potential_access[:-1]):
                if hands[sorted_potential_access[i]].is_equivalent(hands[sorted_potential_access[i+1]]):
                    winner_count += 1
                else:
                    break
            for i in sorted_potential_access[:winner_count]:
                self.players[i].increment_balance((payout*count)//winner_count)  # may annihilate some money
        hole_cards = [hole.get_cards_tuples() for hole in self.holes]
        for i, folded in enumerate(self.folded):
            if folded:
                hole_cards[i] = None

        for player in self.players:
            strategy: Strategy = player.get_strategy()
            strategy.inform_result(self.round, player.get_balance(), tuple(hole_cards), self.community.get_card_tuples(),
                                   tuple(self.bets))








