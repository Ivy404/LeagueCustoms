import DataService

from tkinter import *
from PIL import Image, ImageTk

import Controller

c = Controller.Controller('RGAPI-fedea5c1-8bdc-42c3-8a8a-27b6e1e1f907', 'euw1')
c.get_icon('buildcrash')

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        load = Image.open("../assets/SummonerIcons/img.png")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)


root = Tk()
app = Window(root)
root.wm_title("Tkinter window")
root.geometry("300x300")
root.mainloop()