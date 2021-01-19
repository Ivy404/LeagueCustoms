from DataService import DataService
from Model import PlayerList
from Model import CustomGame


def joined(text):
    f = open(text, encoding="utf-8")

    text = "joined the lobby"
    players = []

    for x in f.readlines():
        offset = 2 if x[len(x) - 1] == "\n" else 1
        players.append(x[:len(x) - offset - len(text)])
    return players[:10]


class Controller:
    def __init__(self, key, region):
        self.data_service = DataService(key, region)
        self.player_list = PlayerList()
        self.init_lists()

    def init_lists(self):
        for x in self.data_service.player_dict.values():
            self.player_list.add_player(x)

    def new_game(self, text):
        players = joined(text)
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




# c = Controller('RGAPI-7f36b2d1-e00d-45e8-b38d-0c7ca26ce610', 'euw1')
#
# c.new_game("../Controller/text_test")
# c.close()
