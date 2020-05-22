import threading
import socket
import json
import time

from system_tool import server_host as host
from system_tool import server_port as port

from system_tool import conn_id_cmd as conn_id
from system_tool import client_id_cmd as client_id
from system_tool import update_id_h_cmd as update_id
from system_tool import player_state_id_h_cmd as player_state_id

from game_view import Game_View


class Client_Player(object):

    def __init__(self, username: str, game_id: int, game: Game_View):

        self.username = username

        self.game_id = game_id
        self.game = game
        self.table_id = 'not_set'
        self.table_seat = -1

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = host
        self.server_port = port

        self.connected = False

        self.connect_game()

    # Connection Management

    def connect_game(self):

        request = []
        request.append(client_id['player'])
        request.append(self.game_id)
        request.append(self.username)

        self.s.connect((self.server_host, self.server_port))

        self.send(request)

        response = self.receive()

        if type(response) == int and response == conn_id['success']:
            self.connected = True
            # INITIALIZE GAME VIEW

        threading.Thread(target=self.player_input_thread).start()
        threading.Thread(target=self.player_output_thread).start()

    def disconnect_game(self):

        self.send(conn_id['disconnect'])
        self.connected = False

    # Client To Server Connection Thread

    def player_input_thread(self):

        while not self.game.player_reply:
            pass

        print('PLAYER GAME VIEW INPUT')
        print(self.game.player_reply)

        if self.game.player_reply[0] == conn_id['disconnect']:
            self.disconnect_game()

        elif self.game.player_reply[0] == player_state_id['player_reply']:
            self.send(self.game.player_reply)

        self.game.player_reply.clear()

    # Server To Client Connection Thread

    def player_output_thread(self):

        while self.connected:

            rx_data = self.receive()

            print('PLAYER RECEIVED FROM SERVER: ')
            print(rx_data)
            if (type(rx_data) == int) and (rx_data == player_state_id['player_request']):
                self.game.isYourTourn()

            elif rx_data[0] == update_id['game_update']:
                self.game.update(rx_data)

            elif rx_data[0] == update_id['game_result']:
                self.game.playerGameResult(rx_data)

            elif rx_data[0] == update_id['round_result']:
                self.game.roundResultUpdate(rx_data)

    # Data Transfer Management

    def send(self, data: []):

        self.s.send(json.dumps(data).encode())

    def receive(self):
        data = self.s.recv(4096).decode()
        print('RECEIVED DATA: ' + data)
        return json.loads(data)
