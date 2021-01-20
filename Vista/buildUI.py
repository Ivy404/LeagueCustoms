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

        self.content = ttk.Frame(self.root, width= 1512, height=1512)
        self.root.title("League Customs")
        self.content.grid(column=0, row=0)

        # Up left
        repositoriFrame = ttk.Frame(self.content, width= 128, height=128)
        repositoriFrame.grid(column=0, row=0, padx=16, pady=16)
        # add user to list
        addToAll = ttk.Button(repositoriFrame, text='Register')
        addToAll.grid(column=0, row=0, sticky=(N,W,E,S))
        # list of all users
        self.listAll = Listbox(repositoriFrame, height=10, width=52)
        scrollAll = ttk.Scrollbar(repositoriFrame, orient=VERTICAL, command=self.listAll.yview)
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
        mid_bar = ttk.Frame(self.content, width= 128, height=128)
        mid_bar.grid(column=1, row=0, padx=16, pady=16)
        # add user to game
        addToGame = ttk.Button(mid_bar, text='Add >>', command=lambda: self.addUser())
        addToGame.grid(column=0, row=0, pady=8)
        # remove user from game
        removeFromGame = ttk.Button(mid_bar, text='<< Remove', command=lambda: self.removeUser())
        removeFromGame.grid(column=0, row=1, pady=8)
        profile = ttk.Button(mid_bar, text='Perfil', command=lambda: self.show_profile(Profile))
        profile.grid(column=0, row=2, pady=8)
        generateGame = ttk.Button(mid_bar, text='Generate', command=lambda: self.generateGame())
        generateGame.grid(column=0, row=3, pady=8)


        # up right
        playerFrame = ttk.Frame(self.content, width= 128, height=128)
        playerFrame.grid(column=2, row=0, padx=16, pady=16)
        # should open a new window to register from lobby
        fromLobby = ttk.Button(playerFrame, text='From lobby')
        fromLobby.grid(column=0, row=0, sticky=(N,W,E,S))
        # this should be a scroll list of the users that will play
        self.listPlayers = Listbox(playerFrame, height=10, width=52)
        scrollPlayers = ttk.Scrollbar(playerFrame, orient=VERTICAL, command=self.listPlayers.yview)
        scrollPlayers.grid(column=1, row=1, sticky=(N,S))
        self.listPlayers['yscrollcommand'] = scrollPlayers.set
        self.listPlayers.grid(column=0, row=1)

        # down left
        # this should have all the data for team 1
        teamBlueFrame = ttk.Frame(self.content, width= 128, height=128)
        teamBlueFrame.grid(column=0, row=1)
        self.teamBlueLabel = ttk.Label(teamBlueFrame, text="Blue team")
        self.teamBlueLabel.grid(column=0, row=0)
        self.listBlue = Listbox(teamBlueFrame, height=5, width=52)
        self.listBlue.grid(column=0, row=1)

        laneFrame = ttk.Frame(self.content, width=128, height=128)
        laneFrame.grid(column=1, row=1)
        labeltop = ttk.Label(laneFrame, text=" ")
        labeltop.grid(column=0, row=0)
        labeljung = ttk.Label(laneFrame, text="Top")
        labeljung.grid(column=0, row=1)
        labelmid = ttk.Label(laneFrame, text="Jungler")
        labelmid.grid(column=0, row=2)
        labeladc = ttk.Label(laneFrame, text="Midlaner")
        labeladc.grid(column=0, row=3)
        labelsup = ttk.Label(laneFrame, text="ADC")
        labelsup.grid(column=0, row=4)
        labelsup = ttk.Label(laneFrame, text="Support")
        labelsup.grid(column=0, row=5)

        # down right
        # this should have all the data for team 2
        teamRedFrame = ttk.Frame(self.content, width= 128, height=128)
        teamRedFrame.grid(column=2, row=1, padx=16, pady=16)
        self.teamRedLabel = ttk.Label(teamRedFrame, text="Red team")
        self.teamRedLabel.grid(column=0, row=0)
        self.listRed = Listbox(teamRedFrame, height=5, width=52)
        self.listRed.grid(column=0, row=1)


        """self.frame = ttk.Frame(content)
        entry = ttk.Entry(self.root)
        self.txt = Text(self.root, height=10, width=50)
        self.bt = Button(self.frame, text="Generate!",width=20, command=lambda: self.generate_teams())
        self.ls = Listbox(content, height=5, width=30)
        self.ls2 = Listbox(content, height=5, width=30)
        self.pf_button = Button(self.frame, text="Show Profile",width=20, command=lambda: self.show_profile(Profile))
        self.t1 = Label(content, text="Team 1")
        self.t2 = Label(content, text="Team 2")
        lblFr1 = LabelFrame(content, height=100, width=200)
        lblFr2 = LabelFrame(content, height=100, width=200)

        positions = constants.positions
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
            name = None
            try:
                name = self.ls.get(self.ls.curselection()[0])
            except IndexError:
                try:
                    name = self.ls2.get(self.ls2.curselection()[0])
                except IndexError:
                    name = None
            if name:
                self.new = Toplevel(self.root)
                _class(self.new, name, self.c)"""

    def show_profile(self, _class):
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            name = None
            try:
                name = self.listAll.get(self.listAll.curselection()[0])
            except IndexError:
                try:
                    name = self.ls2.get(self.ls2.curselection()[0])
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

    def generateGame(self):
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
