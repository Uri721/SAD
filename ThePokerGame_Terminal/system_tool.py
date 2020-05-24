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

player_action_id_b_cmd = {'check': 'ch',
                          'fold': 'f', 'raise': 512, 'call': 'c'}

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


# AUTHENTICATION COMMUNICATION PROTOCOL

    # SERVER TO CLIENT

    # CLIENT TO SERVER

# LOBBY COMMUNICATION PROTOCOL

    # SERVER TO CLIENT

        # LOBBY VIEW UPDATE [BROADCAST]

        # ID: lobby_update
        # [System Users Info, System Games Info, Client User Info]
        # ['system_user_username','$','system_game_id','system_game_name','system_game_players','system_game_players_limit','system_game_start_time','$','client_user_account_balance']

    # CLIENT TO SERVER

        # DISCONNECT

        # ID: disconnect

        # USER SYSTEM ACCESS

        # ID: user

        # PLAYER SYSTEM ACCESS

        # ID: player
        # [Info Game To Access, Info Player Name]
        # ['game_id', 'player_name']

        # USER GAME CREATION

        # ID: create_game
        # [Game Properties]
        # ['game_mode', 'game_name', 'players_limit', 'entry_amount', 'start_time_timestamp', 'blind', 'blind_ratio', 'rebuy']

# GAME COMMUNICATION PROTOCOL

    # SERVER TO CLIENT

        # GAME VIEW UPDATE [BROADCAST]

        # ID: game_update
        # [Info Table, Info Players, Community Cards]
        # ['pot','blind','highest_bet','dealer_position','target_position','$','player_name','player_position','playert_bet','player_stack','player_card_1','player_card_2','$','community_card_1','community_card_2','community_card_3','community_card_4','community_card_5']

        # target position -> [0 : No Target] [N : Target]
        # card -> [-1 : Player Folded] [0: Player In Game / Cards Face Down] [N: Player In Showdown / Cards Face Up]

        # ROUND RESULT UPDATE [BROADCAST]

        # ID: round_result
        # [Winning Hand Info, Winning Players Names]
        # ['winning_hand','player_name']

        # PLAYER GAME RESULT

        # ID: game_result
        # [Game Final Position, Game Prize]
        # ['final_result', 'winnings']

    # CLIENT TO SERVER

        # DISCONNECT

        # ID: disconnect

        # PLAYER DECISION REPLY

        # ID: player_reply
        # [Player Decision Command]
        # ['player_decision']
