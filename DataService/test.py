import json
file = open("../assets/player_dictionaries", "w")

dic = {'ABC': '123', 'DEF' : '456'}
file.write(json.dumps(dic))
file.close()

file = open("../assets/player_dictionaries", "r")
player_dict = json.load(file)

print(player_dict)