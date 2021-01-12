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
    return players


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
        print(team1)
        print(team2)

    def close(self):
        self.data_service.save_to_file()


c = Controller('RGAPI-e561662e-1ff0-4ee6-ba49-d112454fddf5', 'euw1')
c.new_game("text_test")
c.close()