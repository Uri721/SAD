import threading
import socket
import json
import time

from datetime import datetime

from system_tool import conn_id_cmd as conn_id
from system_tool import player_state_id_h_cmd as player_st_id_h
from system_tool import player_action_id_b_cmd as player_action_id

from poker_tool import player_state

from server_user import Server_User


class Server_Player(object):

    def __init__(self, user: Server_User, stack: int, connection: socket, address: str):

        self.user = user

        self.name = user.username
        self.stack = stack

        self.user.update_account_balance(self.stack, False)

        self.connection = connection
        self.address = address

        self.connected = True
        self.state = player_state['out_game']

        self.bet = 0
        self.table_position = -1
        self.cards = [None, None]

        self.player_reply = None

        threading.Thread(target=self.player_input_thread).start()

    # Client to Server Connection Thread

    def player_input_thread(self):

        while self.connected:

            rx_data = self.receive()

            if type(rx_data) == int and rx_data == conn_id['disconnect']:

                self.connected = False

            elif rx_data[0] == player_st_id_h['player_reply']:

                self.player_reply = rx_data

        self.user.update_account_balance(self.stack, True)

    def decide(self):

        print('ESPERANT RESPOSTA DE ' + self.name)
        self.send(player_st_id_h['player_request'])
        print('REQUEST ENVIADA')
        _ = (datetime.timestamp(datetime.now()) + 40000)

        while (self.player_reply is None) and (datetime.timestamp(datetime.now()) < _):
            print('WAITIGN PLAYER REPLY: ')
            print(self.player_reply)
            time.sleep(2)

        if self.player_reply is None:
            print('NO HA REBUT RESPOSTA, TEMPS EXPIRAT, FOLD')
            return [player_action_id['fold']]

        else:

            _ = []
            print('HA REBUT RESPOSTA:')
            print(self.player_reply)
            if len(self.player_reply) > 2:
                _ += [int(self.player_reply[1])]
                _ += [int(self.player_reply[2])]

            else:
                _ += [int(self.player_reply[1])]

            self.player_reply = None

            return _

    # Player Properties Management

    def update_cards(self, cards: []):

        self.cards.clear()
        self.cards = cards

    def update_stack(self, amount: int, increase: bool):

        if increase:
            self.stack = self.stack + amount
        else:
            self.stack = self.stack - amount
            self.bet = self.bet + amount

    # Data Transfer Management

    def send(self, data: []):

        time.sleep(2)

        print('SERVER TO ' + self.name)
        print(data)

        self.connection.send(json.dumps(data).encode())
        time.sleep(0.1)

    def receive(self):

        return json.loads(self.connection.recv(4096).decode())
