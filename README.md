#Texas Hold 'Em Poker Simulator
##Getting Started
Clone this repository
```
git clone https://github.com/santlerson/texas_hold_em_simulator.git
```
Navigate to the directory
```
cd texas_hold_em_simulator
```
Install the dependencies
```
pip install -r requirements.txt
```
Try running the main script!
```
python3 arena.py
```

##Making your own strategy
The base class for strategies is in `strategy.py`
(which also includes an explanation of all the inputs and outputs of the strategy's functions).
Examples can be seen in `sample_strategies/`. Add your strategies to this directory to test them out against
the others!


Developed and tested on Python 3.9.2