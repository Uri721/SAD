import socket
import json
import time
import threading

from system_tool import server_host as host
from system_tool import server_port as port

from system_tool import conn_id_cmd as conn_id
from system_tool import client_id_cmd as client_id

from system_tool import validate_user
from system_tool import update_account_balance

from server_player import Server_Player

from poker_game import Poker_Game


class Server(object):

    def __init__(self):

        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = host
        self.server_port = port

        threading.Thread(target=self.connection_thread).start()

        self.server_game = Poker_Game()
        self.server_game.start_game()

    # Server Connection Thread

    def connection_thread(self):

        self.ss.bind((self.server_host, self.server_port))
        self.ss.listen()

        print('-' * 5 + " Server Initialized " + 5 * '-')

        while True:

            connection, address = self.ss.accept()
            request = json.loads(connection.recv(1024).decode())

            if type(request) == int and request == client_id['player']:
                if self.server_game.table.game_players < self.server_game.players_limit:
                    self.authenticate(connection, address)

    # User Authentication Management

    def authenticate(self, connection: socket, address: str):

        account_balance = -1

        while account_balance == -1:

            rx_data = json.loads(connection.recv(2048).decode())

            account_balance = validate_user(rx_data[0], rx_data[1])

            connection.send(json.dumps(account_balance).encode())
            time.sleep(0.1)

        print('-- ' + rx_data[0] + ' Authenticated --')

        player = Server_Player(rx_data[0], 2000, connection, address)
        self.server_game.add_player(player)


if __name__ == '__main__':
    Server()
