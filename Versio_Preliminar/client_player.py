import threading
import socket
import json
import time

from system_tool import server_host as host
from system_tool import server_port as port

from system_tool import conn_id_cmd as conn_id
from system_tool import client_id_cmd as client_id


class Client_Player(object):

    def __init__(self, username: str, game_id: int):

        self.username = username

        self.game_id = game_id
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
        pass

    # Client To Server Connection Thread

    def player_input_thread(self):
        # ESPERA A REBRE UNA INPUT UPDATE DE LA GAME VIEW
        # POT REBRE UNA DECISIO O UN DISCONNECT
        pass

    # Server To Client Connection Thread

    def player_output_thread(self):
        # ESCOLTA AL SERVER_PLAYER PER REBRE DECISION REQUEST O GAME VIEW UPDATE
        # FINALITZA QUAN CONNECTED = FALSE
        pass

    # Data Transfer Management

    def send(self, data: []):

        self.s.send(json.dumps(data).encode())
        time.sleep(0.1)

    def receive(self):

        return json.loads(self.s.recv(4096).decode())
