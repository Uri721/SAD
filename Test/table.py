from datetime import datetime

from system_tool import game_state
from system_tool import player_actions
from system_tool import format_cards
from hand_rank import rank

from deck import Deck
from deck import Card

from player import Player


class Table:

    def __init__(self, id: int, game_id: int, small_blind: int, stake_ratio: int):

        self.table_capacity = 10

        self.id = id
        self.game_id = game_id

        self.small_blind = small_blind
        self.stake_ratio = stake_ratio

        self.players = []
        self.in_game_players = 0
        self.deck = Deck()
        self.community_cards = []

        self.state = game_state.index('pre_flop')
        self.highest_bet = 0
        self.dealer_postion = 0
        self.target_position = 0
        self.pot = 0

        self.terminated = False

    # Game State Control Functions
    def start_game(self):

        #self.stake_time = datetime.now()

        while self.terminated:

            if self.state == game_state.index('pre_flop'):
                self.start_hand()

            if self.state == game_state.index('flop') or game_state.index('river') or game_state.index('turn'):
                self.update_hand()

            else:
                self.end_hand()

    def start_hand(self):

        self.blinds()
        self.deck.shuffle()
        self.deal_cards(False)
        self.betting_round()
        self.update_state()

    def update_hand(self):

        self.deal_cards(True)
        self.betting_round()
        self.update_state()

    def end_hand(self):

        self.showdown()
        self.update_state()

    # Game Properties Control Functions

    def blinds(self):

        self.players[self.dealer_postion+1].update_balance(self.small_blind)
        self.pot += self.small_blind

        self.players[self.dealer_postion+1].update_balance(self.small_blind*2)
        self.pot += self.small_blind * 2

        self.highest_bet = self.small_blind * 2

        self.update_players_view()

    def deal_cards(self, community_cards: bool):

        if community_cards:

            if self.state == game_state.index('flop'):
                self.deck.deal(1)
                self.community_cards[0:3] = self.deck.deal(3)

            elif self.state == game_state.index('river') or game_state.index('turn'):
                self.deck.deal(1)
                self.community_cards[3] = self.deck.deal(1)

        else:

            self.deck.deal(1)

            i = 1
            while i <= len(self.players):
                self.update_target_position(i)
                self.players[self.target_position].update_cards(
                    self.deck.deal(2))
                i += 1

        self.update_players_view()

    def betting_round(self):

        last_to_talk = self.dealer_postion

        if self.state == game_state.index('pre_flop'):
            self.update_target_position(3)

        else:
            self.update_target_position(1)

        while True:

            target_player = self.players[self.target_position]

            if target_player.in_game:
                data = target_player.make_decision()

                if data[0] == player_actions.index('check'):
                    pass

                elif data[0] == player_actions.index('call'):
                    amount = (self.highest_bet - target_player.current_bet)
                    self.pot += amount
                    target_player.update_balance(amount, False)

                elif data[0] == player_actions.index('fold'):
                    target_player.in_game = False
                    self.in_game_players -= 1

                elif data[0] == player_actions.index('raise'):
                    amount = data[1]
                    self.pot += amount
                    target_player.update_balance(amount, False)
                    self.highest_bet = target_player.current_bet
                    last_to_talk = (self.target_position +
                                    self.table_capacity - 1) % self.table_capacity

            self.update_players_view()

            if self.target_position == last_to_talk:
                break

        for player in self.players:
            player.current_bet = 0

    def showdown(self):

        if self.in_game_players > 1:
            ranks = []
            for player in self.players:
                if player.in_game:
                    ranks.append((player.table_position, rank(
                        format_cards(player.cards + self.community_cards))))

            print(ranks)
            # COMPARAR RANKS, DETERMINAR GUANYADORS I REPARTIR POT ENTRE GUANYADORS

        else:
            for player in self.players:
                if player.in_game:
                    player.update_balance(self.pot, True)
                    self.pot = 0
                    break

        self.hand_finished()

    def update_state(self):

        if(self.state == game_state.index('showdown')):
            self.state = game_state.index('pre_flop')
            return

        if self.in_game_players < 2:
            self.state = game_state.index('showdown')
            return

        else:
            self.state += 1

    def hand_finished(self):

        # Remove Cards & Broke Players
        self.community_cards.clear()

        for player in self.players:
            player.cards.clear()
            if player.balance == 0:
                player.terminated(self.game_id + self.id)
                self.remove_player(player)
            else:
                player.in_game = True

        # Terminate Game If Less Then Two Players Remaining
        self.in_game_players = len(self.players)
        if self.in_game_players < 2:
            self.terminated = True

        # Update Dealer & Target Position
        self.dealer_postion = (self.dealer_postion + 1) % len(self.players)
        self.target_position = self.dealer_postion

    def update_target_position(self, offset: int):

        self.target_position = (self.dealer_postion +
                                offset) % len(self.players)

    def add_player(self, player: Player):

        if len(self.players) < self.table_capacity:
            self.players.append(player)
            self.in_game_players += 1
            return True

        else:
            return False

    def remove_player(self, player: Player):

        self.players.remove(player)

    def update_players_view(self):

        data = []
        data.append(self.game_id + self.id)
        data.append(self.pot)
        data.append(self.small_blind)
        data.append(self.community_cards)
        data.append(self.dealer_postion)
        data.append(self.target_position)

        for player in self.players:
            aux = []
            aux.append(player.table_poition)
            aux.append(player.user.username)
            aux.append(player.in_game)
            aux.append(player.current_bet)
            aux.append(player.balance)
            data.append(aux)
            player.update_view(data)


cards1 = []
cards1.append(Card(0, 2))
cards1.append(Card(0, 3))
cards1.append(Card(0, 4))
cards1.append(Card(0, 5))
cards1.append(Card(0, 6))

cards2 = []
cards2.append(Card(2, 14))
cards2.append(Card(3, 14))
cards2.append(Card(1, 14))
cards2.append(Card(2, 5))
cards2.append(Card(0, 6))

ranks = []
ranks.append((0, rank(format_cards(cards1))))
ranks.append((1, rank(format_cards(cards2))))

print(ranks)

# SEND

# GAME VIEW UPDATE [BROADCAST]
# ID: game_update
# [‘750’,’50’,’3’,’4’,’$’,’alba’,’3’,’300’,’5000’,’0’,’13’,’314’,’uri’,’4’,’300’,’2500’,’0’,’32’,’310’,’josep’,’1’,’300’,’7000’,’0’,’43’,’110’,’ines’,’8’,’300’,’500’,’0’,’35’,’37’,’$’,’34’,’42’,’414’,’411’,’-1’]
# ['pot','small blind','dealer_position','target_position','$','player_name','player_position','playert_bet','player_stack','player_state','player_card_1','player_card_2','$','community_card_1','community_card_2','community_card_3','community_card_4','community_card_5',]

# ROUND RESULT UPDATE [BROADCAST]
# ID: round_result
# ['willy']
# ['598','two_pair',''willy','jhonny'] POT HAVER-HI MES D'UN GUANYADOR, LA MA, EL 598, ENVIAMHO UTILITZANT game_rank_id_b_cmd DE SYSTEM TOOL
# ['winning_hand','player_name'] QUE HA SIGUT LA MA GUANYADORA I QUI HA GUANYAT

# PLAYER GAME RESULT
# ID: game_result
# ['3','20000'] POSICIO FINAL A LA PARTIDA I PASTA GUANYADA
# ['final_result', 'winnings']

# PLAYER DECISION REQUEST
# ID: player_request

# RECEIVE

# DISCONNECT
# ID: disconnect

# PLAYER DECISION REPLY
# ID: player_reply
# ['511'] (FOLD) ENVIAHO AMB player_action_id_b_cmd DE SYSTEM TOOL
# ['512','300'] RAISE PORTA DARRERE LA QUANTITAT QUE S'HA APOSTAT
# ['player_decision']
