import json
import discord
import riotwatcher

playersTeam1 = ["Marcos", "Roger", "Ivy", "Buildcrash", "Oscar"]
playersTeam2 = ["test1", "test2", "test3", "test4", "test5"]
client = discord.Client()
json_file = open("C:/Users/Topik/Desktop/GitHub Projects/LeagueCustoms/assets/token.json", "r", encoding= "utf-8")
token = json.load(json_file)
json_file.close()


@client.event
async def on_ready():
    print("Buenos días")


@client.event
async def on_message(message):
    emoji = '🔥'
    if message.content == "-leaders":
        await message.channel.send("Así va el número de MVP's: ")

    elif message.content == "-test":
        await message.channel.send("¿Quién ha sido el MVP?")

        await message.channel.send("\n **TEAM 1**")
        for x in playersTeam1:
            name = "```css\n[" + x + "]\n```"
            m = await message.channel.send(name)
            await m.add_reaction(emoji)

        await message.channel.send("\n **TEAM 2**")
        for y in playersTeam2:
            name = "```ini\n[" + y + "]\n```"
            m = await message.channel.send(name)
            await m.add_reaction(emoji)










client.run(token["token"])
