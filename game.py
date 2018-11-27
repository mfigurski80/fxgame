import urllib.request, json, datetime


# UTILITY FUNCTIONS
def getJSONFrom(urlToGet):
    print("\t[getting from '" + urlToGet + "']")
    with urllib.request.urlopen(urlToGet) as response:
        data = json.loads(response.read().decode())
        return data
def JSONToFile(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
def FileToJSON(filename):
    try:
        with open(filename) as infile:
            data = json.load(infile)
            return data
    except:
        return None
def timestampToDate(stamp):
    return datetime.datetime.fromtimestamp(stamp).isoformat()

def getFXData(url, key):
    return getJSONFrom(url + "?access_key=" + key)




# HARD SETTINGS
save_file_name = "save.json"
access_keys = ["bdf49805e3ef4e4fac1cf6251f5eae5c", "cc7a55586c597a9c83f7da90b76f9825"]
# access_key = "bdf49805e3ef4e4fac1cf6251f5eae5c"
url = "http://data.fixer.io/api/latest"

# Soft Settings (updateable)
state = {
    "username": "unknown user",
    "savedCur": {},
    "inventory": {"EUR":100},
    "rates": {},
    "ratesLastUpdated": 0,
}




# Executeable functions...
def help():
    print("\t" + state["username"])
    print("\tcommands currently available: ")
    print(commands.keys())

def quit():
    global isExit
    save()
    isExit = True
    print("\t[exiting...]")

def save():
    JSONToFile(state, save_file_name)
    print("\t[save successful]")

def load(filename = save_file_name):
    global state
    data = FileToJSON(filename)
    if data != None:
        state = data
        print("\t[load successful]")
    else:
        print("\t[load not successful. It's possible you do not have a save file yet]")

def setName(nameInArray):
    global state
    state["username"] = " ".join(nameInArray)

def viewInventory():
    totalValue = 0
    for i in state["inventory"].keys():
        print(i,": amount",state["inventory"][i])
        totalValue += state["inventory"][i] / state["rates"][0]["rt"][i]
    print("\tTotal Value: " + str(totalValue))

def printRates(args = []):
    if len(state["rates"]) == 0:
        print("\t[no rates found]")
        return

    if len(args) == 0:
        for i in state["rates"][0]["rt"].keys(): # use latest rates
            print(i, ":", state["rates"][0]["rt"][i])
    else:
        for rt in args:
            print(rt, ":", state["rates"][0]["rt"][rt])
    print("\tUpdated on " + timestampToDate(state["rates"][0]["timestamp"]))

def getRates(which_key = 0):
    global state
    data = getFXData(url, access_keys[which_key])
    if data["success"] == False: # if not successful, try next key
        print("\t[rate retrieval was unsuccessful.]")
        getRates(which_key = which_key+1)
    state["rates"].insert(0,{"rt":data["rates"],"timestamp": data["timestamp"]})
    print("\t[successfully retrieved current rates]")
    if len(state["rates"]) > 5: # make sure list doesn't go over 5
        state["rates"].pop()

def buy(args):
    global state
    name = args[0]
    amount = int(args[1])

    rate = state["rates"][0]["rt"][name]
    cost = amount / rate
    if cost > state["inventory"]["EUR"]:
        print("[not enough EUR to complete purchase]")
        return
    state["inventory"]["EUR"] -= cost
    if name in state["inventory"].keys():
        state["inventory"][name] += amount
    else:
        state["inventory"][name] = amount
    print("[transaction complete. Payed " + str(cost) + " EUR]")

def sell(args):
    global state
    name = args[0]
    amount = int(args[1])

    rate = state["rates"][0]["rt"][name]
    cost = amount / rate
    state["inventory"]["EUR"] += cost
    state["inventory"][name] -= amount
    if state["inventory"][name] == 0: # if no more of asset
        del state["inventory"][name]
    print("[transaction complete. Earned " + str(cost) + " EUR]")


# list of typeable commands
commands = {
    "help": help,
    "q": quit,
    "quit": quit,
    "exit": quit,
    "save": save,
    "load": load,
    "setName": setName,
    "assets": viewInventory,
    "rates": printRates,
    "getRates": getRates,
    "buy": buy,
    "sell": sell
}


load() # load right away
print("Welcome back, " + state["username"])
# controlling loop!!
isExit = False
while not isExit:
    inp = input().split(" ")
    if inp[0] in commands:
        if len(inp) == 1:
            commands[inp[0]]()
        else:
            commands[inp[0]](inp[1:])
