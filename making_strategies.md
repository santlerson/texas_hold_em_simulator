# Making Strategies

## The Game

The game being played here is [Texas Hold 'Em](https://en.wikipedia.org/wiki/Texas_hold_%27em). More specifically, it is
No Limit Texas Hold 'Em with blinds. This means that there is no upper bound on bets (other than a players
balance/stack) and that two players are forced to bet before the cards are dealt.

## Getting Started

Let's make a copy of `call_strategy.py` and take a look at it:

```python
from strategy import Strategy


class MyStrategy(Strategy):

    def __init__(self, player_id, blind_period, initial_big_blind, initial_small_blind, blind_base):
        super().setup(player_id, blind_period, initial_big_blind, initial_small_blind, blind_base)

    def get_bet(self, round_id, balances, bets,
                small_blind_index, big_blind_index,
                players_in_game, community_cards,
                hole_cards, folded):
        return min(balances[self.player_id], max(bets) - bets[self.player_id])

    def inform_result(self, round_id: int, balances,
                      holes_cards,
                      community_cards,
                      bets):
        pass
```

Let's start by looking at the body of `get_bet()`. This is the function that is called when it is your turn to bet. It
is passed a bunch of information about the current state of the game. The function should return the amount of money you
want to bet (meaning the number of chips you want to put in the pot this time). A fold corresponds to any value which
would not be a valid and legal bet for example:

- `-1`
- `0.5`
- `1.0` (or any whole number passed as a float)
- `"fold"`
- `"My name is Inigo Montoya. You killed my father. Prepare to die."`
- Any amount more than your remaining stack

### What should I return to call?

Typically, in order to call, you would need to put an amount that would bring your bet up to the highest bet so
far (`max(bets)`). However, if your remaining stack is less than this amount, this is more than you can bet. In this
case, you should bet your remaining stack. Hence, in the example above, we return:

```python
min(balances[self.player_id], max(bets) - bets[self.player_id])
```

Any bet strictly less than this would be considered a fold.

### What should I return to raise?

To raise, you need to put in an amount that is greater than the highest bet so far (`max(bets)`). However, if your
remaining stack is less than this amount, this is more than you can bet. Therefore suppose we wanted to raise _by_ 15 (
and we knew we could afford it) then we would return:

```python
max(bets) + 15
```

### How do I look at my cards?

In order to make decisions, you will need to look at your cards. These are passed to you in the variable `hole_cards`.
This is a tuple of cards (pairs of integers, for first is the rank 2-14 representing 2-Ace and the second is the suit
0-3 representing clubs, hearts, spades, and diamonds respectively). For example, if you had a pair of aces (clubs and
hearts) in your hand, you would be passed the tuple `((14, 0), (14, 1))`. If you had a king and a queen (both spades),
you would be passed the tuple `((13, 2), (12, 2))`. Let's look at the implementation
in `pocket_rockets_all_in_strategy.py`:

```python
 (rank1, _), (rank2, _) = hole_cards
if rank1 == rank2 == 14:
    return balances[self.player_id]
else:
    return 0
```

Here we unpack our hole, and if we have a pair of aces, we go all in. Otherwise, we check/fold (return 0).

### One final note about `get_bet()`

In a round in which you have folded, more subsequent calls to `get_bet()` will be made. These calls serve to inform you
of the state of the game (what others are betting, what cards are on the table, etc.). The return value is not important
in these cases.

For a detailed explanation on the parameters of `get_bet()`, see the docstring in `strategy.py`.

### A look at `inform_result()`:

Your strategy has not only freedom to make decisions according to the state of the game, but also freedom to learn from
previous outcomes. Say, for example we wanted to find out which of our opponents tend to bluff. We could do this by
looking at their bets and at their hands. This is the purpose of
`inform_result()`. It is called at the end of each round and is passed information about the outcome of the round. It is
up to you to decide what to do with this information. In the example above, we do nothing with it. However, if we wanted
to keep track of the hands of our opponents, we would do that here. A note here would be that we will not always get a
chance to look at everyone's hands. For example if that player folded, or if all players except them folded, we will not
be able to see their hand. In the former case that player's hand will be represented by `None` and in the latter case,
the list of all hands will be replaced by
`None`.

### `__init__()` and blind structure

The following are the parameters of `__init__()`:

- `player_id`: The id of the player. This is an integer representing the index of the user in al relevant lists/tuples
  (e.g. `bets`, `balances`, `players_in_game`, etc.)
- `blind_period`: The number of rounds between increases in the blinds.
- `initial_big_blind`: The initial big blind.
- `initial_small_blind`: The initial small blind.
- `blind_base`: The base of the geometric progression used to increase the blinds.

The blinds "increase by a certain percentage" each period of rounds. The formula for the blinds is as follows:

```
initial_big_blind * blind_base ** (round_id // blind_period)
```

and likewise for the small blind. For example, if `blind_period = 10`, `initial_big_blind = 20`,
`initial_small_blind = 10`, and `blind_base = 1.2`, then the blinds would initially be 20 and 10 respectively. Each 10
rounds, the blinds would increase by 20% (i.e. multiply by 1.2 rounding down). These parameters are passed to
the `__init__()` function, and if you make a call there to `self.setup()` (as is recommended, see example strategies),
they will also be kept in corresponding attributes of the strategy object, and this calculation will be accessible via:

```python
sb, bb = self.get_current_blinds(round_id)
```

where `round_id` is the current round. This is useful for making decisions based on the blinds.

## Final Notes

- Your class _must_ be called `MyStrategy` and must inherit from `Strategy`.
- No reading/writing files at runtime
- No importing modules with some notable exceptions:
  - `import math` (and not `from math import *` etc.)
  - `import random` (and not `from random import *` etc.)
  - `from strategy import Strategy`
  - (I will strongly consider adding support for numpy)