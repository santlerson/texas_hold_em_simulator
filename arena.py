import time
from typing import List
import os
from importlib import import_module

import strategy
import strategy_wrapper
from game import Game
from game import GameParameters
from logger import Logger


LOG_DIR = "logs"
def arena(strategy_paths, strategy_names, game_parameters=None, development_mode=False):
    # foreach python file in sample_strategies, import class and add to strategies
    strategy_classes = []
    strategies: List[strategy.Strategy] = []
    for strategy_file, strategy_name in zip(strategy_paths, strategy_names):
        if strategy_file.endswith(".py"):
            if development_mode:
                dir = os.path.dirname(strategy_file)
                file_name = os.path.basename(strategy_file)
                strategy_module = import_module(dir + "." + file_name[:-3], package=None)
                strategy_class = strategy_module.MyStrategy
            else:
                strategy_class= strategy_wrapper.get_securely_wrapped_class(strategy_file)
            strategy_classes.append(strategy_class)
            # strategy_names.append(strategy_name)

    for i, strategy_class in enumerate(strategy_classes):
        strategies.append(strategy_class(i))
    print(strategy_names)
    if game_parameters is None:
        game_parameters = GameParameters()
    logger = Logger(strategy_names)
    game = Game(game_parameters, tuple(strategies), logger)
    winner = game.play()
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logger.write(os.path.join("logs", f"{time.time()}.xml"))
    print("The winner is " + strategy_names[winner])


STRATEGIES_DIR = "sample_strategies"

def main():
    files = [os.path.join(STRATEGIES_DIR, f) for f in os.listdir(STRATEGIES_DIR)]
    strategy_names = []
    strategy_files = []
    for strategy_file in files:
        if strategy_file.endswith(".py"):
            strategy_names.append(strategy_file[:-3])
            strategy_files.append(strategy_file)
    arena(strategy_files, strategy_names,
          development_mode=False  # set to True during development for more easy debugging
          )


if __name__ == "__main__":
    main()