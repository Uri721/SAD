import tkinter


class Game_View(tkinter.Frame):

    def __init__(self, parent):
        tkinter.Frame.__init__(self, parent)

        self.window = tkinter.Frame(self)
        self.window.pack()

        label = tkinter.Label(self.window, text="lusfliafliuaf")
        label.pack()
