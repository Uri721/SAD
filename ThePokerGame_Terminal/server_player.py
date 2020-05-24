import threading
import socket
import json
import time

from datetime import datetime

from system_tool import conn_id_cmd as conn_id
from system_tool import player_state_id_h_cmd as player_st_id_h
from system_tool import player_action_id_b_cmd as player_action_id

from poker_tool import player_state


class Server_Player(object):

    def __init__(self, name: str, stack: int, connection: socket, address: str):

        self.name = name
        self.stack = stack

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

        print(self.name + ' disconnected')

    def make_move(self):

        print('ESPERANT RESPOSTA DE ' + self.name)
        self.send(player_st_id_h['player_request'])

        _ = (datetime.timestamp(datetime.now()) + 40)

        while (self.player_reply is None) and (datetime.timestamp(datetime.now()) < _):
            pass

        if self.player_reply is None:
            print('NO HA REBUT RESPOSTA, TEMPS EXPIRAT, FOLD')
            return [player_action_id['fold']]

        else:

            _ = self.player_reply[1]
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

        self.connection.send(json.dumps(data).encode())
        time.sleep(0.1)

    def receive(self):

        return json.loads(self.connection.recv(4096).decode())
