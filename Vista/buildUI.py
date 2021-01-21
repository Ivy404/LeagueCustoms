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
        self.c = Controller.Controller('RGAPI-179ffd3e-16c3-49fa-b440-6143b07bfc61', 'euw1')
        self.root = root
        self.root.resizable(width=False, height=False)

        self.content = Frame(self.root, width=1512, height=1512)
        self.root.title("League Customs")
        self.content.grid(column=0, row=0)

        # Up left
        repositoriFrame = Frame(self.content, width=128, height=128)
        repositoriFrame.grid(column=0, row=0, padx=16, pady=16)
        # add user to list
        addToAll = Button(repositoriFrame, text='Register', command=lambda: self.register_user())
        addToAll.grid(column=0, row=0, sticky=(N, W, E, S))
        # list of all users
        self.listAll = Listbox(repositoriFrame, height=10, width=52)
        scrollAll = Scrollbar(repositoriFrame, orient=VERTICAL, command=self.listAll.yview)
        scrollAll.grid(column=1, row=1, sticky=(N, S))
        self.listAll['yscrollcommand'] = scrollAll.set
        self.listAll.grid(column=0, row=1)
        self.update_player_list()

        # up mid
        self.mid_bar = Frame(self.content, width=128, height=128)
        self.mid_bar.grid(column=1, row=0, padx=16, pady=16)
        # add user to game
        self.addToGame = Button(self.mid_bar, text='Add >>', command=lambda: self.addUser())
        self.addToGame.grid(column=0, row=0, pady=8, sticky=(W, E))
        # remove user from game
        self.removeFromGame = Button(self.mid_bar, text='<< Remove', command=lambda: self.removeUser())
        self.removeFromGame.grid(column=0, row=1, pady=8, sticky=(W, E))
        self.profile = Button(self.mid_bar, text='Profile', command=lambda: self.show_profile())
        self.profile.grid(column=0, row=2, pady=8, sticky=(W, E))
        self.generateGame = Button(self.mid_bar, text='Generate', command=lambda: self.generate_game())
        self.generateGame.grid(column=0, row=3, pady=8, sticky=(W, E))

        # up right
        self.playerNotebook = ttk.Notebook(self.content)
        self.playerNotebook.grid(column=2, row=0, padx=16, pady=16)
        self.playerFrame = Frame(self.playerNotebook, width=128, height=128)
        self.playerFrame.grid(column=0, row=0, padx=16, pady=16)
        self.lobbyFrame = Frame(self.playerNotebook, width=128, height=128)
        self.lobbyFrame.grid(column=0, row=0)

        self.txt = Text(self.lobbyFrame, height=10, width=39)
        self.txt.grid(column=0, row=0)

        self.playerNotebook.add(self.playerFrame, text="From List", padding=10)
        self.playerNotebook.add(self.lobbyFrame, text="From Lobby", padding=10)

        self.playerNotebook.bind("<<NotebookTabChanged>>", )
        # this should be a list of the users that will play
        self.listPlayers = Listbox(self.playerFrame, height=10, width=52)
        self.listPlayers.grid(column=0, row=1)

        # down left
        # this should have all the data for team 1
        self.teamBlueFrame = Frame(self.content, width=128, height=128)
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
        self.teamRedFrame = Frame(self.content, width=128, height=128)
        self.teamRedFrame.grid(column=2, row=1, padx=16, pady=16)
        self.teamRedLabel = Label(self.teamRedFrame, text="Red team")
        self.teamRedLabel.grid(column=0, row=0)
        self.listRed = Listbox(self.teamRedFrame, height=5, width=52)
        self.listRed.grid(column=0, row=1)

    def show_profile(self):
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
                self.new.title(name + "'s Profile")
                Profile(self.new, name, self.c)

    def register_user(self):
        try:
            if self.new.state() == "normal":
                self.new.focus()
        except:
            self.new = Toplevel(self.root)
            self.new.title("Register User")
            Register(self.new, self.c)

    def removeUser(self):
        if 0 < len(self.listPlayers.curselection()):
            UsersGame.remove(self.listPlayers.get(self.listPlayers.curselection()[0]))
            self.listPlayers.delete(self.listPlayers.curselection()[0])

    def addUser(self):
        if (0 < len(self.listAll.curselection()) and self.listPlayers.size() < MaxPlayers
                and not self.listAll.get(self.listAll.curselection()[0]) in UsersGame):
            user = self.listAll.get(self.listAll.curselection()[0])
            UsersGame.add(user)
            self.listPlayers.insert('end', user)
            if self.listAll.curselection()[0] + 1 < self.listAll.size():
                select = self.listAll.curselection()[0] + 1
                self.listAll.select_clear(select - 1)
                self.listAll.selection_set(select)

    def update_player_list(self):
        self.listAll.delete(0, END)
        playersAll = list()
        for i in self.c.player_list.players:
            playersAll.append(i)
        playersAll = sorted(playersAll, key=lambda x: x.lower())
        j = 0
        for i in playersAll:
            self.listAll.insert('end', i)
            if j % 2:
                self.listAll.itemconfigure(j, background='#AEB7B3')
            else:
                self.listAll.itemconfigure(j, background='#E1EFE6')
            j += 1

    def generate_game(self):
        if self.playerNotebook.index("current") < 1:
            # print("generating game from list")
            if 9 < self.listPlayers.size():
                # self.c.
                self.listBlue.delete(0, END)
                self.listRed.delete(0, END)
                lobbyText = ""
                for p in self.listPlayers.get(0, 10):
                    lobbyText += p + " joined the lobby\n"
                f = open("../Controller/text_test", "w", encoding="utf8")
                print(lobbyText, file=f)
                f.close()

                team1, team2 = self.c.new_game("../Controller/text_test")
                self.c.close()
                for x in team1.players:
                    self.listBlue.insert('end', x)
                for x in team2.players:
                    self.listRed.insert('end', x)
                self.teamBlueLabel.config(text="Blue Team's Rating -> " + str(int(team1.rating())))
                self.teamRedLabel.config(text="Red Team's Rating -> " + str(int(team2.rating())))
                self.listBlue.update()
                self.listRed.update()
        else:
            # print("generating game from lobby")
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
            self.teamBlueLabel.config(text="Blue Team's Rating -> " + str(int(team1.rating())))
            self.teamRedLabel.config(text="Red Team's Rating -> " + str(int(team2.rating())))
            self.listBlue.update()
            self.listRed.update()
            self.update_player_list()


class Register:
    def __init__(self, root, ctr):

        self.root = root

        self.outer_frame = Frame(self.root)
        self.name_frame = Frame(self.outer_frame,height=50, width=420)
        self.profile_frame = Frame(self.outer_frame, height=500, width=420)

        self.name_label = Label(self.outer_frame, text="Summoner Name:", font="Helvetica 14")
        self.name_entry = Entry(self.outer_frame, font = "Helvetica 14 bold")

        self.name_label.place(x=10,y=10)
        self.name_entry.place(x=180,y=12)

        self.outer_frame.grid(column=0, row=0)
        self.name_frame.grid(column=0, row=0)


class Profile:
    def __init__(self, root, name, ctr):

        self.root = root

        self.outer_frame = Frame(self.root)
        self.left_frame = Frame(self.outer_frame)
        self.right_frame = Frame(self.outer_frame)
        self.role_frame = Frame(self.right_frame)
        self.ctr = ctr
        self.name = name
        # Labels, Combobox, etc.

        # El Exum
        _role = ctr.get_role(self.name)
        if self.name == "Kite Machine 2": self.name = "El Exum"

        self.nameLabel = Label(self.right_frame, text=self.name, font="none 24 bold")
        self.role = Label(self.role_frame, text="Role:")
        self.role_combo = ttk.Combobox(self.role_frame,state="readonly", values=constants.positions)
        self.role_combo.current(0)
        if(_role in constants.positions):
            self.role_combo.current(constants.positions.index(_role))
        self.role.grid(column=0, row=0)
        self.role_combo.grid(column=1, row=0)
        self.rating = Label(self.role_frame, text="Rating:")
        self.rating.grid(column=0, row=1)

        self.applyButton = Button(self.role_frame, text='Apply', command=lambda: self.update_role())
        self.applyButton.grid(column=2, row=0)

        # Rank image
        rank = ctr.get_rank(self.name)
        self.load_rank = Image.open("../assets/ranked_emblems/Emblem_" + rank[0] + rank[1:len(rank)].lower() + ".png")
        # El Exum
        if self.name == "El Exum": self.load_rank = Image.open("../assets/ranked_emblems/Emblem_Challenger.png")

        self.load_rank.thumbnail((128, 128), Image.ANTIALIAS)
        self.render_rank = ImageTk.PhotoImage(self.load_rank)
        self.rank_img = Label(self.left_frame, image=self.render_rank)
        self.rank_img.image = self.render_rank

        # Profile image
        imgFile = ctr.get_icon(self.name)
        self.load_prof = Image.open(imgFile)
        # El Exum
        if self.name == "El Exum": self.load_prof = Image.open("../assets/SummonerIcons/default_icon.jpg")

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
        self.nameLabel.grid(column=0, row=0)
        self.role_frame.grid(column=0, row=1, pady=50)

        self.outer_frame.pack()

    def update_role(self):
        self.ctr.set_role(self.name, self.role_combo.get())


rt = Tk()
app = MainWindow(rt)
rt.mainloop()
