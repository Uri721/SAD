import os
from csv import writer
from csv import reader

system_users_file_path = os.getcwd() + '/SYSTEM_USERS.csv'

server_host = 'localhost'

server_port = 50000

data_transmission_separator = ['$']

conn_id_cmd = {'disconnect': -1, 'failure': 0, 'success': 1}

client_id_cmd = {'user': 100, 'player': 101}

update_id_h_cmd = {'lobby_update': 110, 'game_update': 111,
                   'game_result': 112, 'round_result': 113}

lobby_id_h_cmd = {'create_game': 120, 'join_game': 121}

player_state_id_h_cmd = {'player_request': 500,
                         'player_reply': 501, 'sit_out': 502}

player_action_id_b_cmd = {'check': 510, 'fold': 511, 'raise': 512, 'call': 513}

game_mode_id_b_cmd = {'cash_game': 520, 'sit_and_go': 521,
                      'sit_and_go_express': 522, 'tournament': 523}

game_state_id_b_cmd = {'pre_flop': 550, 'flop': 551,
                       'river': 552, 'turn': 553, 'showdown': 554, 'terminated': 555}

game_rank_id_b_cmd = {'high_card': 590, 'pair': 591, 'two_pair': 592, 'three_kind': 593, 'straight': 594,
                      'flush': 595, 'full_house': 596, 'poker': 597, 'straight_flush': 598, 'royal_flush': 599}

# System Users File Access Request Validation


def validate_user(username: str, password: str):

    with open(system_users_file_path, 'r') as csv_in:

        csv_reader = reader(csv_in)
        for row in csv_reader:
            if row[0] == username and row[1] == password:
                return row[2]
        else:
            return -1


# System Users File User Account Balance Update

def update_account_balance(username: str, account_balance: int):

    data = []

    with open(system_users_file_path, 'r') as csv_in:

        csv_reader = reader(csv_in)
        for row in csv_reader:
            if row[0] == username:
                row[2] = str(account_balance)
                data.append(row)
            else:
                data.append(row)

    with open(system_users_file_path, 'w') as csv_out:

        csv_writer = writer(csv_out)
        csv_writer.writerows(data)
