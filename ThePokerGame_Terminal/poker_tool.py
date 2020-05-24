from system_tool import game_mode_id_b_cmd as game_mode

from hand_rank import rank

from random import shuffle

card_suits = {1: '♦', 2: '♠', 3: '♥', 4: '♣'}

card_ranks = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
              9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

hand_ranks = {0: 'high_card', 1: 'pair', 2: 'two_pair', 3: 'three_kind', 4: 'straight',
              5: 'flush', 6: 'full_house', 7: 'poker', 8: 'straight_flush'}

player_state = {'out_game': -1, 'in_game': 0, 'showdown': 1, 'all_in': 2}


class Deck(object):

    cards = []

    def __init__(self):

        self.cards.clear()
        for suit in card_suits:
            for rank in card_ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):

        shuffle(self.cards)

    def deal(self, n: int):

        if n == 1:
            aux = self.cards[-1]
            self.cards.remove(aux)
            return aux

        else:
            aux = []
            for i in range(n):
                aux.append(self.cards[-1])
                self.cards.remove(aux[i])

            return aux


class Card(object):

    def __init__(self, suit: int, rank: int):

        self.suit = suit
        self.rank = rank

    def __str__(self):

        return card_suits[self.suit] + card_ranks[self.rank]

    def formatted(self):

        return str(self.rank) + card_suits[self.suit]

    def to_transmit(self):

        return str(self.suit)+str(self.rank)


class Round_Result(object):

    def __init__(self, usernames: []):

        self.players_round = usernames

    def format_player(self, username: str, stack: int, current_bet: int, result: str, cards: []):

        return username + ',' + str(stack) + ',' + str(current_bet) + ',' + result + ',' + str(cards[0]) + ',' + str(cards[1])

    def update_player(self, username: str, player_round: str):

        for player_round in self.players_round:
            if player_round == username:
                player_round = player_round

    def add_player(self, username: str):

        self.players_round.append(username)

    def remove_player(self, username: str):

        self.players_round.remove(username)

    def complete_round(self, cards: [], pot: int):

        for player_round in self.players_round:
            player_round += (str(cards[0]) + str(cards[1]) +
                             str(cards[2]) + ',' + str(pot))

    def finish_round(self, usernames: [], cards: []):

        value = []
        tie_breaker = []

        for hand in cards:
            r = rank(hand)
            value.append(r[0])
            tie_breaker.append(r[1])

        if value.count(max(value)) == 1:

            winner = usernames[value.index(max(value))]
            winning_hand = hand_ranks[max(value)]
            # for player in in_game_players:
            #    if player.user.username == winner:
            #        self.update_player(winner, self.format_player(
            #            winner, player.stack, player.current_bet, 'W', player.cards))
            #    else:
            #        self.update_player(player.user.username, self.format_player(
            #            player.user.username, player.stack, player.current_bet, 'L', player.cards))

            # self.complete_round(community_cards, pot)
            return winner, winning_hand

        # else:

            # tied_players = []

            # for v in value:
            # if v is max(value):
            # tied_players.append(value.index(v))

            # i = 1
            # while i < len(tied_players):


def finish_round(usernames: [], cards: []):

    value = []
    tie_breaker = []

    for hand in cards:
        r = rank(hand)
        print(type(r))
        print('r[0] ' + str(r[0]))
        print(type(r[0]))
        print(type(r[1]))
        value += [r[0]]
        print(value)
        aux = [int(i) for i in r[1]]
        tie_breaker.append(sum(aux))

    if value.count(max(value)) == 1:

        winning_hand = hand_ranks[max(value)]
        winner = [usernames[value.index(max(value))]]

        return winning_hand, winner

    else:

        winners = []

        for i in range(len(value)):
            if value[i] == max(value):
                if tie_breaker[i] == max(tie_breaker):
                    winners += [usernames[i]]

        winning_hand = hand_ranks[max(value)]

        return winning_hand, winners


def small_blind(mode: int, entry_amount: int):

    if mode == game_mode['sit_and_go']:
        return (entry_amount/20)

    elif mode == game_mode['tournament']:
        return (entry_amount/25)

    elif mode == game_mode['cash_game']:
        return (entry_amount/20)


"""
usernames = ['uri', 'josep', 'pep', 'willy']

cards = [Card(2, 3).formatted() + ' ' + Card(2, 13).formatted() + ' ' + Card(4, 10).formatted() + ' ' + Card(2, 5).formatted() + ' ' + Card(2, 7).formatted(),
         Card(4, 12).formatted() + ' ' + Card(2, 14).formatted() + ' ' + Card(1,
                                                                              6).formatted() + ' ' + Card(2, 6).formatted() + ' ' + Card(4, 11).formatted(),
         Card(4, 10).formatted() + ' ' + Card(4, 7).formatted() + ' ' + Card(1,
                                                                             7).formatted() + ' ' + Card(3, 7).formatted() + ' ' + Card(2, 7).formatted(),
         Card(2, 2).formatted() + ' ' + Card(2, 10).formatted() + ' ' + Card(1, 2).formatted() + ' ' + Card(3, 9).formatted() + ' ' + Card(4, 10).formatted()]

winning_hand, winners = finish_round(usernames, cards)

print(winning_hand)
print(winners)
"""
