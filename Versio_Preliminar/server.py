import threading
import socket
import json
import time

from system_tool import system_users_file_path

from system_tool import data_transmission_separator as dts

from system_tool import server_host as host
from system_tool import server_port as port

from system_tool import conn_id_cmd as conn_id
from system_tool import client_id_cmd as client_id
from system_tool import lobby_id_h_cmd as lobby_id_h

from system_tool import validate_user
from system_tool import update_account_balance

from server_user import Server_User
from server_player import Server_Player

from poker_game import Poker_Game


class Server(object):

    def __init__(self):

        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = host
        self.server_port = port

        self.lobby_users = []
        self.lobby_games = []
        self.game_id_control = 0

        threading.Thread(target=self.connection_thread).start()

    # Server Connection Thread

    def connection_thread(self):

        self.ss.bind((self.server_host, self.server_port))

        self.ss.listen()

        print('-' * 5 + " Server Initialized " + 5 * '-')

        while True:

            connection, address = self.ss.accept()
            request = json.loads(connection.recv(1024).decode())
            print(request)

            if type(request) == int and request == client_id['user']:
                self.authenticate(connection, address)

            elif request[0] == client_id['player']:
                for game in self.lobby_games:
                    if int(request[1]) == game.id and game.not_full():
                        for user in self.lobby_users:
                            player = Server_Player(
                                user, game.entry_amount, connection, address)
                            game.add_player(player)

                        connection.send(json.dumps(
                            conn_id['success']).encode())

                    else:
                        connection.send(json.dumps(
                            conn_id['failure']).encode())

    # Client To Server User Input Thread

    def server_input_thread(self, user: Server_User):

        while user.connected:

            rx_data = user.receive()
            print(rx_data)

            if type(rx_data) == int and rx_data == conn_id['disconnect']:

                self.disconnect_user(user)
                user.connected = False

            elif rx_data[0] == lobby_id_h['create_game']:
                print(rx_data)
                self.lobby_games.append(Poker_Game(self.assign_id, rx_data))
                self.update_lobby_view()

        self.disconnect_user(user)

    # User Authentication Management

    def authenticate(self, connection: socket, address: str):

        account_balance = -1

        while account_balance == -1:

            rx_data = json.loads(connection.recv(2048).decode())

            account_balance = validate_user(rx_data[0], rx_data[1])

            connection.send(json.dumps(account_balance).encode())
            time.sleep(0.1)

        print('-- ' + rx_data[0] + ' Authenticated --')

        user = Server_User(rx_data[0], account_balance, connection, address)

        self.connect_user(user)

        threading.Thread(target=self.server_input_thread, args=(user,)).start()

    # Connect System User

    def connect_user(self, user: Server_User):

        self.lobby_users.append(user)
        self.update_lobby_view()

    # Disconnect System User

    def disconnect_user(self, user: Server_User):

        update_account_balance(user.username, user.account_balance)
        self.lobby_users.remove(user)
        self.update_lobby_view()

        print('-' * 5 + ' Disconnected ' + 5 * '-')

    # Games Management

    def initialize_game(self, game):

        self.lobby_games.append(game)
        threading.Thread(target=game.start_game).start()
        self.update_lobby_view()

    def finish_game(self, game):

        self.update_lobby_view()

    # Lobby View Update

    def update_lobby_view(self):

        system_users = []
        for user in self.lobby_users:
            system_users.append(user.username)

        system_games = []
        for game in self.lobby_games:
            system_games.append(
                (game.id, game.name, game.players, game.players_limit, game.start_time))

        lobby_view_update = []
        lobby_view_update = system_users + dts + system_games + dts

        time.sleep(0.1)
        print('lobby view update')
        for user in self.lobby_users:
            print(lobby_view_update + [str(user.account_balance)])
            user.send(lobby_view_update + [str(user.account_balance)])
        time.sleep(0.1)

    # Identification Management Tool

    def assign_id(self):

        self.game_id_control += 1
        return self.game_id_control


if __name__ == '__main__':
    Server()
