from DataService import DataService
from Model import PlayerList, Player
from Model import CustomGame


def joined(text):
    players = []
    txt = text
    pos = txt.find(" joined the lobby")
    x = 0
    while (0 < pos):
        players.append(txt[:pos])
        txt = txt[pos + len(" joined the lobby") + 1:]
        pos = txt.find(" joined the lobby")
        x += 1
    return players

class Controller:
    def __init__(self, key, region):
        self.data_service = DataService(key, region)
        self.player_list = PlayerList()
        self.init_lists()

    def init_lists(self):
        for x in self.data_service.player_dict.values():
            self.player_list.add_player(x)

    def new_game(self, players):
        # players = joined(text)
        self.data_service.generate_dics(players)
        self.init_lists()
        plist = self.player_list.get_players_by_elo(players)
        cs = CustomGame(plist)
        team1, team2 = cs.generate_teams()
        return team1, team2

    def close(self):
        self.data_service.save_to_file()

    def set_role(self, name, role):
        self.player_list.set_role(name, role)

    def get_role(self, name):
        return self.player_list.get_role(name)

    def get_icon(self, name):
        return self.data_service.get_icon(name)

    def get_rank(self, name):
        return self.data_service.get_rank(name)

    def get_user(self, name):
        rank = "../assets/ranked_emblems/Emblem_"
        if name in self.player_list:
            rank = rank + self.get_rank(name)[0] + self.get_rank(name)[1:].lower() + ".png"
            return self.data_service.get_icon(name),rank,(name in self.player_list)
        else:
            try:
                rnm = self.data_service.get_rank(name)
                rank = rank + rnm[0] + rnm[1:].lower() + ".png"
                return self.data_service.get_icon(name), rank, (name in self.player_list)
            except:
                return "../assets/SummonerIcons/default_icon.jpg", "../assets/ranked_emblems/Emblem_Unranked.png",\
                       True

    def add_user(self, name, role):
        try:
            self.player_list.add_player(self.data_service.get_player(name))
            self.player_list.set_role(name, role)
            self.data_service.save_to_file()
        except:
            pass

    def get_rating(self, name):
        return self.player_list.get_rating(name)



# c = Controller('RGAPI-7f36b2d1-e00d-45e8-b38d-0c7ca26ce610', 'euw1')
#
# c.new_game("../Controller/text_test")
# c.close()
