from round import Round, GameParameters
import strategy
import strategy_wrapper
from typing import Tuple, List
from player import Player
import os

STRATEGIES_DIR = "sample_strategies"


class Game:
    def __init__(self, game_parameters, strategies: Tuple[strategy.Strategy], logger=None):
        self.round_id = 0
        self.players: Tuple[Player] = tuple(
            [Player(strategy, game_parameters.starting_balance) for strategy in strategies])
        self.game_parameters = game_parameters
        self.logger = logger
        if self.logger:
            self.logger.log_game_params(game_parameters)

    def play(self):
        # bar = tqdm()
        sb_index = 0
        bb_index = 1
        while len([i for i in range(len(self.players)) if self.players[i].get_balance() > 0]) > 1:
            while self.players[sb_index].get_balance() <= 0:
                sb_index = (sb_index + 1) % len(self.players)
            bb_index = (sb_index + 1) % len(self.players)
            while self.players[bb_index].get_balance() <= 0:
                bb_index = (bb_index + 1) % len(self.players)
            round = Round(self.round_id, self.players, self.game_parameters, sb_index, bb_index, self.logger)
            round.play()
            self.round_id += 1
            sb_index = (sb_index + 1) % len(self.players)
            # bar.update(1)
            print([player.get_balance() for player in self.players], flush=True)

        return [i for i, player in enumerate(self.players) if player.get_balance() > 0][0]
