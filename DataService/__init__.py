from riotwatcher import LolWatcher, ApiError
import Model
import json
import requests
import shutil

class DataService:
    def __init__(self, APIKey, region):
        self.watcher = LolWatcher(APIKey)
        self.region = region
        self.version = self.watcher.data_dragon.versions_for_region(self.region)
        player_json = "../assets/player_dictionaries"
        file = open(player_json, "r")
        self.player_dict = json.load(file)
        for x in self.player_dict:
            self.player_dict[x] = Model.from_dict(self.player_dict[x])
        file.close()
        print(self.player_dict)

    def get_player(self, name):
        if name in self.player_dict:
            return self.player_dict[name]
        summoner = self.watcher.summoner.by_name(self.region, name)
        player = Model.Player(name, summoner['id'])
        rank = self.watcher.league.by_summoner(self.region, summoner['id'])
        if summoner['summonerLevel'] <= 30:
            player.set_elo("LVL30")
        elif rank == []:
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
        try:
            summoner = self.watcher.summoner.by_name(self.region, name)
            pfversion = self.version['n']['profileicon']
            iconUrl = 'http://ddragon.leagueoflegends.com/cdn/'+ pfversion +'/img/profileicon/' \
                      + str(summoner['profileIconId']) + '.png'
            response = requests.get(iconUrl, stream=True)
            with open('../assets/SummonerIcons/img.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            return "../assets/SummonerIcons/img.png"
        except:
            return "../assets/SummonerIcons/default_icon.png"

    def get_rank(self, name):
        summoner = self.watcher.summoner.by_name(self.region, name)
        try:
            return self.watcher.league.by_summoner(self.region, summoner['id'])[0]['tier']
        except:
            return "UNRANKED"


