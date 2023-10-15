from round import Round, GameParameters
from strategy import Strategy
from typing import Tuple, List
from player import Player
import os



class Game:
    def __init__(self, game_parameters, strategies: Tuple[Strategy]):
        self.round_id = 0
        self.players: Tuple[Player] = tuple(
            [Player(strategy, game_parameters.starting_balance) for strategy in strategies])
        self.game_parameters = game_parameters

    def play(self):
        # bar = tqdm()
        sb_index = 0
        bb_index = 1
        while len([i for i in range(len(self.players)) if self.players[i].get_balance() > 0]) > 1:
            while self.players[sb_index].get_balance() <= 0:
                sb_index = (sb_index + 1) % len(self.players)
            bb_index = (sb_index + 1) % len(self.players)
            round = Round(self.round_id, self.players, self.game_parameters, sb_index, bb_index)
            round.play()
            self.round_id += 1
            sb_index = (sb_index + 1) % len(self.players)
            # bar.update(1)
            print([player.get_balance() for player in self.players], flush=True)


        return [i for i, player in enumerate(self.players) if player.get_balance() > 0][0]

def main():
    #foreach python file in sample_strategies, import class and add to strategies
    strategy_files = os.listdir("sample_strategies")
    strategy_classes = []
    strategies: List[Strategy] = []
    strategy_names = []
    for strategy_file in strategy_files:
        if strategy_file.endswith(".py"):
            strategy_module = __import__("sample_strategies." + strategy_file[:-3], fromlist=[""])
            strategy_classes.append(strategy_module.MyStrategy)
            strategy_names.append(strategy_file[:-3])
    for i, strategy_class in enumerate(strategy_classes):
        strategies.append(strategy_class(i))
    print(strategy_names)
    game_parameters = GameParameters()
    game = Game(game_parameters, tuple(strategies))
    winner = game.play()
    print("The winner is " + strategy_names[winner])

if __name__ == "__main__":
    main()
