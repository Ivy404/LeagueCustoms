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
        self.c = Controller.Controller('RGAPI-45572e6e-d70d-46b2-8c7e-862917c2dd92', 'euw1')
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

            if 9 < self.listPlayers.size():
                self.listBlue.delete(0, END)
                self.listRed.delete(0, END)
                #lobbyText = ""
                #for p in self.listPlayers.get(0, 10):
                #    lobbyText += p + " joined the lobby\n"

                team1, team2 = self.c.new_game(self.listPlayers.get(0,10))
                self.c.close()
                for x in team1.players:
                    self.listBlue.insert('end', x)
                for x in team2.players:
                    self.listRed.insert('end', x)
                self.teamBlueLabel.config(text="Blue Team's Rating -> " + str(team1.rating()))
                self.teamRedLabel.config(text="Red Team's Rating -> " + str(team2.rating()))
                self.listBlue.update()
                self.listRed.update()
        else:
            # print("generating game from lobby")
            self.listBlue.delete(0, END)
            self.listRed.delete(0, END)

            team1, team2 = self.c.new_game(Controller.joined(self.txt.get("1.0", END)))
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
            txt = self.txt.get("1.0", END)
            pos = txt.find(" joined the lobby")
            while (0 < pos and self.listPlayers.size() < 10):
                if(not txt[:pos] in UsersGame):
                    UsersGame.add(txt[:pos])
                    self.listPlayers.insert('end', txt[:pos])
                    txt = txt[pos + len(" joined the lobby") + 1:]
                    pos = txt.find(" joined the lobby")


class Register:
    def __init__(self, root, ctr):

        self.root = root
        self.ctr = ctr

        self.outer_frame = Frame(self.root)
        self.name_frame = Frame(self.outer_frame,height=50, width=475)
        self.profile_frame = Frame(self.outer_frame, height=256, width=475)
        self.button_frame = Frame(self.outer_frame,height=50, width=475)

        self.name_label = Label(self.name_frame, text="Summoner Name:") # , font="Helvetica 14"
        self.name_entry = Entry(self.name_frame, width=29) # , font = "Helvetica 11 bold"
        self.search_button = Button(self.name_frame, text="Search", width=14, command= lambda : self.search_func())

        self.name_label.place(x=10,y=10)
        self.name_entry.place(x=124,y=12)
        self.search_button.place(x=280,y=8)

        self.userName_label = Label(self.profile_frame, text="", justify=CENTER, width=16, font="none 24 bold")
        self.temp_label = Label(self.profile_frame, text="Summoner Name:", justify=CENTER)
        self.userName_label.place(x=186,y=24)
        self.temp_label.place(x=296,y=10)
        self.role_box = ttk.Combobox(self.profile_frame, state=DISABLED, values=constants.positions, width=29)
        self.role_box.current(0)
        self.role_box.place(x=10, y=224)
        self.load_rank = Image.open("../assets/ranked_emblems/Emblem_Unranked.png")
        self.load_rank.thumbnail((128, 128), Image.ANTIALIAS)
        self.render_rank = ImageTk.PhotoImage(self.load_rank)
        self.rank_img = Label(self.profile_frame, image=self.render_rank, width=180, height=180)
        self.rank_img.image = self.render_rank
        self.rank_img.place(x=256,y=64)
        # Profile image
        self.load_profile = Image.open("../assets/SummonerIcons/default_icon.jpg")
        self.load_profile.thumbnail((180, 180), Image.ANTIALIAS)
        self.render_profile = ImageTk.PhotoImage(self.load_profile)
        self.profile_img = Label(self.profile_frame, image=self.render_profile, relief=SUNKEN, borderwidth=10, width=180, height=180)
        self.profile_img.image = self.render_profile
        self.profile_img.place(x=10,y=10)

        self.add_button = Button(self.button_frame, text="Add", width=24, state=DISABLED, command= lambda : self.add_func())
        self.add_button.grid(column=0, row=0, padx=16, pady=16, sticky=(N,W,E,S))
        self.ok_button = Button(self.button_frame, text="Ok", width=24, state=DISABLED)
        self.ok_button.grid(column=1, row=0, padx=16, pady=16, sticky=(N,W,E,S))

        self.outer_frame.grid(column=0, row=0)
        self.name_frame.grid(column=0, row=0)
        self.profile_frame.grid(column=0, row=1)
        self.button_frame.grid(column=0, row=2)

    def search_func(self):
        image, rank, is_in = self.ctr.get_user(self.name_entry.get())
        self.load_profile = Image.open(image)
        self.render_profile = ImageTk.PhotoImage(Image.open(image).resize((180, 180), Image.ANTIALIAS))
        self.profile_img.config(image=self.render_profile)
        self.profile_img.image = self.render_profile
        self.load_rank = Image.open(rank)
        self.render_rank = ImageTk.PhotoImage(Image.open(rank).resize((180, 180), Image.ANTIALIAS))
        self.rank_img.config(image=self.render_rank)
        self.rank_img.image = self.render_rank
        if is_in:
            self.userName_label.config(text=self.name_entry.get())
            self.ok_button.config(state=DISABLED)
            self.add_button.config(state=DISABLED)
            self.role_box.config(state=DISABLED)
        else:
            self.userName_label.config(text=self.name_entry.get())
            self.ok_button.config(state=ACTIVE)
            self.add_button.config(state=ACTIVE)
            self.role_box.config(state="readonly")

    def add_func(self):
        self.ctr.add_user(self.userName_label.cget("text"), self.role_box.get())
        self.ctr.close()
        app.update_player_list()
        pass


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

        self.nameLabel = Label(self.right_frame, text=self.name, font="none 24 bold")
        self.role = Label(self.role_frame, text="Role:")
        self.role_combo = ttk.Combobox(self.role_frame,state="readonly", values=constants.positions)
        self.role_combo.current(0)
        if _role in constants.positions:
            self.role_combo.current(constants.positions.index(_role))
        self.role.grid(column=0, row=0)
        self.role_combo.grid(column=1, row=0)
        self.rating = Label(self.role_frame, text=("Rating: " + str(ctr.get_rating(self.name))))
        self.rating.grid(column=0, row=1)

        self.applyButton = Button(self.role_frame, text='Apply', command=lambda: self.update_role())
        self.applyButton.grid(column=2, row=0)

        # Rank image
        try:
            rank = ctr.get_rank(self.name)
            self.load_rank = Image.open("../assets/ranked_emblems/Emblem_" + rank[0] + rank[1:len(rank)].lower() + ".png")

            self.load_rank.thumbnail((128, 128), Image.ANTIALIAS)
            self.render_rank = ImageTk.PhotoImage(self.load_rank)
            self.rank_img = Label(self.left_frame, image=self.render_rank)
            self.rank_img.image = self.render_rank
        except:
            # Something went wrong
            self.load_rank = Image.open("../assets/ranked_emblems/Emblem_Unranked.png")
            self.load_rank.thumbnail((128, 128), Image.ANTIALIAS)
            self.render_rank = ImageTk.PhotoImage(self.load_rank)
            self.rank_img = Label(self.left_frame, image=self.render_rank)
            self.rank_img.image = self.render_rank

        # Profile image
        try:
            imgFile = ctr.get_icon(self.name)
            self.load_prof = Image.open(imgFile)

            self.load_prof.thumbnail((128, 128), Image.ANTIALIAS)
            self.render_prof = ImageTk.PhotoImage(self.load_prof)
            self.prof_img = Label(self.left_frame, image=self.render_prof, relief=SUNKEN, borderwidth=10)
            self.prof_img.image = self.render_prof
        except:
            self.load_prof = Image.open("../assets/SummonerIcons/default_icon.jpg")

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
