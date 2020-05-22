import socket
import json
import time


class Server_User(object):

    def __init__(self, username: str, account_balance: int, connection: socket, address: str):

        self.username = username
        self.account_balance = account_balance
        # admin
        self.connection = connection
        self.address = address

        self.connected = True

    # User Properties Management

    def update_account_balance(self, amount: int, increase: bool):

        if increase:
            self.account_balance += amount

        else:
            self.account_balance = self.account_balance - amount

    # Data Transfer Management

    def send(self, data: []):

        self.connection.send(json.dumps(data).encode())
        time.sleep(0.1)

    def receive(self):

        return json.loads(self.connection.recv(4096).decode())
