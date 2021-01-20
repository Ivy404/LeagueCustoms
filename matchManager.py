from riotwatcher import LolWatcher, ApiError

watcher = LolWatcher('RGAPI-580545bf-2972-45f2-a1df-3bf5e8fe6f96')

region = 'euw1'

# x = input("summoner name:")

x = 'Unkindłed One'
me = watcher.summoner.by_name(region, x)

print(me)

# versions = watcher.data_dragon.versions_for_region(region)
# champs = versions['n']['champion']
#
# current_list = watcher.data_dragon.champions(champs)

# check league's latest version
latest = watcher.data_dragon.versions_for_region(region)['n']['champion']
# Lets get some champions static information
static_champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

# print(watcher.data_dragon.profile_icons(latest))

# champ static list data to dict for looking up
champ_dict = {}
for key in static_champ_list['data']:
    row = static_champ_list['data'][key]
    champ_dict[row['key']] = row['id']

print("rank solo/duo: ")
print(watcher.league.by_summoner(region, me['id']))

my_matches = watcher.match.matchlist_by_account('euw1', me['accountId'])

last_match = my_matches['matches'][3]
match_detail = watcher.match.by_id(region, last_match['gameId'])

counter = 0

# for x in match_detail:
#     if x == 'participants':
#         print('participants :')
#         for y in match_detail[x]:
#             print('\t' , match_detail[x][counter]['participantId'])
#             for z in match_detail[x][counter]:
#                 print('\t\t' + z,':', match_detail[x][counter][z])
#             counter += 1
#     else:
#         print(x, ':', match_detail[x])

#
# participants = []
# for row in match_detail['participants']:
#     participants_row = {}
#     participants_row['champion'] = row['championId']
#     participants_row['win'] = row['stats']['win']
#     participants_row['kills'] = row['stats']['kills']
#     participants_row['deaths'] = row['stats']['deaths']
#     participants_row['assists'] = row['stats']['assists']
#     participants.append(participants_row)
# #print([match_detail[x] for x in match_detail])
# print(match_detail['participants'])
# for x in participants[0]:
#     print(x, end = '\t\t')
# print('championName')
# for x in participants:
#     for y in x:
#         print(x[y], end = '\t\t\t')
#     print(champ_dict[str(x['champion'])])
# print([x for x in current_list['data']])