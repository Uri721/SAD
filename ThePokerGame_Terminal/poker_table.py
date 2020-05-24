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

    def __init__(self, blind: int):

        self.limit = 10

        self.blind = blind
        # self.inc_blind_rate = inc_blind_rate

        self.deck = Deck()
        self.community_cards = [None, None, None, None, None]

        self.players = [None for _ in range(self.limit)]
        self.rounds = []

        self.game_players = 0
        self.in_game_players = 0

        self.pot = 0
        self.highest_bet = 0

        self.dealer = 0
        self.target = -1

        self.state = 0
        self.all_in_table = False

    def __str__(self):

        return ('SMALL BLIND: ' + str(self.blind)+' COMMUNITY CARDS: '+str(self.community_cards)+' PLAYERS: '+str(self.players)+' GAME PLAYERS: '+str(self.game_players)+' IN GAME PLAYERS: '+str(self.in_game_players)+' POT: '+str(self.pot)+' HIGHEST BET: '+str(self.highest_bet)+' DEALER: '+str(self.dealer)+' TARGET: '+str(self.target)+' STATE: '+str(self.state))

    def start_game(self):

        threading.Thread(target=self.game_state_control).start()
        threading.Thread(target=self.players_state_control).start()

    # Game State Management

    def game_state_control(self):

        print('TABLE STARTS')

        while self.state != game_state_id['terminated']:

            self.deck = Deck()
            self.deck.shuffle()

            self.state = game_state_id['pre_flop']

            self.community_cards = [None, None, None, None, None]

            for player in self.players:
                if player is not None:
                    player.state = player_state['in_game']

            self.in_game_players = self.game_players
            self.all_in_players = 0
            self.all_in_table = False

            self.dealer = self.next_player_position(self.dealer)
            self.target = -1

            self.blinds()

            while self.state != game_state_id['showdown']:

                print('1.' + str(self))
                self.deal_cards()
                print('2.' + str(self))
                self.betting_round()
                print('3.' + str(self))
                self.update_state()
                print('4.' + str(self))

            self.showdown()
            self.update_state()

        print('TABLE FINISHED')

    # Player State Management

    def players_state_control(self):

        while self.state != game_state_id['terminated']:

            for player in self.players:
                if (player is not None) and (not player.connected):
                    self.disconnect_player(player)
                time.sleep(5)

    def add_player(self, player: Server_Player):

        if self.game_players < self.limit:

            print(str(self.game_players) + ' Player Added : ' + player.name)

            self.players[self.players.index(None)] = player
            self.game_players += 1
            player.table_position = (self.players.index(player) + 1)
            return True

        else:

            print('Full Table Entry Denied : ' + player.name)
            return False

    def disconnect_player(self, player: Server_Player):

        if player.connected:
            if self.game_players == 1:
                player.send([update_id['game_result'],
                             (self.game_players), 5000])
                time.sleep(0.25)
            else:
                player.send([update_id['game_result'], (self.game_players), 0])
                time.sleep(0.25)

        if player.state != player_state['out_game']:
            self.in_game_players -= 1

        self.players[self.players.index(player)] = None
        self.game_players -= 1

    # Game Properties Control Functions

    def blinds(self):

        small_blind = self.next_player_position(self.dealer)

        self.players[small_blind].update_stack(self.blind, False)
        self.pot += self.blind

        big_blind = self.next_player_position(small_blind)

        self.players[big_blind].update_stack(self.blind * 2, False)
        self.pot += self.blind * 2

        self.highest_bet = self.blind * 2

        self.update_players_view()
        time.sleep(3)

    def deal_cards(self):

        if self.state == game_state_id['pre_flop']:

            self.update_target('round_start')

            for _ in range(self.in_game_players):
                self.players[self.target].update_cards(self.deck.deal(2))
                self.update_target('increment')

        elif self.state == game_state_id['flop']:

            self.deck.deal(1)
            self.community_cards[0:3] = self.deck.deal(3)

        elif self.state == game_state_id['river']:

            self.deck.deal(1)
            self.community_cards[3] = self.deck.deal(1)

        elif self.state == game_state_id['turn']:

            self.deck.deal(1)
            self.community_cards[4] = self.deck.deal(1)

        self.target = -1
        self.update_players_view()
        time.sleep(5)

    def betting_round(self):

        self.update_target('betting_round_start')

        to_talk_players = self.in_game_players

        while not self.all_in_table and self.in_game_players > 1:

            if to_talk_players == 0:
                break

            time.sleep(0.5)
            decision = self.players[self.target].make_move()

            if type(decision) is int:

                self.pot += decision
                self.players[self.target].update_stack(decision, False)
                self.update_all_in_table()
                self.highest_bet = self.players[self.target].bet
                to_talk_players = self.in_game_players - 1

                print(self.players[self.target].name +
                      ' raised ' + str(decision))

            else:

                if decision == player_action_id['call']:

                    aux = (self.highest_bet - self.players[self.target].bet)
                    self.pot += aux
                    self.players[self.target].update_stack(aux, False)
                    self.update_all_in_table()

                    print(self.players[self.target].name +
                          ' called ' + str(decision))

                elif decision == player_action_id['fold']:

                    self.players[self.target].state = player_state['out_game']
                    self.in_game_players -= 1

                    print(self.players[self.target].name +
                          ' folded ')

                to_talk_players -= 1

                print(to_talk_players)

            time.sleep(2.5)
            self.update_target('increment')
            self.update_players_view()
            time.sleep(5)

        for player in self.players:
            if player is not None:
                player.bet = 0

        self.update_players_view()
        time.sleep(4)

    def showdown(self):

        self.target = -1
        hand_result = -1

        if self.in_game_players > 1:

            usernames = []
            cards = []

            for player in self.players:
                if player is not None and player.state != player_state['out_game']:
                    player.state = player_state['showdown']
                    usernames += [player.name]
                    cards += [player.cards[0].formatted() + ' ' + player.cards[1].formatted() + ' ' + self.community_cards[0].formatted() +
                              ' ' + self.community_cards[1].formatted() + ' ' + self.community_cards[2].formatted()]

            print()
            print('CARTES')
            print(cards)
            print(type(cards))
            print('USERNAMES')
            print(usernames)
            print(type(usernames))

            hand_result, winners = finish_round(usernames, cards)

        else:

            for player in self.players:
                if player is not None and player.state == player_state['in_game']:
                    winners = [player.name]
                    break

        self.update_players_view()
        time.sleep(7.5)

        if len(winners) > 1:
            for player in self.players:
                if player is not None and player.name in winners:
                    player.update_stack((self.pot/len(winners)), True)

            self.pot = 0

        else:
            for player in self.players:
                if player is not None and player.name == winners[0]:
                    player.update_stack(self.pot, True)
                    self.pot = 0
                    break

        self.update_round_result(hand_result, winners)
        time.sleep(7.5)

        for player in self.players:
            if player is not None and player.stack < self.blind:
                self.disconnect_player(player)

        self.community_cards = [None, None, None, None, None]
        self.update_players_view()
        time.sleep(4)

    # Game Parameters Management

    def update_state(self):

        if self.game_players < 2:
            for player in self.players:
                if player is not None:
                    self.disconnect_player(player)
            self.state == game_state_id['terminated']
            return

        elif self.in_game_players > 2:
            self.state = game_state_id['showdown']
            return

        elif self.state == game_state_id['showdown']:
            self.state = game_state_id['pre_flop']

        else:
            self.state += 1

    def update_all_in_table(self):

        if self.players[self.target].stack == 0:

            self.players[self.target].state = player_state['all_in']
            self.all_in_players += 1

            if self.all_in_players == self.in_game_players:
                for player in self.players:
                    if player is not None and player.state == player_state['all_in']:
                        player.state = player_state['showdown']
                self.all_in_table = True

    def update_target(self, cmd: str):

        if cmd == 'round_start':
            self.target = self.next_player_position(self.dealer)

        elif cmd == 'increment' and not self.all_in_table:
            self.target = self.next_player_position(self.target)

        elif cmd == 'betting_round_start' and not self.all_in_table:

            if self.state == game_state_id['pre_flop']:
                self.target = self.next_player_position(self.dealer)
                self.target = self.next_player_position(self.target)
                self.target = self.next_player_position(self.target)

            else:
                self.target = self.next_player_position(self.dealer)

        print(type(self.target))
        print(cmd + ' TARGET: ' + str(self.target))

    def next_player_position(self, target: int):

        for _ in range(self.limit):
            target = ((target + 1) % self.limit)
            if (self.players[target] is not None) and (self.players[target].state == player_state['in_game']):
                return target

    # Game View Update

    def update_players_view(self):

        print('UPDATE PLAYERS VIEW')

        dealer_aux = self.dealer + 1
        target_aux = self.target + 1

        tx_data = [update_id['game_update']]
        tx_data += [self.pot, self.blind, self.highest_bet,
                    dealer_aux, target_aux]

        tx_data += dts

        for player in self.players:
            if player is not None:

                print(player.name + ' state is ' + str(player.state))

                tx_data += [player.name, player.table_position, player.bet,
                            player.stack]

                if player.state == player_state['in_game'] or player.state == player_state['all_in']:
                    print(player.name + ' state 0')
                    tx_data += [0, 0]
                elif player.state == player_state['out_game']:
                    print(player.name + ' state -1')
                    tx_data += [-1, -1]
                elif player.state == player_state['showdown']:
                    print(player.name + ' state 1')
                    tx_data += [player.cards[0].to_transmit(),
                                player.cards[1].to_transmit()]

        tx_data += dts

        for card in self.community_cards:
            if card is None:
                tx_data += [0]
            else:
                tx_data += [card.to_transmit()]

        for player in self.players:
            if player is not None:

                if (player.state == player_state['in_game'] or player.state == player_state['all_in']) and player.cards[0] is not None:
                    tx_data[tx_data.index(player.name) +
                            4] = player.cards[0].to_transmit()
                    tx_data[tx_data.index(player.name) +
                            5] = player.cards[1].to_transmit()
                    print('TX TO ' + player.name + ' : ')
                    print(tx_data)
                    player.send(tx_data)
                    if player.state == player_state['in_game'] or player.state == player_state['all_in']:
                        tx_data[tx_data.index(player.name) + 4] = 0
                        tx_data[tx_data.index(player.name) + 5] = 0
                    else:
                        tx_data[tx_data.index(player.name) + 4] = -1
                        tx_data[tx_data.index(player.name) + 5] = -1
                else:
                    print('TX TO ' + player.name + ' : ')
                    print(tx_data)
                    player.send(tx_data)

    # Round Result Update

    def update_round_result(self, hand_result: int, winners: []):

        tx_data = [update_id['round_result']]
        tx_data += [hand_result]
        tx_data += winners

        for player in self.players:
            if player is not None:
                print('TX TO ' + player.name + ' : ')
                print(tx_data)
                player.send(tx_data)
