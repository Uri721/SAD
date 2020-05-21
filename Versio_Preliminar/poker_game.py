import threading
from datetime import datetime

from system_tool import game_mode_id_b_cmd as game_mode_id
from system_tool import game_state_id_b_cmd as game_state_id

from poker_tool import small_blind

from poker_table import Poker_Table


class Poker_Game(object):

    def __init__(self, id: int, game_properties: []):

        self.id = id
        self.mode = game_properties[1]
        self.name = game_properties[2]

        if self.mode == game_mode_id['cash_game']:
            threading.Thread(target=self.cash_game,
                             args=(game_properties,)).start()

        elif self.mode == game_mode_id['sit_and_go']:
            threading.Thread(target=self.sit_and_go,
                             args=(game_properties,)).start()

        elif self.mode == game_mode_id['sit_and_go_express']:
            threading.Thread(target=self.sit_and_go_express,
                             args=(game_properties,)).start()

        elif self.mode == game_mode_id['tournament']:
            threading.Thread(target=self.tournament,
                             args=(game_properties,)).start()

    def cash_game(self, game_properties: []):
        pass

    def sit_and_go(self, game_properties: []):

        self.start_time = float(game_properties[3])
        self.players_limit = int(game_properties[4])
        self.entry_amount = int(game_properties[5])
        self.small_blind = small_blind(self.mode, self.entry_amount)
        self.stakes_ratio = int(game_properties[6])
        self.rebuy = bool(game_properties[7])

        self.terminated = False
        self.players = 0
        self.table = Poker_Table(
            self.id, 1, self.small_blind, self.stakes_ratio)

        while not self.terminated:

            while (self.start_time > datetime.timestamp(datetime.now())) and (len(self.table.players) < self.table.limit):
                pass

            print('Game ' + self.id + ' started')

            self.table.start_game()

            while self.table.state != game_state_id['terminated']:
                pass

            self.terminated = True

            print('Game ' + self.id + ' finnished')

    def sit_and_go_express(self, game_properties: []):
        pass

    def tournament(self, game_properties: []):

        self.start_time = float(game_properties[3])
        self.players_limit = int(game_properties[4])
        self.entry_amount = int(game_properties[5])
        self.small_blind = small_blind(self.mode, self.entry_amount)
        self.stakes_ratio = int(game_properties[6])
        self.rebuy = bool(game_properties[7])

        self.aux_id = 0
        self.players = 0
        self.tables = []

    # Players Management

    def add_player(self, player):

        if self.mode == game_mode_id['cash_game'] or game_mode_id['sit_and_go'] or game_mode_id['sit_and_go_express']:

            if self.table.add_player(player):
                self.players += 1
                return True

            else:
                return False

        elif self.mode == game_mode_id['tournament']:

            if self.players < self.players_limit:

                for table in self.tables:
                    if table.add_player(player):
                        break

                else:
                    table = Poker_Table(self.assign_id(), self.id,
                                        self.small_blind, self.stakes_ratio)
                    table.add_player(player)
                    self.tables.append(table)

                self.players += 1
                return True

            else:
                return False

    # Identification Management Tool

    def assign_id(self):

        self.aux_id += 1
        return self.aux_id
