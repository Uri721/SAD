import os
import tkinter

from PIL import ImageTk, Image


class Access_View(object):

    def __init__(self):

        self.window = tkinter.Tk()
        self.window.iconphoto(True, ImageTk.PhotoImage(
            file=os.getcwd()+'/Images/chips.png'))
        self.window.title("System Access")
        self.window.geometry("350x250")
        self.window.eval('tk::PlaceWindow . center')

    def execute(self):

        blank_space_0 = tkinter.Label(self.window, text="")
        blank_space_0.pack()

        username = tkinter.Label(
            self.window, text="Username", borderwidth=10, font="Helvetica 15")
        username.pack()

        user_text = tkinter.Entry(self.window, font="Helvetica 15")
        user_text.pack()

        password = tkinter.Label(
            self.window, text="Password", borderwidth=10, font="Helvetica 15")
        password.pack()

        pass_text = tkinter.Entry(self.window, font="Helvetica 15")
        pass_text.pack()

        def process_input():

            nom = user_text.get()
            contra = pass_text.get()
            global data
            data = [nom, contra]
            self.window.destroy()

        blank_space_1 = tkinter.Label(self.window, text="")
        blank_space_1.pack()

        logIn = tkinter.Button(self.window, text="Log In",
                               command=process_input, font="Helvetica 15")
        logIn.pack()

        self.window.mainloop()

        return data
