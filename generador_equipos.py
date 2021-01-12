
def joined(text):
    f = open(text, encoding="utf-8")
    out = open("output","w")

    text = "joined the lobby"
    players = []

    for x in f.readlines():
        offset = 2 if x[len(x) - 1] == "\n" else 1
        players.append(x[:len(x)-offset-len(text)])
    return players

print(joined("text_test"))


