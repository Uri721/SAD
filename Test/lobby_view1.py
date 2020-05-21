import tkinter
from game_setup import Game_SetUp
from system_tool import lobby_id_h_cmd as lobby_id_h
from system_tool import conn_id_cmd as conn_id
import datetime
from PIL import ImageTk, Image


class Lobby_View(object):

    def __init__(self):
        self.system_users = []
        self.system_games = []
        self.acc_balances = "0"
        self.games = 0
        self.updated = False
        self.started = False
        self.system_users_before = ["c"]
        self.system_games_before = ["c"]
        self.acc_balances_before = "-1"
        self.busy = False

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
                if i == "$":
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

                accountBalance = tkinter.Label(self.frame, text=str(
                    self.acc_balances)+"$", font="Helvetica 15", bg='white')
                accountBalance.grid(row=0, column=1)

                for g in self.system_games:
                    self.addGame(g)

                for u in self.system_users:
                    self.addUser(u)

                self.updated = False

            self.window.after(1000, self.updateWindow)

    def lobbyView(self):
        self.window = tkinter.Tk()
        self.window.iconphoto(
            True, ImageTk.PhotoImage(file='/Users/carlosrodriguezperise/Desktop/Imatges/chips.png'))
        self.window.eval('tk::PlaceWindow . center')
        self.window.title('Lobby View')

        self.frame = tkinter.Frame(self.window)
        self.frame.pack(side='left', padx=20, pady=20)

        self.frameU = tkinter.Frame(self.window)
        self.frameU.pack(side='left', padx=20, pady=20)

        usersConnected = tkinter.Label(
            self.frameU, text="Users Connected:", font="Helvetica 15")
        usersConnected.grid(row=0)

        gameList = tkinter.Label(
            self.frame, text="Game List", borderwidth=10, font="Helvetica 15")
        gameList.grid(row=1, column=0)

        newGame = tkinter.Button(
            self.frame, text="New Game", command=self.createNewGame, font="Helvetica 15")
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
            self.error("The game is already full")
        else:
            if datetime.datetime.fromtimestamp(g[4]) < datetime.datetime.now():
                self.error("The game has already started")
            else:
                self.window.destroy()
                self.input = [lobby_id_h['join_game'], self.games]

    def createNewGame(self):
        gs = Game_SetUp()
        gameSet = gs.gameSetUp()

        if not gameSet == 'null':
            if not gameSet[1] == 'null':  # se ha cerrado la ventana
                newgm = [self.games, gameSet[1], "0", gameSet[2], gameSet[4]]

                game = tkinter.Label(
                    self.frame2, text=gameSet[1], borderwidth=10, font="Helvetica 15")
                game.grid(sticky='W')
                enter = tkinter.Button(self.frame2, text="Enter", command=lambda: self.play(
                    newgm), font="Helvetica 15")
                enter.grid(row=self.games+2, column=1)

                self.games += 1
                self.system_games.append(newgm)

                self.input = [lobby_id_h['create_game'], self.games]

    def addGame(self, g):
        game = tkinter.Label(
            self.frame2, text=g[1], borderwidth=10, font="Helvetica 15")
        game.grid(row=int(g[0])+1, column=0)

        enter = tkinter.Button(self.frame2, text="Enter",
                               command=lambda: self.play(g), font="Helvetica 15")
        enter.grid(row=int(g[0])+1, column=1)

    def addUser(self, u):
        usr = tkinter.Label(self.frameU2, text=u,
                            borderwidth=10, font="Helvetica 15")
        usr.grid(row=self.system_users.index(u)+1)

    def input(self):
        if self.input == 'null':
            return conn_id['disconnect']
        else:
            return self.input

    def error(self, err):
        win = tkinter.Toplevel()
        win.title('ERROR')
        win.iconphoto(
            True, ImageTk.PhotoImage(file='/Users/carlosrodriguezperise/Desktop/Imatges/error.png'))
        win.focus_set()
        win.grab_set()

        fr = tkinter.Frame(win)
        fr.pack(padx=20, pady=20)

        error1 = tkinter.Label(
            fr, text=err, borderwidth=10, font="Helvetica 15")
        error1.pack()

        button_quit = tkinter.Button(
            fr, text="Return", command=win.destroy, font="Helvetica 15")
        button_quit.pack()

        win.wait_window()


"""
d1=datetime.time(1,2,3)
d2=datetime.date(2020,1,11)
d=datetime.datetime.combine(d2,d1)
c=datetime.datetime.timestamp(d)

data_rx=["ALBA", "INES","BIEL", "$", "1", "Joc1", "4", "4",c,"2", "Joc2", "3", "4",c, "$", "200" ]
            
 
lobby = Lobby_View()
lobby.update(data_rx)
lobby.lobbyView()"""
