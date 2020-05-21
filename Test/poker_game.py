from datetime import datetime

from system_tool import small_blind
from player import Player
from table import Table


class Poker_Game:

    def __init__(self, id: int, properties: []):

        self.id = id
        self.mode = properties[1]
        self.name = properties[2]
        self.start_time = float(properties[3])
        self.players_limit = int(properties[4])
        self.entry_amount = int(properties[5])
        self.small_blind = small_blind(self.mode, self.entry_amount)
        self.stakes_ratio = int(properties[6])
        self.rebuy = bool(properties[7])

        self.tables = []
        self.players = 0
        self.aux_id = 0

    def start_game(self):

        # Wait For Game Start Time
        while self.start_time > datetime.timestamp(datetime.now()):
            pass

        print('Game ' + self.id + ' started')

        # Start Game In Tables With More Than One Player
        for table in self.tables:
            if len(table.players) > 1:
                table.start_game()

    def add_player(self, player: Player):

        # Check If Capacity Limit Reached
        if self.players < self.players_limit:
            # Add Player To Table
            for table in self.tables:
                if table.add_player(player):
                    break
            # No Available Tables, Create Table
            else:
                table = Table(self.assign_id(), self.id,
                              self.small_blind, self.stakes_ratio)
                table.add_player(player)
                self.tables.append(table)

            self.players += 1
            return True

        else:
            return False

    def assign_id(self):

        self.aux_id += 1
        return self.aux_id
