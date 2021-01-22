import json
import discord
import time
import heapq as hq
import riotwatcher
from discord.ext.commands import bot

playersTeam1 = ["Marcos", "Roger", "Ivy", "Buildcrash", "Oscar"]
playersTeam2 = ["test1", "test2", "test3", "test4", "test5"]
client = discord.Client()
json_file = open("C:/Users/Topik/Desktop/GitHub Projects/LeagueCustoms/assets/token.json", "r", encoding="utf-8")
token = json.load(json_file)
json_file.close()


@client.event
async def on_ready():
    print("Buenos días")


@client.event
async def on_message(message):
    emoji = '🔥'
    reactionList = []


    if message.content == "-leaders":
        await message.channel.send("Así va el número de MVP's: ")

    elif message.content == "-test":
        await message.channel.send("¿Quién ha sido el MVP?")

        await message.channel.send("\n **TEAM 1**")
        for x in playersTeam1:
            name = "```css\n[" + x + "]\n```"
            m = await message.channel.send(name)
            await m.add_reaction(emoji)
            reactionList.append(m.id)

        await message.channel.send("\n **TEAM 2**")
        for y in playersTeam2:
            name = "```ini\n[" + y + "]\n```"
            m = await message.channel.send(name)
            await m.add_reaction(emoji)
            reactionList.append(m.id)

        time.sleep(5)
        listaVotos = await votesRecount(reactionList, emoji)
        await winners(listaVotos,message)



async def votesRecount(reactionList, emoji):
    fire_list = []
    cont = 0
    usuarios_visited = set()
    usuarios_ban = set()
    usuarios_visited.add(801838385773674516)
    for x in reactionList:
        channel = client.get_channel(724043110178357250)
        message = await channel.fetch_message(x)
        for y in message.reactions:
            if y.emoji == emoji:
                async for user in y.users():
                    if user.id not in usuarios_visited:
                        usuarios_visited.add(user.id)
                    else:
                        usuarios_ban.add(user.id)

    for x in reactionList:
        channel = client.get_channel(724043110178357250)
        message = await channel.fetch_message(x)
        for y in message.reactions:
            cont = 0
            if y.emoji == emoji:
                async for user in y.users():
                    if user.id in usuarios_ban:
                        cont+= 1

                name = message.content
                name = name[8:-5]
                hq.heappush(fire_list, ((y.count * -1) + cont, name))

    return fire_list


async def winners(listaVotos,message):
    listaMVP = []
    mvp_check = False
    max_vots = True
    maxNumber = 100

    for x in listaVotos:
        if x[0] != 0:
            mvp_check = True

    if mvp_check == False:
        await message.channel.send("No hay MVP :( ")

    else:
        listaMVP.append(hq.heappop(listaVotos))
        while max_vots:
            temp = hq.heappop(listaVotos)
            if temp[0] == listaMVP[0][0]:
                listaMVP.append(temp)
            else:
                max_vots = False
        if len(listaMVP) == 1:
            await message.channel.send("El MVP ha sido: 🙌 **" + hq.heappop(listaMVP)[1] + "** 🙌")
        else:
            await message.channel.send("Los MVP's han sido: ")
            for x in listaMVP:
                await message.channel.send("🙌 ** " + x[1] + " ** 🙌")


client.run(token["token"])
