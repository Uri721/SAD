import tkinter
import datetime

from PIL import ImageTk, Image


class Game_SetUp(object):

    def __init__(self):

        self.win = tkinter.Toplevel()
        self.win.title('New Game Setup')
        self.win.iconphoto(True, ImageTk.PhotoImage(
            file='/Users/carlosrodriguezperise/Desktop/Imatges/chips.png'))

        self.win.focus_set()
        self.win.grab_set()

    def gameSetUp(self):

        self.stup = 'null'
        fra = tkinter.Frame(self.win)
        fra.pack(padx=20, pady=20)

        def gType(selection):
            self.tipusJoc = selection

        gameType = tkinter.Label(
            fra, text="Game Type", borderwidth=10, font="Helvetica 15")
        gameType.grid(sticky='W')

        optionList = ["Tournament", "Sit&Go", "Cash"]
        variable = tkinter.StringVar(fra)
        variable.set(optionList[0])

        opt = tkinter.OptionMenu(fra, variable, *optionList, command=gType)
        opt.config(width=18, font="Helvetica 15")
        opt.grid(row=0, column=1)

        gameName = tkinter.Label(
            fra, text="Game Name", borderwidth=10, font="Helvetica 15")
        gameName.grid(sticky='W')

        gameNameText = tkinter.Entry(fra, font="Helvetica 15")
        gameNameText.grid(row=1, column=1)

        self.tipusJoc = optionList[0]

        def process_input():

            nomJoc = gameNameText.get()
            numMaxJugadors = maxNumPlayersText.get()
            dinersInicials = initialMoneyText.get()
            timeStart = startTimeText.get()
            st = stakesText.get()
            stRatio = stakesRatioText.get()

            DateTime = timeStart.split(" ")
            date = DateTime[0].split("-")
            time = DateTime[1].split(":")

            d1 = datetime.time(int(time[0]), int(time[1]), int(time[2]))
            d2 = datetime.date(int(date[0]), int(date[1]), int(date[2]))
            d = datetime.datetime.combine(d2, d1)
            timeStart = datetime.datetime.timestamp(d)

            self.stup = [self.tipusJoc, nomJoc, numMaxJugadors, dinersInicials,
                         timeStart, st, stRatio]

            e = False

            if int(numMaxJugadors) > 10:
                self.stup.clear()
                self.error("Max Num of Players cannot be over 10")
                e = True

            elif d < datetime.datetime.now():
                self.stup.clear()
                self.error("Wrong start time")
                e = True

            if e == False:
                self.win.destroy()

        maxNumPlayers = tkinter.Label(
            fra, text="Max Num of Players", borderwidth=10, font="Helvetica 15")
        maxNumPlayers.grid(sticky='W')

        maxNumPlayersText = tkinter.Entry(fra, font="Helvetica 15")
        maxNumPlayersText.grid(row=2, column=1)

        initialMoney = tkinter.Label(
            fra, text="Initial Money", borderwidth=10, font="Helvetica 15")
        initialMoney.grid(sticky='W')

        initialMoneyText = tkinter.Entry(fra, font="Helvetica 15")
        initialMoneyText.grid(row=3, column=1)

        startTime = tkinter.Label(
            fra, text="Start Time", borderwidth=10, font="Helvetica 15")
        startTime.grid(sticky='W')

        startTimeText = tkinter.Entry(fra, font="Helvetica 15")
        startTimeText.grid(row=4, column=1)

        stakes = tkinter.Label(
            fra, text="Stakes", borderwidth=10, font="Helvetica 15")
        stakes.grid(sticky='W')

        stakesText = tkinter.Entry(fra, font="Helvetica 15")
        stakesText.grid(row=5, column=1)

        stakesRatio = tkinter.Label(
            fra, text="Stakes Ratio", borderwidth=10, font="Helvetica 15")
        stakesRatio.grid(sticky='W')

        stakesRatioText = tkinter.Entry(fra, font="Helvetica 15")
        stakesRatioText.grid(row=6, column=1)
        create = tkinter.Button(
            fra, text="Create", command=process_input, font="Helvetica 15")
        create.grid(row=7, column=1, sticky='E')

        self.win.wait_window()
        return self.stup

    def error(self, err):

        wind = tkinter.Toplevel()
        wind.title('ERROR')
        wind.iconphoto(False, ImageTk.PhotoImage(
            file='/Users/carlosrodriguezperise/Desktop/Imatges/error.png'))
        wind.focus_set()
        wind.grab_set()

        fr = tkinter.Frame(wind)
        fr.pack(padx=20, pady=20)

        error1 = tkinter.Label(
            fr, text=err, borderwidth=10, font="Helvetica 15")
        error1.pack()

        button_quit = tkinter.Button(
            fr, text="Return", command=wind.destroy, font="Helvetica 15")
        button_quit.pack()

        wind.wait_window()
