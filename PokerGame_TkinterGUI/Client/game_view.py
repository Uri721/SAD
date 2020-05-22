import os
import tkinter
from PIL import ImageTk, Image
from system_tool import player_action_id_b_cmd as player_action
from system_tool import player_state_id_h_cmd as player_state_id


class Game_View(tkinter.Frame):
    def __init__(self, parent, name):
        tkinter.Frame.__init__(self, parent)
        self.parentWindow = parent

        self.window = tkinter.Frame(self)
        self.window.pack()

        self.player_reply = []
        self.idpartida = 'null'
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

        self.inicipartida = 0
        self.positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.updated = False
        self.started = False
        self.endPlayer = False

        self.yourTourn = False
        self.showCall = False

        self.background = []
        self.imagesCardsPlayers = []
        self.imagesCardsTable = []
        self.labelsCardsPlayers = []
        self.labelsCardsTable = []

        self.updatecards = False
        self.updatesmallblind = False
        self.updatepot = False
        self.updatetablecards = False
        self.updatedealer = False
        self.updatecardsplayers = False

        for i in range(10):
            self.background.append('grey')

        self.gameView()

    def update(self, updat):
        print("UPDATE GAME VIEW")
        print(updat)
        self.idpartida = updat[0]
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

        self.pot = -1
        self.highestBet = -1
        self.small_blind = -1
        self.dealer_position = -1
        self.target_position = -1
        self.players = []
        self.cardsTable = []
        self.background = []
        for i in range(10):
            self.background.append('grey')

        self.pot = upd[0]
        self.small_blind = upd[1]
        self.highestBet = upd[2]
        self.dealer_position = upd[3]
        self.target_position = upd[4]
        player = []
        retirats = []
        c = 0
        a = 0
        b = 0
        rrr = False
        currentcards = []
        for i in upd:
            if i == "$":
                a += 1
            else:
                if c >= 5:
                    if a == 1:
                        if b == 4:
                            if i == "-1":
                                retirats.append(len(self.players))
                            elif i == "1":
                                rrr = True
                                currentcards.append(rrr)
                                rrr = False
                        if b < 7:
                            player.append(i)
                            b += 1
                        if b > 4:
                            currentcards.append(i)
                        if b == 7:
                            self.players.append(player)
                            self.cardsPlayers.append(currentcards)
                            currentcards = []
                            player = []
                            b = 0
                    if a == 2:
                        self.cardsTable.append(i)

            c += 1

        mevaposicio = -1
        mev = 1
        for i in self.players:
            if i[0] == self.player_name:
                self.background[int(i[1])-1] = 'SeaGreen3'
                mevaposicio = mev
            mev += 1

        if not self.target_position == 0:
            self.background[int(self.target_position)-1] = 'CadetBlue2'

        for i in retirats:
            jugador = self.players[i]
            self.background[int(jugador[1])-1] = 'indian red'

        if int(self.players[mevaposicio-1][2]) < int(self.highestBet):
            self.showCall = True

        if self.inicipartida < 2 or rrr == True:
            self.updatecards = True
        if not self.pot_before == self.pot:
            self.updated = True
            self.updatepot = True
        if not self.small_blind_before == self.small_blind:
            self.updated = True
            self.updatesmallblind = True
        if not self.dealer_position_before == self.dealer_position:
            self.updated = True
            self.updatedealer = True
        if not self.target_position_before == self.target_position:
            self.updated = True
        if not self.players_before == self.players:
            self.updated = True
        if not self.cardsTable_before == self.cardsTable:
            self.updated = True
            self.updatetablecards = True
        if not self.highestBet_before == self.highestBet:
            self.updated = True

        self.yourTourn = False
        self.iniciPartida = +1
        if not self.target_position == self.target_position_before:
            self.updateGameview()

    def updateGameview(self):
        print('GAME VIEW UPDATE FUNCTION STARTED')
        if self.updated == True:

            # busco posicio current user
            id = -1
            for i in self.players:
                print(str(i[0]))
                print(str(self.player_name))
                if str(i[0]) == str(self.player_name):
                    id = int(i[1])

            copiaPositions = []
            newPositions = []
            copiaPositions = self.positions
            self.positions = []
            posit = 9-id
            if posit < 1:
                posit = posit+10
            for i in copiaPositions:
                if i-posit < 0:
                    newPositions.insert(i-posit+9, i)
                else:
                    newPositions.insert(i-posit, i)
            self.positions = newPositions

            # update pot

            if self.updatepot == True:
                self.framePot.destroy()
                self.chips_img = 'null'
                self.chips_label.destroy()

                self.framePot = tkinter.Frame(self.window, bg='white')
                self.framePot.place(x=585, y=320)

                self.chips_img = Image.open(os.getcwd()+'/Images/chips.png')
                self.chips_img = self.chips_img.resize(
                    (50, 50), Image.ANTIALIAS)
                self.chips_img = ImageTk.PhotoImage(self.chips_img)
                self.chips_label = tkinter.Label(
                    self.framePot, image=self.chips_img, bg='white')
                self.chips_label.grid(row=0, column=0)

                pot = tkinter.Label(self.framePot, text="POT :"+str(self.pot) +
                                    "$", borderwidth=10, font="Helvetica 15", bg='white')
                pot.grid(row=0, column=1)

                self.updatepot = False

            # update smallblind
            if self.updatesmallblind == True:
                self.frameBlind.destroy()
                self.frameBlind = tkinter.Frame(self.window, bg='white')
                self.frameBlind.place(x=20, y=20)
                blind = tkinter.Label(self.frameBlind, text="Small Blind " +
                                      str(self.small_blind)+"$", borderwidth=10, font="Helvetica 15", bg='white')
                blind.pack()
                self.updatesmallblind = False

            # update dealerposition
            if self.updatedealer == True:
                for i in self.framesDealer:
                    i.destroy()
                self.createFramesDealer()

                self.addDealer()
                self.updateDealer = False

            # update player and target:
            if self.updatecards == True:
                self.imagesCardsPlayers = []
                self.labelsCardsPlayers = []

                for i in self.framesCards:
                    i.destroy()

                self.createFramesCards()

            for i in self.framesPlayers:
                i.destroy()
            self.createFramesPlayers()
            self.addPlayers()
            # update tableCards
            if self.updatetablecards == True:
                self.imagesCardsTable = []
                self.labelsCardsTable = []

                self.frameTableCards.destroy()
                self.frameTableCards = tkinter.Frame(self.window, bg='green')
                self.frameTableCards.place(x=495, y=380)
                self.addTableCards()

            self.updated = False
            print('GAME VIEW UPDATE FUNCTION FINISHED')
            self.window.after(100, self.updateGameview)
            self.updatetablecards = False

    def isYourTourn(self):
        self.yourTourn = True

    def roundResultUpdate(self, roundresult):
        if not roundresult == 'null':
            rr = []
            it = 0
            maguanyadora = roundresult[1]
            for i in roundresult:
                if not it <= 1:
                    rr.append(i)
                it += 1

            roundResult = tkinter.Toplevel()
            roundResult.title('Round Result')
            roundResult.iconphoto(False, ImageTk.PhotoImage(
                file=os.getcwd()+'/Images/result.png'))
            roundResult.focus_set()
            roundResult.grab_set()

            roundResultFrame = tkinter.Frame(roundResult)
            roundResultFrame.pack(padx=20, pady=20)

            roundResultLabel = tkinter.Label(
                roundResultFrame, text="Winners: ", borderwidth=10, font="Helvetica 20")
            roundResultLabel.pack()
            for i in rr:
                winnersLabel = tkinter.Label(
                    roundResultFrame, text=i, borderwidth=10, font="Helvetica 20")
                winnersLabel.pack()

            if not maguanyadora == -1:
                winningCard = tkinter.Label(
                    roundResultFrame, text="Winning Hand:", borderwidth=10, font="Helvetica 20")
                winningCard.pack()

                self.ma = self.printCards(maguanyadora)
                self.maLabel = tkinter.Label(roundResultFrame, image=self.ma)
                self.maLabel.pack()
            returnButton = tkinter.Button(
                roundResultFrame, text="Return", font="Helvetica 20", command=roundResult.destroy)
            returnButton.pack()

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

            gameResult = tkinter.Toplevel()
            gameResult.title('Game Result')
            gameResult.iconphoto(False, ImageTk.PhotoImage(
                os.getcwd()+'/Images/result.png'))
            gameResult.focus_set()
            gameResult.grab_set()

            gameResultFrame = tkinter.Frame(gameResult)
            gameResultFrame.pack(padx=20, pady=20)

            gameResultLabel = tkinter.Label(
                gameResultFrame, text="Position: "+str(posiciofinal), borderwidth=10, font="Helvetica 20")
            gameResultLabel.pack()

            winningsLabel = tkinter.Label(
                gameResultFrame, text="Winnings: "+str(winnings), borderwidth=10, font="Helvetica 20")
            winningsLabel.pack()

            def closingGame():
                self.endPlayer = True
                gameResult.destroy()
            returnButton = tkinter.Button(
                gameResultFrame, text="Return", font="Helvetica 20", command=closingGame)
            returnButton.pack()

            gameResult.protocol("WM_DELETE_WINDOW", closingGame)

    def gameView(self):

        self.my_img = Image.open(os.getcwd()+'/Images/mesa.png')
        self.my_img = self.my_img.resize((1275, 767), Image.ANTIALIAS)
        self.my_img = ImageTk.PhotoImage(self.my_img)
        self.my_label = tkinter.Label(self.window, image=self.my_img)
        self.my_label.pack()

        self.frameButtons = tkinter.Frame(self.window)
        self.frameButtons.place(x=500, y=20)
        self.buttons()

        self.framePot = tkinter.Frame(self.window, bg='white')
        self.framePot.place(x=585, y=320)

        self.chips_label = tkinter.Label(
            self.framePot, bg='green')
        self.chips_label.grid(row=0, column=0)

        self.frameBlind = tkinter.Frame(self.window, bg='white')
        self.frameBlind.place(x=20, y=20)

        self.frameTableCards = tkinter.Frame(self.window, bg='green')
        self.frameTableCards.place(x=495, y=380)

        self.createFramesPlayers()
        self.createFramesCards()
        self.createFramesDealer()

        self.started = True

        self.window.after(1000, self.updateGameview)

    def addPlayers(self):
        for i in self.players:
            self.addPlayer(i)
            if self.updatecards == True:
                self.addCards(i)

        self.updatecards = False

    def addPlayer(self, pla):
        name = str(pla[0])
        pos = int(pla[1])
        bet = pla[2]
        stack = pla[3]

        user = tkinter.Label(self.framesPlayers[self.positions[pos-1]-1], text=name,
                             borderwidth=10, font="Helvetica 15", bg=self.background[pos-1])
        user.grid(row=0, column=0)

        accUser = tkinter.Label(self.framesPlayers[self.positions[pos-1]-1], text=str(stack) +
                                "$", borderwidth=10, font="Helvetica 15", bg=self.background[pos-1])
        accUser.grid(row=0, column=1)

        betUser = tkinter.Label(self.framesPlayers[self.positions[pos-1]-1], text="Bet: " +
                                str(bet)+"$", borderwidth=10, font="Helvetica 15", bg=self.background[pos-1])
        betUser.grid(row=1, columnspan=2)

    def buttons(self):

        user_text = tkinter.Entry(
            self.frameButtons, font="Helvetica 20", width='10')
        user_text.grid(row=0, column=1)

        def buttonCheck():
            if self.yourTourn == True:
                self.player_reply = [
                    player_state_id['player_reply'], player_action['check']]
                self.yourTourn = False

        def buttonFold():
            if self.yourTourn == True:
                self.player_reply = [
                    player_state_id['player_reply'], player_action['fold']]
                self.yourTourn = False

        def buttonRaise():
            if self.yourTourn == True:
                self.player_reply = [player_state_id['player_reply'],
                                     player_action['raise'], user_text.get()]
                self.yourTourn = False

        def buttonCall():
            if self.yourTourn == True and self.showCall == True:
                self.player_reply = [
                    player_state_id['player_reply'], player_action['call']]
                self.showCall = False
                self.yourTourn = False

        check = tkinter.Button(
            self.frameButtons, text="Check", command=buttonCheck, font="Helvetica 20")
        check.grid(row=0, column=5)

        fold = tkinter.Button(self.frameButtons, text="Fold",
                              command=buttonFold, font="Helvetica 20")
        fold.grid(row=0, column=4)

        raisee = tkinter.Button(
            self.frameButtons, text="Raise", command=buttonRaise, font="Helvetica 20")
        raisee.grid(row=0, column=3)

        call = tkinter.Button(
            self.frameButtons, text="Call", command=buttonCall, font="Helvetica 20")
        call.grid(row=0, column=6)

        raiseLabel = tkinter.Label(
            self.frameButtons, text="Raise: ", font="Helvetica 20")
        raiseLabel.grid(row=0, column=0)

        raiseLabelD = tkinter.Label(
            self.frameButtons, text="$", font="Helvetica 20")
        raiseLabelD.grid(row=0, column=2)

    def addDealer(self):
        self.dealer = Image.open(os.getcwd()+'/Images/dealer.png')
        self.dealer = self.dealer.resize((45, 45), Image.ANTIALIAS)
        self.dealer = ImageTk.PhotoImage(self.dealer)
        self.dealerLabel = tkinter.Label(self.framesDealer[self.positions[int(
            self.dealer_position)-1]-1], image=self.dealer, bg='green')
        self.dealerLabel.pack()

    def addTableCards(self):

        car = []
        lab = []
        for i in self.cardsTable:
            car.append(self.printCards(i))
        self.imagesCardsTable.append(car)

        for i in range(len(self.cardsTable)):
            l = tkinter.Label(self.frameTableCards, image=self.imagesCardsTable[len(
                self.imagesCardsTable)-1][i])
            lab.append(l)
        self.labelsCardsTable.append(lab)

        for i in range(len(self.cardsTable)):
            self.labelsCardsTable[len(
                self.labelsCardsTable)-1][i].pack(side='left')

    def addCards(self, usr):
        cards = []
        labels = []
        for i in range(2):
            if not usr[0] == self.player_name:
                if usr[4] == "1":
                    cards.append(self.printCards(usr[5+i]))
                else:
                    cards.append(self.printCards(-1))
            else:
                cards.append(self.printCards(usr[5+i]))
        self.imagesCardsPlayers.append(cards)

        for i in range(2):
            label = tkinter.Label(self.framesCards[self.positions[int(
                usr[1])-1]-1], image=self.imagesCardsPlayers[len(self.imagesCardsPlayers)-1][i])
            labels.append(label)
        self.labelsCardsPlayers.append(labels)

        for i in range(2):
            self.labelsCardsPlayers[len(
                self.labelsCardsPlayers)-1][i].grid(row=0, column=i)

    def printCards(self, code):
        path = self.decodeCard(code)

        card = Image.open(path)
        card = card.resize((70, 107), Image.ANTIALIAS)
        card = ImageTk.PhotoImage(card)

        return card

    def createFramesCards(self):
        fr1 = tkinter.Frame(self.window)
        fr1.place(x=90, y=90)

        fr2 = tkinter.Frame(self.window)
        fr2.place(x=340, y=200)

        fr3 = tkinter.Frame(self.window)
        fr3.place(x=600, y=200)

        fr4 = tkinter.Frame(self.window)
        fr4.place(x=850, y=200)

        fr5 = tkinter.Frame(self.window)
        fr5.place(x=1100, y=90)

        fr10 = tkinter.Frame(self.window)
        fr10.place(x=90, y=610)

        fr9 = tkinter.Frame(self.window)
        fr9.place(x=340, y=500)

        fr8 = tkinter.Frame(self.window)
        fr8.place(x=600, y=500)

        fr7 = tkinter.Frame(self.window)
        fr7.place(x=850, y=500)

        fr6 = tkinter.Frame(self.window)
        fr6.place(x=1100, y=610)
        self.framesCards = [fr1, fr2, fr3, fr4, fr5, fr6, fr7, fr8, fr9, fr10]

    def createFramesDealer(self):
        f1 = tkinter.Frame(self.window, bg='green')
        f1.place(x=200, y=300)

        f2 = tkinter.Frame(self.window, bg='green')
        f2.place(x=490, y=250)

        f3 = tkinter.Frame(self.window, bg='green')
        f3.place(x=750, y=250)

        f4 = tkinter.Frame(self.window, bg='green')
        f4.place(x=1000, y=250)

        f5 = tkinter.Frame(self.window, bg='green')
        f5.place(x=1100, y=300)

        f10 = tkinter.Frame(self.window, bg='green')
        f10.place(x=200, y=460)

        f9 = tkinter.Frame(self.window, bg='green')
        f9.place(x=490, y=520)

        f8 = tkinter.Frame(self.window, bg='green')
        f8.place(x=750, y=520)

        f7 = tkinter.Frame(self.window, bg='green')
        f7.place(x=1000, y=520)

        f6 = tkinter.Frame(self.window, bg='green')
        f6.place(x=1100, y=460)

        self.framesDealer = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]

    def createFramesPlayers(self):
        for i in range(10):
            if self.positions[i]-1 == 0:
                frame1 = tkinter.Frame(self.window, bg=self.background[i])
                frame1.place(x=90, y=200)
            if self.positions[i]-1 == 1:
                frame2 = tkinter.Frame(self.window, bg=self.background[i])
                frame2.place(x=340, y=100)
            if self.positions[i]-1 == 2:
                frame3 = tkinter.Frame(self.window, bg=self.background[i])
                frame3.place(x=600, y=100)
            if self.positions[i]-1 == 3:
                frame4 = tkinter.Frame(self.window, bg=self.background[i])
                frame4.place(x=850, y=100)
            if self.positions[i]-1 == 4:
                frame5 = tkinter.Frame(self.window, bg=self.background[i])
                frame5.place(x=1100, y=200)
            if self.positions[i]-1 == 9:
                frame10 = tkinter.Frame(self.window, bg=self.background[i])
                frame10.place(x=90, y=515)
            if self.positions[i]-1 == 8:
                frame9 = tkinter.Frame(self.window, bg=self.background[i])
                frame9.place(x=340, y=615)
            if self.positions[i]-1 == 7:
                frame8 = tkinter.Frame(self.window, bg=self.background[i])
                frame8.place(x=600, y=615)
            if self.positions[i]-1 == 6:
                frame7 = tkinter.Frame(self.window, bg=self.background[i])
                frame7.place(x=850, y=615)
            if self.positions[i]-1 == 5:
                frame6 = tkinter.Frame(self.window, bg=self.background[i])
                frame6.place(x=1100, y=515)

        self.framesPlayers = [frame1, frame2, frame3, frame4,
                              frame5, frame6, frame7, frame8, frame9, frame10]

    def decodeCard(self, coding):
        if not int(coding) == -1:

            suit = int(coding)//100
            rank = int(coding)-suit*100
            if suit == 0:
                suit = int(coding)//10
                rank = int(coding)-suit*10

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

            path = os.getcwd()+'/Images/cards/'+rank_string+' of '+suit_string+'.png'
        else:
            path = os.getcwd()+'/Images/cards/default.png'
        return path
