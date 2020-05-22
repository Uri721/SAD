import threading
import socket
import json
import time

from system_tool import server_host as host
from system_tool import server_port as port

from system_tool import conn_id_cmd as conn_id
from system_tool import client_id_cmd as client_id
from system_tool import lobby_id_h_cmd as lobby_id_h

from client_player import Client_Player

from access_view import Access_View
from lobby_view import Lobby_View

import datetime


class Client_User(object):

    def __init__(self):

        self.username = 'not_set'

        self.password = 'not_set'
        self.account_balance = -1

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = host
        self.server_port = port

        self.connected = False

        self.client_games = []

        self.connect_lobby()

    # Connection Management

    def connect_lobby(self):

        self.s.connect((self.server_host, self.server_port))
        self.s.send(json.dumps(client_id['user']).encode())

        self.authenticate_connection()

        threading.Thread(target=self.user_input_thread).start()
        threading.Thread(target=self.user_output_thread).start()

        self.lobby = Lobby_View(self.username)
        self.lobby.lobbyView()

    def disconnect_lobby(self):

        self.send(conn_id['disconnect'])
        self.connected = False

        print('-' * 5 + ' Disconnected ' + 5 * '-')

    def authenticate_connection(self):

        while not self.connected:

            data = Access_View().execute()

            self.username = data[0]
            self.password = data[1]

            self.send(data)

            data = self.receive()
            print(int(data))
            self.account_balance = int(data)

            if self.account_balance != -1:
                self.connected = True

        print('-- ' + self.username + ' Authenticated --')

    # Client To Server Connection Thread

    def user_input_thread(self):

        time.sleep(0.25)

        while self.connected:

            while not self.lobby.user_input:
                pass
            print('USER LOBBY VIEW INPUT: ')
            print(self.lobby.user_input)
            if self.lobby.user_input[0] == conn_id['disconnect']:
                self.disconnect_lobby()

            elif self.lobby.user_input[0] == lobby_id_h['create_game']:
                self.send(self.lobby.user_input)

            elif self.lobby.user_input[0] == lobby_id_h['join_game']:
                print(self.lobby)
                time.sleep(2)
                Client_Player(
                    self.username, self.lobby.user_input[1], self.lobby.GAME)

            self.lobby.user_input.clear()

    # Server To Client Connection Thread os.getcwd()+'/Images/chips.png'

    def user_output_thread(self):

        time.sleep(0.25)

        while self.connected:
            _ = self.receive()
            print('RX SERVIDOR: ')
            print(_)
            self.lobby.update(_)

    # Data Transfer Management

    def send(self, data: []):

        self.s.send(json.dumps(data).encode())
        time.sleep(0.1)

    def receive(self):

        print('receiving')
        return json.loads(self.s.recv(4096).decode())


if __name__ == '__main__':
    Client_User()
