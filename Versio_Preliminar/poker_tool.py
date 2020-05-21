from system_tool import game_mode_id_b_cmd as game_mode

from hand_rank import rank

from random import shuffle

card_suits = {1: '♦', 2: '♠', 3: '♥', 4: '♣'}

card_ranks = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8',
              9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

player_state = {'out_game': -1, 'in_game': 0, 'showdown': 1}


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

        aux = []

        for i in range(n):
            aux.append(self.cards[len(self.cards) - 1])
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

    def finish_round(self, in_game_players: [], community_cards: [], pot: int):

        usernames = []
        hands = []

        for player in in_game_players:
            usernames.append(player.user.username)
            hands.append(player.cards[0].formatted() + ' ' + player.cards[1].formatted() + ' ' +
                         community_cards[0].formatted() + ' ' + community_cards[1].formatted() + ' ' + community_cards[2].formatted())

        value = []
        tie_breaker = []

        for cards in hands:
            r = rank(cards)
            value.append(r[0])
            tie_breaker.append(r[1])

        if value.count(max(value)) == 1:

            winner = usernames[value.index(max(value))]

            for player in in_game_players:
                if player.user.username == winner:
                    self.update_player(winner, self.format_player(
                        winner, player.stack, player.current_bet, 'W', player.cards))
                else:
                    self.update_player(player.user.username, self.format_player(
                        player.user.username, player.stack, player.current_bet, 'L', player.cards))

            self.complete_round(community_cards, pot)
            return winner

        # else:

            #tied_players = []

            # for v in value:
            # if v is max(value):
            # tied_players.append(value.index(v))

            #i = 1
            # while i < len(tied_players):


def small_blind(mode: int, entry_amount: int):

    if mode == game_mode['sit_and_go']:
        return (entry_amount/20)

    elif mode == game_mode['tournament']:
        return (entry_amount/25)

    elif mode == game_mode['cash_game']:
        return (entry_amount/20)


"""
poket1 = [Card(0, 14), Card(1, 14)]
poket2 = [Card(3, 14), Card(2, 14)]
poket3 = [Card(3, 2), Card(2, 3)]
comm = [Card(0, 13), Card(0, 3), Card(3, 3)]

hands = []

hands.append(poket3[0].formatted() + ' ' + poket3[1].formatted() + ' ' +
             comm[0].formatted() + ' ' + comm[1].formatted() + ' ' + comm[2].formatted())
hands.append(poket1[0].formatted() + ' ' + poket1[1].formatted() + ' ' +
             comm[0].formatted() + ' ' + comm[1].formatted() + ' ' + comm[2].formatted())
hands.append(poket2[0].formatted() + ' ' + poket2[1].formatted() + ' ' +
             comm[0].formatted() + ' ' + comm[1].formatted() + ' ' + comm[2].formatted())

c = []
tie_br = []

print("%-18s %-15s %s" % ("HAND", "CATEGORY", "TIE-BREAKER"))
for cards in hands:
    (category, tie_breaker) = rank(cards)
    print("%-18r %-15s %r" % (cards, str(category), tie_breaker))
    c.append(category)
    tie_br.append(tie_breaker)


print(c.count(min(c)))

string = ['sr', 'sg'] + str

print(string)


class One(object):

    def __init__(self):
        self.input = []

    def update(self, data: []):
        self.input = data


class Two(object):

    def __init(self):
        self.input = []

    def update_input(self, data: []):
        self.input = data


one = One()
two = Two()

two.update_input(['hola', 'que', 'tal'])
one.update(two.input)
print(one.input)
print(id(two.input))
print(id(one.input))

x = ['hola']

print(not x)
x.clear()
print(not x)

"""
l = [str(Card(1, 5)), str(Card(3, 4)), None, str(Card(1, 14))]
print(l)
