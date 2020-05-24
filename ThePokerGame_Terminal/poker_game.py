from poker_table import Poker_Table


class Poker_Game(object):

    def __init__(self):

        self.players_limit = 2
        self.players = 0

        self.entry_amount = 2000
        self.small_blind = 20

        self.table = Poker_Table(self.small_blind)

    def start_game(self):

        while self.table.game_players < self.players_limit:
            pass

        self.table.start_game()

    # Players Management

    def add_player(self, player):

        self.table.add_player(player)
