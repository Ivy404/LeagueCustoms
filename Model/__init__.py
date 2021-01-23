from Model import constants

def from_dict(dic):
    p = Player("","")
    p.name = dic["NAME"]
    p.id = dic["ID"]
    p.elo = dic["ELO"]
    p.role = dic["ROLE"]
    p.rank = dic["RANKED"]
    return p


class Player:
    # Iron-Silver: 4, Gold:3 , Platinum-Diamond: 2, Master+: 1

    def __init__(self, name, ID):
        self.name = name
        self.id = ID
        self.elo = 0
        self.role = ""
        self.rank = ""

    def set_elo(self, elo):
        self.rank = elo
        if elo == "IRON" or elo == "BRONZE" or elo == "LVL30":
            self.elo = 1
        elif elo == "SILVER" or elo == "UNRANKED":
            self.elo = 2
        elif elo == "GOLD":
            self.elo = 3
        elif elo == "PLATINUM" or elo == "DIAMOND":
            self.elo = 4
        else:
            self.elo = 5

    def set_role(self, role):
        self.role = role

    def get_role(self):
        return self.role

    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.elo < other.elo

    def to_dict(self):
        return {"NAME": self.name,"ID": self.id,"ELO": self.elo, "ROLE" : self.role, "RANKED" : self.rank}


class Team:
    def __init__(self):
        self.players = list()
        self.positions = constants.positions[1:]

    def randomize_positions(self):
        import random
        random.shuffle(self.players)

    def add_player(self, player):
        self.players.append(player)

    def rating(self):
        rating = 0
        c = 0
        for x in self.players:
            if self.positions[c] == x.role:
                rating += x.elo*0.5
            rating += x.elo
            c += 1
        return float(rating)

    def get_players(self):
        return self.players

    def __str__(self):
        st = "Rating \t------->  " + str(self.rating()) + "\n"
        for x in range(len(self.players)):
            st += self.positions[x] + ": \t" + str(self.players[x]) + "\n"
        return st


class CustomGame:
    def __init__(self, ls):
        self.players = ls

    def get_by_id(self, id):
        for x in self.players:
            if x.id == id:
                return x

    def generate_teams(self):
        exit = False
        prm = 0.5
        while not exit:
            c = 0
            team1 = Team()
            team2 = Team()
            subgroups = {}
            for x in self.players:
                if not x.elo in subgroups:
                    subgroups[x.elo] = [x]
                else:
                    subgroups[x.elo].append(x)
            for x in subgroups:
                import random
                random.shuffle(subgroups[x])
                for y in subgroups[x]:
                    if c % 2: team1.add_player(y)
                    else: team2.add_player(y)
                    c += 1

            team1.randomize_positions()
            team2.randomize_positions()
            if abs(team1.rating() - team2.rating()) < (1 + prm):
                exit = True
            else:
                prm += 0.1
        return team1, team2


class PlayerList:
    def __init__(self):
        self.players = dict()

    def get_players_by_elo(self,ls):
        order = []
        for x in ls:
            if x in self.players:
                order.append((self.players[x].elo, self.players[x]))
        sorted(order)
        return [x[1] for x in order]

    def __contains__(self, item):
        return item in self.players

    def add_player(self, player):
        self.players[player.name] = player

    def set_role(self, name, role):
        if name in self.players:
            self.players[name].set_role(role)

    def get_role(self, name):
        if name in self.players:
            return self.players[name].get_role()

    def get_rating(self, name):
        return self.players[name].elo


