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
UsersGame = set()

class MainWindow:
    def __init__(self, root):
        self.c = Controller.Controller('RGAPI-580545bf-2972-45f2-a1df-3bf5e8fe6f96', 'euw1')
        self.root = root
        self.root.resizable(width=False, height=False)

        self.content = Frame(self.root, width= 1512, height=1512)
        self.root.title("League Customs")
        self.content.grid(column=0, row=0)

        # Up left
        repositoriFrame = Frame(self.content, width= 128, height=128)
        repositoriFrame.grid(column=0, row=0, padx=16, pady=16)
        # add user to list
        addToAll = Button(repositoriFrame, text='Register', command=lambda: self.update_player_list())
        addToAll.grid(column=0, row=0, sticky=(N,W,E,S))
        # list of all users
        self.listAll = Listbox(repositoriFrame, height=10, width=52)
        scrollAll = Scrollbar(repositoriFrame, orient=VERTICAL, command=self.listAll.yview)
        scrollAll.grid(column=1, row=1, sticky=(N,S))
        self.listAll['yscrollcommand'] = scrollAll.set
        self.listAll.grid(column=0, row=1)
        playersAll = list()
        for i in self.c.player_list.players:
            #listAll.insert('end', i)
            playersAll.append(i)
        # playersAll.sort() no se si realmente va bien ordenarlos,
        # porque pone primero los que empiezan por mayusculas, luego las minusculas
        for i in playersAll:
            self.listAll.insert('end', i)

        # up mid
        self.mid_bar = Frame(self.content, width= 128, height=128)
        self.mid_bar.grid(column=1, row=0, padx=16, pady=16)
        # add user to game
        self.addToGame = Button(self.mid_bar, text='Add >>', command=lambda: self.addUser())
        self.addToGame.grid(column=0, row=0, pady=8)
        # remove user from game
        self.removeFromGame = Button(self.mid_bar, text='<< Remove', command=lambda: self.removeUser())
        self.removeFromGame.grid(column=0, row=1, pady=8)
        self.profile = Button(self.mid_bar, text='Profile', command=lambda: self.show_profile(Profile))
        self.profile.grid(column=0, row=2, pady=8)
        self.generateGame = Button(self.mid_bar, text='Generate', command=lambda: self.generate_game())
        self.generateGame.grid(column=0, row=3, pady=8)


        # up right
        self.playerNotebook = ttk.Notebook(self.content)
        self.playerNotebook.grid(column=2, row=0, padx=16, pady=16)
        self.playerFrame = Frame(self.playerNotebook, width= 128, height=128)
        self.playerFrame.grid(column=0, row=0, padx=16, pady=16)
        self.lobbyFrame = Frame(self.playerNotebook,width= 128, height=128)
        self.lobbyFrame.grid(column=0, row=0, padx=16, pady=16)

        self.playerNotebook.add(self.playerFrame, text="From List", padding=10)
        self.playerNotebook.add(self.lobbyFrame, text="From Lobby", padding=10)

        self.playerNotebook.bind("<<NotebookTabChanged>>", )
        # this should be a scroll list of the users that will play
        self.listPlayers = Listbox(self.playerFrame, height=10, width=52)
        self.listPlayers.grid(column=0, row=1)

        # down left
        # this should have all the data for team 1
        self.teamBlueFrame = Frame(self.content, width= 128, height=128)
        self.teamBlueFrame.grid(column=0, row=1)
        self.teamBlueLabel = Label(self.teamBlueFrame, text="Blue team")
        self.teamBlueLabel.grid(column=0, row=0)
        self.listBlue = Listbox(self.teamBlueFrame, height=5, width=52)
        self.listBlue.grid(column=0, row=1)

        self.laneFrame = Frame(self.content)
        self.laneFrame.grid(column=1, row=1)
        self.labeltop = Label(self.laneFrame, text="Lanes", font="Helvetica 10 bold")
        self.labeltop.grid(column=0, row=0)
        self.labeljung = Label(self.laneFrame, text="Top")
        self.labeljung.grid(column=0, row=1)
        self.labelmid = Label(self.laneFrame, text="Jungler")
        self.labelmid.grid(column=0, row=2)
        self.labeladc = Label(self.laneFrame, text="Midlaner")
        self.labeladc.grid(column=0, row=3)
        self.labelsup = Label(self.laneFrame, text="ADC")
        self.labelsup.grid(column=0, row=4)
        self.labelsup = Label(self.laneFrame, text="Support")
        self.labelsup.grid(column=0, row=5)

        # down right
        # this should have all the data for team 2
        self.teamRedFrame = Frame(self.content, width= 128, height=128)
        self.teamRedFrame.grid(column=2, row=1, padx=16, pady=16)
        self.teamRedLabel = Label(self.teamRedFrame, text="Red team")
        self.teamRedLabel.grid(column=0, row=0)
        self.listRed = Listbox(self.teamRedFrame, height=5, width=52)
        self.listRed.grid(column=0, row=1)
        self.update_player_list()


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
        if(0 < len(self.listPlayers.curselection())):
            UsersGame.remove(self.listPlayers.get(self.listPlayers.curselection()[0]))
            self.listPlayers.delete(self.listPlayers.curselection()[0])

    def addUser(self):
        if(0 < len(self.listAll.curselection()) and self.listPlayers.size() < MaxPlayers
        and not self.listAll.get(self.listAll.curselection()[0]) in UsersGame):
            user = self.listAll.get(self.listAll.curselection()[0])
            UsersGame.add(user)
            self.listPlayers.insert('end', user)

    def update_player_list(self):
        for i in range(0, self.listAll.size()):
            if i%2: self.listAll.itemconfigure(i, background='#AEB7B3')
            else: self.listAll.itemconfigure(i, background='#E1EFE6')

    def generate_game(self):
        return
        if(9 < self.listPlayers.size()):
            #self.c.
            self.listBlue.delete(0, END)
            self.listRed.delete(0, END)
            f = open("../Controller/text_test", "w", encoding="utf8")
            print(self.txt.get("1.0", END), file=f)
            f.close()

            team1, team2 = self.c.new_game("../Controller/text_test")
            self.c.close()
            for x in team1.players:
                self.listBlue.insert('end', x)
            for x in team2.players:
                self.listRed.insert('end', x)
            self.t1.config(text="Team 1's Rating -> " + str(team1.rating()))
            self.teamBlueLabel.config(text="Team 1's Rating -> " + str(team1.rating()))
            self.t2.config(text="Team 2's Rating -> " + str(team2.rating()))
            self.teamRedLabel.config(text="Team 2's Rating -> " + str(team2.rating()))
            self.listBlue.update()
            self.listRed.update()

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
