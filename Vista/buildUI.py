import json
from tkinter import *
from tkinter import ttk

from PIL import ImageTk, Image
from Model import constants
from Controller import joined
import Controller

file = open("../assets/player_dictionaries", "r")
player_dict = json.load(file)
file.close()

MaxPlayers = 10

class MainWindow:
    def __init__(self, root):
        self.c = Controller.Controller('RGAPI-580545bf-2972-45f2-a1df-3bf5e8fe6f96', 'euw1')
        self.root = root

        self.content = ttk.Frame(self.root, width= 1512, height=1512)
        self.root.title("League Customs")
        self.content.grid(column=0, row=0)

        # Up left
        self.repositoriFrame = ttk.Frame(self.content, width= 128, height=128)
        self.repositoriFrame.grid(column=0, row=0, padx=16, pady=16)
        # add user to list
        self.addToAll = ttk.Button(self.repositoriFrame, text='Register')
        self.addToAll.grid(column=0, row=0, sticky=(N,W,E,S))
        # list of all users
        self.listAll = Listbox(self.repositoriFrame, height=10, width=52)
        self.scrollAll = ttk.Scrollbar(self.repositoriFrame, orient=VERTICAL, command=self.listAll.yview)
        self.scrollAll.grid(column=1, row=1, sticky=(N,S))
        self.listAll['yscrollcommand'] = self.scrollAll.set
        self.listAll.grid(column=0, row=1)
        self.playersAll = list()
        for i in self.c.player_list.players:
            #listAll.insert('end', i)
            self.playersAll.append(i)
        # playersAll.sort() no se si realmente va bien ordenarlos,
        # porque pone primero los que empiezan por mayusculas, luego las minusculas
        for i in self.playersAll:
            self.listAll.insert('end', i)

        # up mid
        self.mid_bar = ttk.Frame(self.content, width= 128, height=128)
        self.mid_bar.grid(column=1, row=0, padx=16, pady=16)
        # add user to game
        self.addToGame = ttk.Button(self.mid_bar, text='Add >>', command=lambda: self.addUser())
        self.addToGame.grid(column=0, row=0, pady=8)
        # remove user from game
        self.removeFromGame = ttk.Button(self.mid_bar, text='<< Remove', command=lambda: self.removeUser())
        self.removeFromGame.grid(column=0, row=1, pady=8)
        self.profile = ttk.Button(self.mid_bar, text='Profile', command=lambda: self.show_profile(Profile))
        self.profile.grid(column=0, row=2, pady=8)
        self.generateGame = ttk.Button(self.mid_bar, text='Generate')
        self.generateGame.grid(column=0, row=3, pady=8)


        # up right
        self.playerNotebook = ttk.Notebook(self.content)
        self.playerNotebook.grid(column=2, row=0, padx=16, pady=16)
        self.playerFrame = ttk.Frame(self.playerNotebook, width= 128, height=128)
        self.playerFrame.grid(column=0, row=0, padx=16, pady=16)
        self.lobbyFrame = ttk.Frame(self.playerNotebook,width= 128, height=128)
        self.lobbyFrame.grid(column=0, row=0, padx=16, pady=16)

        self.playerNotebook.add(self.playerFrame, text="From List", padding=10)
        self.playerNotebook.add(self.lobbyFrame, text="From Lobby", padding=10)

        self.playerNotebook.bind("<<NotebookTabChanged>>", )
        # this should be a scroll list of the users that will play
        self.listPlayers = Listbox(self.playerFrame, height=10, width=52)
        self.scrollPlayers = ttk.Scrollbar(self.playerFrame, orient=VERTICAL, command=self.listPlayers.yview)
        self.scrollPlayers.grid(column=1, row=1, sticky=(N,S))
        self.listPlayers['yscrollcommand'] = self.scrollAll.set
        self.listPlayers.grid(column=0, row=1)

        # down left
        # this should have all the data for team 1
        self.teamBlueFrame = ttk.Frame(self.content, width= 128, height=128)
        self.teamBlueFrame.grid(column=0, row=1)
        self.teamBlueLabel = ttk.Label(self.teamBlueFrame, text="Blue team")
        self.teamBlueLabel.grid(column=0, row=0)
        self.listBlue = Listbox(self.teamBlueFrame, height=5, width=52)
        self.listBlue.grid(column=0, row=1)

        self.laneFrame = ttk.Frame(self.content, width=128, height=128)
        self.laneFrame.grid(column=1, row=1)
        self.labeltop = ttk.Label(self.laneFrame, text=" ")
        self.labeltop.grid(column=0, row=0)
        self.labeljung = ttk.Label(self.laneFrame, text="Top")
        self.labeljung.grid(column=0, row=1)
        self.labelmid = ttk.Label(self.laneFrame, text="Jungler")
        self.labelmid.grid(column=0, row=2)
        self.labeladc = ttk.Label(self.laneFrame, text="Midlaner")
        self.labeladc.grid(column=0, row=3)
        self.labelsup = ttk.Label(self.laneFrame, text="ADC")
        self.labelsup.grid(column=0, row=4)
        self.labelsup = ttk.Label(self.laneFrame, text="Support")
        self.labelsup.grid(column=0, row=5)

        # down right
        # this should have all the data for team 2
        self.teamRedFrame = ttk.Frame(self.content, width= 128, height=128)
        self.teamRedFrame.grid(column=2, row=1, padx=16, pady=16)
        self.teamRedTag = ttk.Label(self.teamRedFrame, text="Red team")
        self.teamRedTag.grid(column=0, row=0)
        self.listRed = Listbox(self.teamRedFrame, height=5, width=52)
        self.listRed.grid(column=0, row=1)


    def show_profile(self, _class):
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            name = None
            try:
                name = self.listAll.get(self.listAll.curselection()[0])
            except IndexError:
                name = None
            if name:
                self.new = Toplevel(self.root)
                _class(self.new, name, self.c)

    def removeUser(self):
        if 0 < len(self.listAll.curselection()):
            self.listPlayers.delete(self.listPlayers.curselection()[0])

    def addUser(self):
        if 0 < len(self.listAll.curselection()) and len(self.listPlayers.curselection()) < MaxPlayers:
            self.listPlayers.insert('end', self.listAll.get(self.listAll.curselection()[0]))
        pass


class GetFromLobby:
    def __init__(self, root):
        self.root = root



class Profile:
    def __init__(self, root, name, ctr):

        self.root = root

        self.outer_frame = Frame(self.root)
        self.left_frame = Frame(self.outer_frame)
        self.right_frame = Frame(self.outer_frame)
        self.role_frame = Frame(self.right_frame)

        # Labels, Combobox, etc.

        # El Exum
        if name == "Kite Machine 2": name = "El Exum"

        self.name = Label(self.right_frame, text=name,font="none 24 bold")
        self.role = Label(self.role_frame, text="Role:")
        self.role_combo = ttk.Combobox(self.role_frame,state="readonly", values=("Top", "Jungle", "Mid", "ADC", "Support"))
        self.role.grid(column=0, row=0)
        self.role_combo.grid(column=1, row=0)
        self.rating = Label(self.role_frame, text="Rating:")
        self.rating.grid(column=0, row=1)

        # Rank image
        rank = ctr.get_rank(name)
        self.load_rank = Image.open("../assets/ranked_emblems/Emblem_" + rank[0] + rank[1:len(rank)].lower() + ".png")
        # El Exum
        if name == "El Exum": self.load_rank = Image.open("../assets/ranked_emblems/Emblem_Challenger.png")

        self.load_rank.thumbnail((128, 128), Image.ANTIALIAS)
        self.render_rank = ImageTk.PhotoImage(self.load_rank)
        self.rank_img = Label(self.left_frame, image=self.render_rank)
        self.rank_img.image = self.render_rank

        # Profile image
        imgFile = ctr.get_icon(name)
        self.load_prof = Image.open(imgFile)
        # El Exum
        if name == "El Exum": self.load_prof = Image.open("../assets/SummonerIcons/default_icon.jpg")

        self.load_prof.thumbnail((128, 128), Image.ANTIALIAS)
        self.render_prof = ImageTk.PhotoImage(self.load_prof)
        self.prof_img = Label(self.left_frame, image=self.render_prof, relief=SUNKEN, borderwidth=10)
        self.prof_img.image = self.render_prof


        # Left frame
        self.left_frame.grid(column=0, row=0, padx=10, pady=10)

        self.rank_img.grid(column=0, row=1)
        self.prof_img.grid(column=0, row=0)

        # Right frame
        self.right_frame.grid(column=1, row=0, padx=10, pady=10)
        self.name.grid(column=0, row=0)
        self.role_frame.grid(column=0, row=1, pady=50)

        self.outer_frame.pack()


rt = Tk()
app = MainWindow(rt)
rt.mainloop()
