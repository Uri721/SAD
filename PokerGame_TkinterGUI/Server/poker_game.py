import threading
import time
from datetime import datetime

from system_tool import game_mode_id_b_cmd as game_mode_id
from system_tool import game_state_id_b_cmd as game_state_id

from poker_tool import small_blind

from poker_table import Poker_Table


class Poker_Game(object):

    def __init__(self, id: int, game_properties: []):

        print('poker game iniciat: ' + str(id) + ' ' + str(game_properties[1]))
        self.id = id
        self.mode = game_properties[1]
        self.name = game_properties[2]
        self.start_time = float(game_properties[3])
        self.players_limit = int(game_properties[4])
        self.players = 0
        self.tables = []
        self.game_properties = game_properties

    def __str__(self):

        return ('ID: ' + str(self.id) + ' MODE: ' + str(self.mode) + ' NAME/START_TIME/LIMIT: ' + self.name+' '+str(self.start_time) + ' ' + str(self.players_limit) + ' PLAYERS IN GAME: ' + str(self.players) + 'TABLE: ' + str(self.tables[0]))

    def start_game(self):
        if self.mode == game_mode_id['cash_game']:
            self.cash_game(self.game_properties)

        elif self.mode == game_mode_id['sit_and_go']:
            self.sit_and_go(self.game_properties)

        elif self.mode == game_mode_id['tournament']:
            print('NO HAURIA')

    def cash_game(self, game_properties: []):
        pass

    def sit_and_go(self, game_properties: []):

        print('sitandgo')

        self.entry_amount = int(game_properties[5])
        self.small_blind = small_blind(self.mode, self.entry_amount)
        self.stakes_ratio = int(game_properties[6])
        self.rebuy = bool(game_properties[7])

        self.terminated = False
        self.tables += [Poker_Table(self.id, 1,
                                    self.small_blind, self.stakes_ratio)]
        print(str(self))

        while (self.start_time > datetime.timestamp(datetime.now())) and (self.tables[0].game_players < 2):
            pass

        print('Game ' + str(self.id) + ' started')

        self.tables[0].start_game()

        while self.tables[0].state != game_state_id['terminated']:
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

    # Players Management

    def add_player(self, player):

        if self.mode == game_mode_id['cash_game'] or game_mode_id['sit_and_go'] or game_mode_id['sit_and_go_express']:

            if self.tables[0].add_player(player):
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

    def not_full(self):

        return (self.players <= self.players_limit)

    # Identification Management Tool

    def assign_id(self):

        self.aux_id += 1
        return self.aux_id
