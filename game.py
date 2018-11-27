import urllib.request, json


# UTILITY FUNCTIONS
def getJSONFrom(urlToGet):
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

def getFXData(url, key):
    return getJSONFrom(url + "?access_key=" + key)




# HARD SETTINGS
save_file_name = "save.json"
access_key = "bdf49805e3ef4e4fac1cf6251f5eae5c"
url = "http://data.fixer.io/api/latest"

# Soft Settings (updateable)
state = {
    "username": "unknown user",
    "savedCur": {},
    "inventory": {"EUR":100},
    "rates": {},
    "ratesLastUpdated": 0
}




# Executeable functions...
def quit():
    global isExit
    isExit = True

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
        print("\t[load not successful]")

def setName(nameInArray):
    global state
    state["username"] = " ".join(nameInArray)

def printRates():
    for i in state["rates"].keys():
        print(i, ":", state["rates"][i])

# list of typeable commands
commands = {
    "q": quit,
    "quit": quit,
    "exit": quit,
    "save": save,
    "load": load,
    "setName": setName,
    "rates": printRates,
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
