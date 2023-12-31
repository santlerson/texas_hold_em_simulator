# import xml.etree.ElementTree as ET
from typing import List
import json

# class XMLLogger:
#     def __init__(self, player_names: List[str]):
#         self.log = ET.Element('log')
#         self.log.set('version', '1.0')
#         self.players = ET.SubElement(self.log, 'players')
#         for i, player_name in enumerate(player_names):
#             player = ET.SubElement(self.players, 'player')
#             player.set('name', player_name)
#             player.set('id', str(i))
#         self.rounds = ET.SubElement(self.log, 'rounds')
#         self.current_round = None
#         self.current_round_stages=None
#         self.stage = None
#         self.stage_element = None
#
#     def create_new_round(self, bb_index, sb_index):
#         self.current_round = ET.SubElement(self.rounds, 'round')
#         self.current_round.set("bb", str(bb_index))
#         self.current_round.set("sb", str(sb_index))
#         self.current_round_stages = ET.SubElement(self.current_round, 'stages')
#         self.stage = 0
#         self.stage_element = ET.SubElement(self.current_round_stages, 'stage')
#
#         # hole_cards_element = ET.SubElement(self.current_round, 'hole_cards')
#         # for i, hole_card in enumerate(hole_cards):
#         #     (rank1, suit1), (rank2, suit2) = hole_card
#         #     hole_card_element = ET.SubElement(hole_cards_element, 'hole_card')
#         #     hole_card_element.set('player', str(i))
#         #     hole_card_element.set('rank1', str(rank1))
#         #     hole_card_element.set('suit1', str(suit1))
#         #     hole_card_element.set('rank2', str(rank2))
#         #     hole_card_element.set('suit2', str(suit2))
#         # community_cards_element = ET.SubElement(self.current_round, 'community_cards')
#         # for i, community_card in enumerate(community_cards):
#         #     (rank, suit) = community_card
#         #     community_card_element = ET.SubElement(community_cards_element, 'community_card')
#         #     community_card_element.set('rank', str(rank))
#         #     community_card_element.set('suit', str(suit))
#
#     def log_holes_cards(self, hole_cards):
#         hole_cards_element = ET.SubElement(self.current_round, 'hole_cards')
#         for i, hole_card in enumerate(hole_cards):
#             (rank1, suit1), (rank2, suit2) = hole_card
#             hole_card_element = ET.SubElement(hole_cards_element, 'hole_card')
#             hole_card_element.set('player', str(i))
#             hole_card_element.set('rank1', str(rank1))
#             hole_card_element.set('suit1', str(suit1))
#             hole_card_element.set('rank2', str(rank2))
#             hole_card_element.set('suit2', str(suit2))
#
#     def log_community_cards(self, community_cards):
#         community_cards_element = ET.SubElement(self.current_round, 'community_cards')
#         for i, community_card in enumerate(community_cards):
#             (rank, suit) = community_card
#             community_card_element = ET.SubElement(community_cards_element, 'community_card')
#             community_card_element.set('rank', str(rank))
#             community_card_element.set('suit', str(suit))
#
#     def advance_stage(self):
#         self.stage = self.stage + 1
#         self.stage_element = ET.SubElement(self.current_round_stages, 'stage')
#
#     def log_bet(self, player_id, bet, total_in_pot):
#         bet_element = ET.SubElement(self.stage_element, 'bet')
#         bet_element.set('player', str(player_id))
#         bet_element.set('amount', str(bet))
#         bet_element.set('total_in_pot', str(total_in_pot))
#
#     def log_fold(self, player_id):
#         fold_element = ET.SubElement(self.stage_element, 'fold')
#         fold_element.set('player', str(player_id))
#
#     def log_results(self, payouts, new_balances):
#         results_element = ET.SubElement(self.current_round, 'results')
#         for i, payout in enumerate(payouts):
#             result_element = ET.SubElement(results_element, 'result')
#             result_element.set('player', str(i))
#             result_element.set('payout', str(payout))
#             result_element.set('balance', str(new_balances[i]))
#
#
#     def write(self, filename):
#         tree = ET.ElementTree(self.log)
#         tree.write(filename)
#
# #refactor in json
class Logger:
    def __init__(self, player_names: List[str]):
        self.log = {}
        self.log["players"] = player_names
        self.log["rounds"] = []
        self.current_round = None
        self.current_round_stages=None
        self.stage = None
        self.stage_element = None

    def log_game_params(self, game_params):
        self.log["parameters"]={
            "starting_balance": game_params.starting_balance,
        }
    def create_new_round(self, bb_index, sb_index):
        #clear out last stage if empty
        if self.stage_element is not None and len(self.stage_element["actions"]) == 0:
            del self.current_round["stages"][-1]
        self.current_round = {}
        self.current_round["bb"] = bb_index
        self.current_round["sb"] = sb_index
        self.current_round["stages"] = []
        self.stage = -1
        self.advance_stage()
        # self.current_round["stages"].append(self.stage_element)
        self.log["rounds"].append(self.current_round)

    def log_holes_cards(self, hole_cards):
        self.current_round["hole_cards"] = hole_cards

    def log_community_cards(self, community_cards):
        self.current_round["community_cards"] = community_cards

    def advance_stage(self):
        self.stage = self.stage + 1
        self.stage_element = {"actions":[]}
        self.current_round["stages"].append(self.stage_element)

    def log_bet(self, player_id, bet, total_in_pot):
        bet_element = {"player":player_id, "amount":bet, "total_in_pot":total_in_pot}
        self.stage_element["actions"].append(bet_element)

    def log_fold(self, player_id):
        fold_element = {"player":player_id}
        self.stage_element["actions"].append(fold_element)

    def log_results(self, payouts, new_balances):
        self.current_round["payouts"] = payouts
        self.current_round["new_balances"] = new_balances

    def log_blinds(self, bb, sb):
        self.current_round["bb_amount"] = bb
        self.current_round["sb_amount"] = sb

    def write(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.log, outfile)



