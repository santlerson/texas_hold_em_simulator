from deck import Deck
from typing import Tuple, List
from community import Community
from hole import Hole
from player import Player
from strategy import Strategy
import concurrent.futures
from logger import Logger

TIMEOUT = 1


class GameParameters:
    def __init__(self, starting_balance=1000,
                 blind_period=10, initial_big_blind=20, initial_small_blind=10, blind_base=1.2,
                 ):
        self.starting_balance = starting_balance
        self.blind_period = blind_period
        self.initial_big_blind = initial_big_blind
        self.initial_small_blind = initial_small_blind
        self.blind_base = blind_base
        self.big_blind = lambda round_number: int(initial_big_blind * (blind_base ** (round_number // blind_period)))
        self.small_blind = lambda round_number: int(initial_small_blind * (blind_base ** (round_number // blind_period)))

    def get_big_blind(self, round_number):
        return self.big_blind(round_number)

    def get_small_blind(self, round_number):
        return self.small_blind(round_number)

    def get_blind_parameters(self):
        return self.blind_period, self.initial_big_blind, self.initial_small_blind, self.blind_base

STAGES = range(4)
(PREFLOP, FLOP, TURN, RIVER) = STAGES


class Round:
    def __init__(self, round_id, players: Tuple[Player], game_parameters: GameParameters, small_blind_index,
                 big_blind_index, logger: "Logger" = None):
        self.big_blind_index = big_blind_index
        self.small_blind_index = small_blind_index
        self.bets: List[int] = [0 for _ in players]
        self.round = round_id
        self.game_parameters = game_parameters
        self.deck = Deck()
        self.community = Community.from_deck(self.deck)
        self.players: Tuple[Player] = players
        self.in_game = [player.get_balance() > 0 for player in players]
        self.holes: List[Hole] = [Hole(self.deck.draw(2)) for i, _ in enumerate(players) ]
        self.bets[self.big_blind_index] = min(game_parameters.get_big_blind(round_id),
                                              players[self.big_blind_index].get_balance())
        self.bets[self.small_blind_index] = min(game_parameters.get_small_blind(round_id),
                                                players[self.small_blind_index].get_balance())
        self.stage = PREFLOP
        self.folded = [False for _ in players]
        self.logger: Logger = logger
        if logger:
            logger.create_new_round(self.big_blind_index, self.small_blind_index)
            logger.log_blinds(self.bets[self.big_blind_index], self.bets[self.small_blind_index])

    def play(self):
        cards_tuple = self.community.get_card_tuples()
        if self.logger:
            self.logger.log_holes_cards([hole.get_cards_tuples() if self.in_game[i] else None for i, hole in
                                         enumerate(self.holes)])

        while self.stage < len(STAGES) and len([i for i in range(len(self.players)) if (not self.folded[i]) and
                                                                                       self.players[
                                                                                           i].get_balance() > 0]) > 1:
            has_had_chance_to_bet = [False for _ in self.players]
            cards_tuple = self.community.get_card_tuples()
            i = self.small_blind_index if self.stage != PREFLOP else (self.big_blind_index + 1) % len(self.players)
            betting_done = False
            while any([((not self.folded[j]) and
                        (self.bets[j] < min(max(self.bets), self.players[j].get_balance()))) or
                       (not has_had_chance_to_bet[j])
                       for j in range(len(self.players))]) and len([j for j in range(len(self.players)) if
                                                                      (not self.folded[j])
                                                                    and (self.bets[j] or
                                                                         self.players[j].get_balance())]) > 1:
                betting_done = True
                has_had_chance_to_bet[i] = True
                player: Player = self.players[i]
                if self.in_game[i]:
                    # player.get_strategy().get_bet(self.round,
                    #                               tuple([p.get_balance()-self.bets[i]
                    #                                      for p in self.players]),
                    #                               tuple(self.bets),
                    #                                 self.small_blind_index,
                    #                               self.big_blind_index,
                    #                               tuple(self.in_game),
                    #                               self.community.get_card_tuples(),
                    #                                 self.holes[i].get_cards_tuples(),
                    #                                 tuple(self.folded))
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(player.get_strategy().get_bet,
                                                 self.round,
                                                 tuple([p.get_balance() - self.bets[i]
                                                        for p in self.players]),
                                                 tuple(self.bets),
                                                 self.small_blind_index,
                                                 self.big_blind_index,
                                                 tuple(self.in_game),
                                                 self.community.get_card_tuples(),
                                                 self.holes[i].get_cards_tuples(),
                                                 tuple(self.folded))
                        try:
                            bet = future.result(timeout=TIMEOUT)
                        except concurrent.futures.TimeoutError:
                            bet = -1  # fold
                            print("Player {} timed out".format(i))
                        except Exception as e:
                            print("Player {} raised an exception: {}".format(i, e))
                            bet = -1  # fold

                    minimum_bet = min(max(self.bets) - self.bets[i], player.get_balance() - self.bets[i])
                    if not isinstance(bet, int) or bet < minimum_bet or bet + self.bets[i] > player.get_balance() or \
                            self.folded[i]:
                        if self.logger and not self.folded[i]:
                            self.logger.log_fold(i)
                        self.folded[i] = True

                    else:
                        self.bets[i] += bet
                        if self.logger:
                            self.logger.log_bet(i, bet, self.bets[i])
                i = (i + 1) % len(self.players)
            self.stage += 1
            self.community.advance_stage()
            if self.logger:
                self.logger.advance_stage()

        hands = [hole.best_hand(self.community.get_cards()) for hole in self.holes]
        # argsorted_hands = sorted(range(len(hands)), key=lambda x: hands[x], reverse=True)
        player_payouts = [0 for _ in self.players]
        for i, (player, bet) in enumerate(zip(self.players, self.bets)):
            player.decrement_balance(bet)
            player_payouts[i] -= bet
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
                if hands[sorted_potential_access[i]].is_equivalent(hands[sorted_potential_access[i + 1]]):
                    winner_count += 1
                else:
                    break
            for i in sorted_potential_access[:winner_count]:
                self.players[i].increment_balance((payout * count) // winner_count)  # may annihilate some money
                player_payouts[i] += (payout * count) // winner_count
        hole_cards = [hole.get_cards_tuples() for hole in self.holes]
        if self.logger:
            self.logger.log_community_cards(self.community.get_card_tuples())
        for i, folded in enumerate(self.folded):
            if folded:
                hole_cards[i] = None
        if self.logger:
            self.logger.log_results(player_payouts, [player.get_balance() for player in self.players])
        with concurrent.futures.ThreadPoolExecutor() as executor:
            l = []
            for player in self.players:
                strategy: Strategy = player.get_strategy()
                # strategy.inform_result(self.round, player.get_balance(), tuple(hole_cards), self.community.get_card_tuples(),
                #                        tuple(self.bets))
                l.append(executor.submit(strategy.inform_result, self.round, player.get_balance(), tuple(hole_cards),
                                         self.community.get_card_tuples(),
                                         tuple(self.bets)))
            for future in concurrent.futures.as_completed(l):
                try:
                    future.result(timeout=TIMEOUT)
                except concurrent.futures.TimeoutError:
                    print("Timeout")
                except Exception as e:
                    print(e)
