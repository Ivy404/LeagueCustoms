from riotwatcher import LolWatcher, ApiError
import Model
import json
import requests
import shutil

class DataService:
    def __init__(self, APIKey, region):
        self.watcher = LolWatcher(APIKey)
        self.region = region
        player_json = "../assets/player_dictionaries"
        file = open(player_json, "r")
        self.player_dict = json.load(file)
        for x in self.player_dict:
            self.player_dict[x] = Model.from_dict(self.player_dict[x])
        file.close()

    def get_player(self, name):
        if name in self.player_dict:
            return self.player_dict[name]
        summoner = self.watcher.summoner.by_name(self.region, name)
        player = Model.Player(name, summoner['id'])
        rank = self.watcher.league.by_summoner(self.region, summoner['id'])
        if rank == []:
            player.set_elo("UNRANKED")
        else:
            player.set_elo(rank[0]['tier'])
        self.player_dict[name] = player
        return player

    def generate_dics(self, ls):
        plist = []
        for x in ls:
            plist.append(self.get_player(x))
        return plist

    def set_player_dict(self, dic):
        self.player_dict = dic

    def save_to_file(self):
        file = open("../assets/player_dictionaries", "w")
        dc = dict()
        for x in self.player_dict:
            dc[x] = self.player_dict[x].to_dict()
        file.write(json.dumps(dc))
        file.close()

    def remove_from_file(self, name):
        file = open("../assets/player_dictionaries", "r")
        self.player_dict = json.load(file)
        for x in self.player_dict:
            if x != name:
                self.player_dict[x] = Model.from_dict(self.player_dict[x])
        file.close()
        file = open("../assets/player_dictionaries", "w")
        dc = dict()
        for x in self.player_dict:
            dc[x] = self.player_dict[x].to_dict()
        file.write(json.dumps(dc))
        file.close()

    def get_icon(self, name):
        summoner = self.watcher.summoner.by_name(self.region, name)
        iconUrl = 'http://ddragon.leagueoflegends.com/cdn/11.1.1/img/profileicon/' \
                  + str(summoner['profileIconId']) + '.png'
        response = requests.get(iconUrl, stream=True)
        with open('../assets/SummonerIcons/img.png', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

