import os
import time
import datetime
import tkinter

from PIL import ImageTk, Image

from system_tool import lobby_id_h_cmd as lobby_id_h
from system_tool import conn_id_cmd as conn_id
from system_tool import game_mode_id_b_cmd as game_mode

from game_view import Game_View
from game_setup import Game_SetUp


class Lobby_View(object):

    def __init__(self):

        self.system_users = []
        self.system_games = []
        self.acc_balances = '0'
        self.games = 0
        self.updated = False
        self.started = False
        self.system_users_before = ['c']
        self.system_games_before = ['c']
        self.acc_balances_before = '-1'
        self.busy = False
        self.user_input = []

    def update(self, upda):

        if self.started == True and self.busy == False:
            self.busy == True
            up = upda
            a = 0
            b = 0
            joc = []

            self.updated = False

            self.acc_balances_before = self.acc_balances
            self.system_games_before = self.system_games
            self.system_users_before = self.system_users

            self.system_users = []
            self.system_games = []
            self.acc_balances = 0
            self.games = 0

            for i in up:
                if i == '$':
                    a += 1
                else:
                    if a == 0:
                        self.system_users.append(i)
                    if a == 1:
                        if b < 5:
                            joc.append(i)
                            b += 1
                        if b == 5:
                            self.system_games.append(joc)
                            joc = []
                            b = 0
                            self.games += 1

            self.acc_balances = up[len(up)-1]
            if not self.acc_balances == self.acc_balances_before:
                self.updated = True
            if not self.system_games == self.system_games_before:
                self.updated = True
            if not self.system_users == self.system_users_before:
                self.updated = True

            self.updateWindow()
            self.busy = False

    def updateWindow(self):

        if self.started == True:
            if self.updated == True:

                self.frame2.destroy()
                self.frameU2.destroy()

                self.frame2 = tkinter.Frame(self.frame)
                self.frame2.grid(columnspan=2)

                self.frameU2 = tkinter.Frame(self.frameU)
                self.frameU2.grid(row=1)

                Balance = tkinter.Label(
                    self.frame, text='Account Balance: ', font='Helvetica 15', bg='white')
                Balance.grid(row=0, column=0)

                accountBalance = tkinter.Label(self.frame, text=str(
                    self.acc_balances)+'$', font='Helvetica 15', bg='white')
                accountBalance.grid(row=0, column=1)

                for g in self.system_games:
                    self.addGame(g)

                for u in self.system_users:
                    self.addUser(u)

                self.updated = False

            self.window.after(1000, self.updateWindow)

    def lobbyView(self):

        self.window = tkinter.Tk()
        self.window.iconphoto(False, ImageTk.PhotoImage(
            file=os.getcwd()+'/Images/chips.png'))
        self.window.eval('tk::PlaceWindow . center')
        self.window.title('Lobby View')

        self.frame = tkinter.Frame(self.window)
        self.frame.pack(side='left', padx=20, pady=20)

        self.frameU = tkinter.Frame(self.window)
        self.frameU.pack(side='left', padx=20, pady=20)

        usersConnected = tkinter.Label(
            self.frameU, text='Users Connected:', font='Helvetica 15')
        usersConnected.grid(row=0)

        gameList = tkinter.Label(
            self.frame, text='Game List', borderwidth=10, font='Helvetica 15')
        gameList.grid(row=1, column=0)

        newGame = tkinter.Button(
            self.frame, text='New Game', command=self.createNewGame, font='Helvetica 15')
        newGame.grid(row=1, column=1)

        self.frame2 = tkinter.Frame(self.frame)
        self.frame2.grid(columnspan=2)

        self.frameU2 = tkinter.Frame(self.frameU)
        self.frameU2.grid(row=1)

        self.started = True
        self.window.after(1000, self.updateWindow)

        self.window.mainloop()

    def play(self, g):

        if g[2] >= g[3]:
            self.error('The game is already full')

        else:
            if datetime.datetime.fromtimestamp(g[4]) < datetime.datetime.now():
                self.error('The game has already started')

            else:

                self.user_input = [lobby_id_h['join_game'], g[0]]
                time.sleep(0.25)
                self.user_input.clear()

                # ENTER GAME
                TopLevelGame = tkinter.Toplevel(self.window)
                TopLevelGame.title(g[1])
                TopLevelGame.iconphoto(False, ImageTk.PhotoImage(
                    file=os.getcwd()+'/Images/chips.png'))
                TopLevelGame.attributes('-zoomed', True)
                GAME = Game_View(TopLevelGame)
                GAME.pack()

    def createNewGame(self):

        gs = Game_SetUp()
        gameSet = gs.gameSetUp()

        if not (not gameSet):
            if not (not gameSet[1]):

                newgm = [self.games, gameSet[1], '0', gameSet[2], gameSet[4]]

                self.addGame(newgm)

                self.games += 1
                self.system_games.append(newgm)

                if gameSet[0] == 'Tournament':
                    _ = game_mode['tournament']
                elif gameSet[0] == 'Sit&Go':
                    _ = game_mode['sit_and_go']
                elif gameSet[0] == 'Cash':
                    _ = game_mode['cash_game']

                self.user_input = [lobby_id_h['create_game'], _, gameSet[1],
                                   gameSet[4], gameSet[2], gameSet[3], gameSet[6], gameSet[7]]
                time.sleep(0.25)
                self.user_input.clear()

    def addGame(self, g):

        frameGame = tkinter.Frame(self.frame2)
        frameGame.grid(row=int(g[0])+1, columnspan=2)

        game = tkinter.Label(
            frameGame, text=g[1], borderwidth=10, font='Helvetica 15')
        game.grid(row=0, column=0)

        enter = tkinter.Button(frameGame, text='Enter',
                               command=lambda: self.play(g), font='Helvetica 15')
        enter.grid(row=0, column=1)

        start = tkinter.Label(frameGame, text=' Start: ' +
                              str(datetime.datetime.fromtimestamp(g[4])), font='Helvetica 15')
        start.grid(row=1, columnspan=3)

        players = tkinter.Label(
            frameGame, text='Players: '+g[2]+'/'+g[3], font='Helvetica 15')
        players.grid(row=0, column=2)

    def addUser(self, u):

        usr = tkinter.Label(self.frameU2, text=u,
                            borderwidth=10, font='Helvetica 15')
        usr.grid(row=self.system_users.index(u)+1)

    def error(self, err):

        win = tkinter.Toplevel()
        win.title('ERROR')
        win.iconphoto(False, ImageTk.PhotoImage(
            file=os.getcwd()+'/Imatges/error.png'))
        win.focus_set()
        win.grab_set()

        fr = tkinter.Frame(win)
        fr.pack(padx=20, pady=20)

        error1 = tkinter.Label(
            fr, text=err, borderwidth=10, font='Helvetica 15')
        error1.pack()

        button_quit = tkinter.Button(
            fr, text='Return', command=win.destroy, font='Helvetica 15')
        button_quit.pack()

        win.wait_window()
