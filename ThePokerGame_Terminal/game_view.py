import sys
from system_tool import player_action_id_b_cmd as player_action
from system_tool import player_state_id_h_cmd as player_state_id
from system_tool import conn_id_cmd as conn_id
import time
import atexit
import signal
from sys import exit


class Game_View(object):
    def handler(self, signal_received, frame):
        self.player_reply = [conn_id['disconnect']]
        print('DISCONNECTING')
        time.sleep(1)
        exit(0)

    def __init__(self, name):
        self.player_reply = []
        self.player_name = name
        self.pot = -1
        self.small_blind = -1
        self.dealer_position = -1
        self.target_position = -1
        self.players = []
        self.cardsTable = []
        self.highestBet = 0
        self.cardsPlayers = []

        self.highestBet_before = -1
        self.pot_before = -1
        self.small_blind_before = -1
        self.dealer_position_before = -1
        self.target_position_before = -1
        self.players_before = []
        self.cardsTable_before = []
        self.cardsPlayers_before = []

        self.updated = False
        self.started = False
        self.endPlayer = False

        self.yourTourn = False
        self.showCall = False
        self.updd = []
        self.upd_before = []

        signal.signal(signal.SIGTSTP, self.handler)  # disconnect with ctrl z

    def update(self, updat):
        upd = []
        it = 0
        for i in updat:
            if not it == 0:
                upd.append(i)
            it += 1
        self.busy = True
        self.updated = False
        self.positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.pot_before = self.pot
        self.small_blind_before = self.small_blind
        self.dealer_position_before = self.dealer_position
        self.target_position_before = self.target_position
        self.players_before = self.players
        self.highestBet_before = self.highestBet
        self.cardsTable_before = self.cardsTable
        self.cardsPlayers_before = self.cardsPlayers
        self.upd_before = self.updd
        self.updd = upd

        self.pot = -1
        self.highestBet = -1
        self.small_blind = -1
        self.dealer_position = -1
        self.target_position = -1
        self.players = []
        self.cardsTable = []

        self.showCall = False
        self.pot = upd[0]
        self.small_blind = upd[1]
        self.highestBet = upd[2]
        self.dealer_position = upd[3]
        self.target_position = upd[4]
        player = []
        c = 0
        a = 0
        b = 0
        for i in upd:
            if i == "$":
                a += 1
            else:
                if c >= 5:
                    if a == 1:
                        if b < 6:
                            player.append(i)
                            b += 1

                        if b == 6:
                            self.players.append(player)
                            player = []
                            b = 0
                    if a == 2:
                        self.cardsTable.append(i)

            c += 1

        mevaposicio = -1
        mev = 1
        for i in self.players:
            if i[0] == self.player_name:
                mevaposicio = mev
            mev += 1

        if int(self.players[mevaposicio-1][2]) < int(self.highestBet):
            self.showCall = True

        if not self.pot_before == self.pot:
            self.updated = True
        if not self.small_blind_before == self.small_blind:
            self.updated = True
        if not self.dealer_position_before == self.dealer_position:
            self.updated = True
        if not self.target_position_before == self.target_position:
            self.updated = True
        if not self.players_before == self.players:
            self.updated = True
        if not self.cardsTable_before == self.cardsTable:
            self.updated = True
        if not self.highestBet_before == self.highestBet:
            self.updated = True
        if not self.upd_before == self.updd:
            self.updateGameview()

    def updateGameview(self):
        if self.updated == True:
            for i in range(10):
                print("")

            print("YOU ARE "+str(self.player_name))
            print("")
            print("///////////////////////////")
            # update pot
            print("")
            print("POT: "+str(self.pot))

            # update smallblind
            print("SMALL BLIND: "+str(self.small_blind))

            # update dealerposition
            dealer = 0
            for i in self.players:
                if i[1] == self.dealer_position:
                    dealer = i[0]
            print("DEALER: "+str(dealer))
            print("")
            # update player
            players_ordenats = [[], [], [], [], [], [], [], [], [], []]
            for i in self.players:
                players_ordenats[int(i[1])] = i

            retired = False
            print("USERS: ")

            print("---------------------------")
            for i in players_ordenats:
                if not i == []:
                    if int(i[4]) == -1:
                        retired = True
                        i[4] = 0
                    elif int(i[5]) == -1:
                        retired = True
                        i[5] = 0
                    if retired == True:
                        print("NAME: "+str(i[0])+" --> Retired")
                    else:
                        print("NAME: "+str(i[0]))
                    retired = False
                    print("Bet: "+str(i[2]))
                    print("Stack: "+str(i[3]))
                    print(
                        "Cards: "+self.printCards(i[4])+"  "+self.printCards(i[5]))

                    print("---------------------------")

            players_ordenats = [[], [], [], [], [], [], [], [], [], []]

            # update tableCards
            print("")
            print("TABLE CARDS: ")
            print(self.printCards(self.cardsTable[0])+"  "+self.printCards(self.cardsTable[1])+"  "+self.printCards(
                self.cardsTable[2])+"  "+self.printCards(self.cardsTable[3])+"  "+self.printCards(self.cardsTable[4]))

            # update Tourn
            tourn = 0
            for i in self.players:
                if i[1] == self.target_position:
                    tourn = i[0]
            print("TOURN: "+str(tourn))
            print("")
            print("///////////////////////////")
            print("")
            self.updated = False

    def playerGameResult(self, playerresult):
        if not playerresult == 'null':
            pr = []
            it = 0
            for i in playerresult:
                if not it == 0:
                    pr.append(i)
                it += 1
            posiciofinal = pr[0]
            winnings = pr[1]
            print("")
            print("***************************")
            print("***************************")
            print("PLAYER GAME RESULT:")
            print("Position: "+str(posiciofinal))
            print("Winnings: "+str(winnings))
            print("***************************")
            print("***************************")
            print("")
            exit(0)

    def roundResultUpdate(self, roundresult):
        if not roundresult == 'null':
            rr = []
            it = 0
            maguanyadora = roundresult[1]
            for i in roundresult:
                if not it <= 1:
                    rr.append(i)
                it += 1
            print("")

            print("***************************")
            print("***************************")
            print("ROUND RESULT:")
            print("Winner: "+str(rr))

            if not maguanyadora == -1:
                print("Winning Hand: "+str(maguanyadora))
            print("***************************")
            print("***************************")
            print("")

    def isYourTourn(self):

        print("")
        print("Enter your move:")
        if self.showCall == True:
            print(
                "f to Fold    ch to Check   c to Call   bet Raise amount [ex:100]")
        else:
            print("f to Fold    ch to Check   number to Raise that number")

        inp = input()

        if inp == "ch":
            self.player_reply = [
                player_state_id['player_reply'], "ch"]
        elif inp == "f":
            self.player_reply = [
                player_state_id['player_reply'], "f"]
        elif inp == "c":
            self.player_reply = [
                player_state_id['player_reply'], "c"]
        else:
            self.player_reply = [player_state_id['player_reply'],
                                 int(inp)]
        print(self.player_reply)

    def printCards(self, card):
        if not int(card) == 0:

            suit = int(card)//100
            rank = int(card)-suit*100
            if suit == 0:
                suit = int(card)//10
                rank = int(card)-suit*10

            rank_string = ""
            suit_string = ""
            if rank == 2:
                rank_string = "Two"
            if rank == 3:
                rank_string = "Three"
            if rank == 4:
                rank_string = "Four"
            if rank == 5:
                rank_string = "Five"
            if rank == 6:
                rank_string = "Six"
            if rank == 7:
                rank_string = "Seven"
            if rank == 8:
                rank_string = "Eight"
            if rank == 9:
                rank_string = "Nine"
            if rank == 10:
                rank_string = "Ten"
            if rank == 11:
                rank_string = "Jack"
            if rank == 12:
                rank_string = "Queen"
            if rank == 13:
                rank_string = "King"
            if rank == 14:
                rank_string = "Ace"

            if suit == 1:
                suit_string = "Diamonds"
            if suit == 2:
                suit_string = "Spades"
            if suit == 3:
                suit_string = "Hearts"
            if suit == 4:
                suit_string = "Clubs"

            if not rank_string == "":
                path = "["+rank_string+" of "+suit_string+"]"
            else:
                path = "[*]"
        else:
            path = "[*]"
        return path

# GAME=Game_View("jugador1")
#GAME.update(['id','500','80','40', '3', '2', '$','jugador2', '2','10', '10', '-1','-1','jugador3', '3','10', '10', '0','0','jugador1', '1','10', '10', '13','410', '$', '0','0', '0', '0', '0'])
#           id pot  blind  highest dealer targ
