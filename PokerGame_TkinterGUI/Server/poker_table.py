import threading
import time

from system_tool import data_transmission_separator as dts
from system_tool import update_id_h_cmd as update_id
from system_tool import game_state_id_b_cmd as game_state_id
from system_tool import player_action_id_b_cmd as player_action_id

from poker_tool import Deck
from poker_tool import Card
from poker_tool import player_state
from poker_tool import finish_round

from server_player import Server_Player


class Poker_Table(object):

    def __init__(self, game_id: int, table_id: int, small_blind: int, stake_ratio: int):

        print('TAULA INICIALITZADA')
        self.limit = 10

        self.game_id = game_id
        self.table_id = table_id

        self.small_blind = small_blind
        self.stake_ratio = stake_ratio

        self.deck = Deck()
        self.community_cards = [None, None, None, None, None]

        self.players = []
        for _ in range(self.limit):
            self.players += [None]

        self.game_players = 0
        self.in_game_players = 0

        self.pot = 0
        self.highest_bet = 0
        self.dealer = 0
        self.target = -1

        self.state = 0
        self.terminated = False

    def __str__(self):

        return ('TABLE ID: ' + str(self.table_id)+' SMALL BLIND: ' + str(self.small_blind)+' STAKE RATIO: '+str(self.stake_ratio)+' COMMUNITY CARDS: '+str(self.community_cards)+' PLAYERS: '+str(self.players)+' GAME PLAYERS: '+str(self.game_players)+' IN GAME PLAYERS: '+str(self.in_game_players)+' POT: '+str(self.pot)+' HIGHEST BET: '+str(self.highest_bet)+' DEALER: '+str(self.dealer)+' TARGET: '+str(self.target)+' STATE: '+str(self.state))

    def start_game(self):

        t_g = threading.Thread(target=self.game_state_control)
        t_g.name = 'game_state_control'
        t_g.start()
        t_p = threading.Thread(target=self.players_state_control)
        t_p.name = 'players_state_control'
        t_p.start()

    # Game State Management

    def game_state_control(self):

        self.update_state()

        while self.state != game_state_id['terminated']:

            print('INICI JOC A LA TAULA')
            print(str(self))
            if self.state == game_state_id['pre_flop']:

                self.blinds()
                self.deck.shuffle()
                self.deal_cards()
                self.betting_round()
                self.update_state()

            elif self.state == game_state_id['flop'] or game_state_id['river'] or game_state_id['turn']:
                print(self.state)
                self.deal_cards()
                self.betting_round()
                self.update_state()

            elif self.state == game_state_id['showdown']:

                self.showdown()
                self.update_state()

    # Player State Management

    def players_state_control(self):

        while self.state != game_state_id['terminated']:

            for player in self.players:
                if (player is not None) and (not player.connected):
                    self.players[self.players.index(player)] = None
                    self.game_players -= 1
                time.sleep(1)

    def add_player(self, player: Server_Player):

        if self.game_players < self.limit:
            self.players[self.players.index(None)] = player
            self.game_players += 1
            player.table_position = (self.players.index(player) + 1)
            print('ADD PLAYER: ' + str(self))
            return True

        else:
            return False

    # Game Properties Control Functions

    def blinds(self):

        print('CEGUES')

        _ = self.next_player_position(self.dealer)

        self.players[_].update_stack(self.small_blind, False)
        print(self.players[_].name + ' ha pagat' + str(self.small_blind))
        self.pot += self.small_blind

        _ = self.next_player_position(_)

        self.players[_].update_stack(self.small_blind * 2, False)
        print(self.players[_].name + ' ha pagat' + str(self.small_blind))
        self.pot += self.small_blind * 2

        self.highest_bet = self.small_blind * 2

        self.update_players_view()

    def deal_cards(self):

        if self.state == game_state_id['pre_flop']:

            self.update_target('cards_deal')
            print('REPARTINT CARTES PRE FLOP')

            for _ in range(self.in_game_players):
                self.players[self.target].update_cards(
                    self.deck.deal(2))
                print(self.players[self.target].name + ' ha rebut ' + str(
                    self.players[self.target].cards[0]) + ' ' + str(self.players[self.target].cards[1]))
                self.update_target('increment')

        elif self.state == game_state_id['flop']:
            print('REPARTINT CARTESFLOP')
            self.deck.deal(1)
            self.community_cards[0:3] = self.deck.deal(3)

        elif self.state == game_state_id['river']:
            print('REPARTINT CARTES RIVER')
            self.deck.deal(1)
            self.community_cards[3] = self.deck.deal(1)

        elif self.state == game_state_id['turn']:
            print('REPARTINT CARTES TURN')
            self.deck.deal(1)
            self.community_cards[4] = self.deck.deal(1)

        self.target = -1
        self.update_players_view()

    def betting_round(self):

        last_to_talk = self.dealer
        self.update_target('round_start')

        print('RONDA APOSTES')

        while True:

            if self.target == last_to_talk:
                print('Target: ' + str(self.target) +
                      ' last to talk : ' + str(last_to_talk))
                break

            data = self.players[self.target].decide()

            if data[0] == player_action_id['check']:
                pass

            elif data[0] == player_action_id['fold']:
                self.players[self.target].state = player_state['out_game']
                self.in_game_players -= 1

            elif data[0] == player_action_id['raise']:
                amount = data[1]
                self.pot += amount
                self.players[self.target].update_stack(amount, False)
                self.highest_bet = self.players[self.target].bet
                last_to_talk = self.target

            elif data[0] == player_action_id['call']:
                amount = (self.highest_bet -
                          self.players[self.target].bet)
                self.pot += amount
                self.players[self.target].update_stack(amount, False)

            self.update_target('increment')

        for player in self.players:
            if player is not None:
                player.bet = 0

    def showdown(self):

        self.target = -1

        if self.in_game_players > 1:

            usernames = []
            cards = []

            hand_result = -1

            for player in self.players:
                if (player is not None) and (player.state == player_state['in_game']):
                    usernames += [player.name]
                    cards += [player.cards[0].formatted() + ' ' + player.cards[1].formatted() + ' ' + self.community_cards[0].formatted() +
                              ' ' + self.community_cards[1].formatted() + ' ' + self.community_cards[2].formatted()]

            winner, hand_result = finish_round(usernames, cards)

        else:
            print('SHOW')
            for player in self.players:
                if (player is not None) and (player.state == player_state['in_game']):
                    print('done')
                    player.update_balance(self.pot, True)
                    winner = player.name
                    self.pot = 0
                    break

        self.update_players_view()
        self.update_round_result(hand_result, winner)

        for player in self.players:
            if (player is not None) and (player.stack == 0):
                player.send([update_id['game_result'], (self.game_players), 0])
                self.players[self.players.index(player)] = None
                self.game_players = self.game_players - 1

        self.community_cards = [None, None, None, None, None]
        self.update_players_view()

    # Game Parameters Management

    def update_state(self):

        if self.state == 0:
            for player in self.players:
                if player is not None:
                    player.state = 0
                    self.in_game_players += 1
            self.state = game_state_id['pre_flop']

        elif self.state == game_state_id['showdown']:
            if self.game_players < 2:
                self.terminated = True
                return

            self.update_dealer()
            self.state = game_state_id['pre_flop']

            self.in_game_players = 0
            for player in self.players:
                if player is not None:
                    player.state = 0
                    self.in_game_players += 1
            return

        elif self.in_game_players < 2:
            self.state = game_state_id['showdown']
            return

        else:
            self.state += 1

        self.update_players_view()

    def update_dealer(self):

        self.dealer = self.next_player_position(self.dealer)
        self.update_players_view()

    def update_target(self, cmd: str):

        if cmd == 'increment':
            self.target = self.next_player_position(self.target)

        elif cmd == 'cards_deal':
            self.target = self.next_player_position(self.dealer)

        elif cmd == 'round_start':

            if self.state == game_state_id['pre_flop']:
                self.target = self.next_player_position(self.dealer)
                self.target = self.next_player_position(self.target)
                self.target = self.next_player_position(self.target)

            else:
                self.target = self.next_player_position(self.dealer)

        self.update_players_view()

    def next_player_position(self, target: int):

        for _ in range(self.limit):
            target = ((target + 1) % self.limit)
            if (self.players[target] is not None) and (self.players[target].state == player_state['in_game']):
                return target

    # Game View Update

    def update_players_view(self):

        print('Update players view')
        print(str(self))

        dealer_aux = int(self.dealer) + 1
        target_aux = int(self.target) + 1
        tx_data = [update_id['game_update']]
        tx_data += [self.pot, self.small_blind, self.highest_bet,
                    dealer_aux, target_aux]

        tx_data += dts

        for player in self.players:
            if player is not None:
                tx_data += [player.name, player.table_position, player.bet,
                            player.stack, player.state]
                if player.cards[0] is not None:
                    tx_data += [player.cards[0].to_transmit(),
                                player.cards[1].to_transmit()]
                else:
                    tx_data += [-1, -1]

        tx_data += dts

        for card in self.community_cards:
            if card is None:
                tx_data += [-1]
            else:
                tx_data += [card.to_transmit()]

        for player in self.players:
            if player is not None:
                print('TX TO ' + player.name + ' : ')
                print(tx_data)
                player.send(tx_data)

        time.sleep(10)

    # Round Result Update

    def update_round_result(self, hand_result: int, winners: []):

        tx_data = [update_id['round_result']]
        tx_data += [hand_result]
        tx_data += winners

        for player in self.players:
            if player is not None:
                player.send(tx_data)

        time.sleep(10)

# SEND

# GAME VIEW UPDATE [BROADCAST]
# ID: game_update
# [‘750’,’50’,’3’,’4’,’$’,’alba’,’3’,’300’,’5000’,’0’,’13’,’314’,’uri’,’4’,’300’,’2500’,’0’,’32’,’310’,’josep’,’1’,’300’,’7000’,’0’,’43’,’110’,’ines’,’8’,’300’,’500’,’0’,’35’,’37’,’$’,’34’,’42’,’414’,’411’,’-1’]
# ['pot','small blind','highest_bet','dealer_position','target_position','$','player_name','player_position','playert_bet','player_stack','player_state','player_card_1','player_card_2','$','community_card_1','community_card_2','community_card_3','community_card_4','community_card_5',]

# ROUND RESULT UPDATE [BROADCAST]
# ID: round_result
# ['willy']
# ['598','two_pair',''willy','jhonny'] POT HAVER-HI MES D'UN GUANYADOR, LA MA, EL 598, ENVIAMHO UTILITZANT game_rank_id_b_cmd DE SYSTEM TOOL
# ['winning_hand','player_name'] QUE HA SIGUT LA MA GUANYADORA I QUI HA GUANYAT

# PLAYER GAME RESULT
# ID: game_result
# ['3','20000'] POSICIO FINAL A LA PARTIDA I PASTA GUANYADA
# ['final_result', 'winnings']

# RECEIVE

# DISCONNECT
# ID: disconnect

# PLAYER DECISION REPLY
# ID: player_reply
# ['511'] (FOLD) ENVIAHO AMB player_action_id_b_cmd DE SYSTEM TOOL
# ['512','300'] RAISE PORTA DARRERE LA QUANTITAT QUE S'HA APOSTAT
# ['player_decision']
