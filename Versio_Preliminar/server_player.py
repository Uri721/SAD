import threading
import socket
import json
import time

from system_tool import conn_id_cmd as conn_id
from system_tool import player_state_id_h_cmd as player_st_id_h

from server_user import Server_User


class Server_Player(object):

    def __init__(self, user: Server_User, stack: int, connection: socket, address: str):

        self.user = user
        self.stack = stack

        self.user.update_account_balance(self.stack, False)

        self.connection = connection
        self.address = address

        self.connected = True
        self.in_game = False

        self.current_bet = 0
        self.cards = []

        self.player_reply = 'not_set'

        threading.Thread(target=self.player_input_thread).start()

    # Client to Server Connection Thread

    def player_input_thread(self):

        while self.connected:

            rx_data = self.receive()

            if type(rx_data) == int and rx_data == conn_id['disconnect']:

                self.connected = False

            elif rx_data[0] == player_st_id_h['player_reply']:

                self.player_reply = rx_data[1]

        self.user.update_account_balance(self.stack, True)

    #
    def player_decision(self):

        while self.player_reply == 'not_set':
            pass

        _ = self.player_reply

        self.player_reply = 'not_set'

        return _

    # Player Properties Management

    def update_cards(self, cards: []):

        self.cards.clear()
        self.cards[0:1] = cards

    def update_stack(self, amount: int, increase: bool):

        if increase:
            self.stack += amount
        else:
            self.stack -= amount
            self.current_bet += amount

    # Data Transfer Management

    def send(self, data: []):

        self.connection.send(json.dumps(data).encode())
        time.sleep(0.1)

    def receive(self):

        return json.loads(self.connection.recv(4096).decode())
