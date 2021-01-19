import json
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image

from Controller import joined
import Controller

file = open("../Controller/player_dictionaries", "r")
player_dict = json.load(file)
file.close()


class Win:
    def __init__(self, root):
        self.c = Controller.Controller('RGAPI-fedea5c1-8bdc-42c3-8a8a-27b6e1e1f907', 'euw1')
        self.root = root
        content = ttk.Frame(self.root)
        self.root.title("League Customs")
        self.frame = ttk.Frame(content)
        entry = ttk.Entry(self.root)
        self.txt = Text(self.root, height=10, width=50)
        self.bt = Button(self.frame, text="Generate!",width=20, command=lambda: self.generate_teams())
        self.pf_button = Button(self.frame, text="Show Profile",width=20, command=lambda: self.show_profile(Profile))
        self.ls = Listbox(content, height=5, width=30)
        self.ls2 = Listbox(content, height=5, width=30)
        self.t1 = Label(content, text="Team 1")
        self.t2 = Label(content, text="Team 2")
        lblFr1 = LabelFrame(content, height=100, width=200)
        lblFr2 = LabelFrame(content, height=100, width=200)

        positions = ["Top", "Jungle", "Mid", "ADC", "Support"]
        for x in positions:
            Label(lblFr1, text=x).grid()
            Label(lblFr2, text=x).grid()

        menu = Menu()
        for i in ('One', 'Two', 'Three'):
            menu.add_command(label=i)
        # pf = Profile(self.root) # pf.show_profile()
        # Calling on_change when you press the return key
        # self.bt.bind("<ButtonPress>", lambda a: self.generate_teams())
        # frame.grid(column=1,row=0)
        content.grid(column=0, row=0, padx=10, pady=10)
        self.t1.grid(column=1, row=0)
        lblFr1.grid(column=0, row=1)
        self.ls.grid(column=1, row=1, padx=10, pady=10)
        self.t2.grid(column=1, row=2)
        lblFr2.grid(column=0, row=3)
        self.ls2.grid(column=1, row=3, padx=10, pady=10)
        # entry.grid(column=1,row=0)
        self.txt.grid(column=2, row=0, padx=10, pady=10)
        self.frame.grid(column=2,row=1)
        self.pf_button.grid(column=0, row=0, pady=5)
        self.bt.grid(column=0, row=1, pady=5)

    def generate_teams(self):
        self.ls.delete(0, END)
        self.ls2.delete(0, END)
        f = open("../Controller/text_test", "w", encoding="utf8")
        print(self.txt.get("1.0", END), file=f)
        f.close()

        team1, team2 = self.c.new_game("../Controller/text_test")
        self.c.close()
        for x in team1.players:
            self.ls.insert('end', x)
        for x in team2.players:
            self.ls2.insert('end', x)
        self.t1.config(text="Team 1's Rating -> " + str(team1.rating()))
        self.t2.config(text="Team 2's Rating -> " + str(team2.rating()))
        self.ls.update()
        self.ls2.update()

    def show_profile(self, _class):
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            self.new = Toplevel(self.root)
            _class(self.new)


class Profile:
    def __init__(self, root):
        self.root = root
        self.load = Image.open("../Vista/test.jpg")
        self.render = ImageTk.PhotoImage(self.load)
        self.img = Label(self.root, image=self.render, height=267, width=267)
        self.img.image = self.render
        self.img.grid(column=0,row=0)


rt = Tk()
app = Win(rt)
rt.mainloop()
