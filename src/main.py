import rconutil
import pprint
import json

host, port, password = "", -1, ""

with open("./creds.json", "r") as file:
    content = file.read()
    json_data = json.loads(content)
    
    host = json_data["host"]
    port = json_data["port"]
    password = json_data["password"]


# Yeah we rewriting, what u gonna do bout it? :D
# Here's the plan I write to versions.
# core is going to have base rcon this can be used however
# secure will have a rcon client and server with P2P socket encryption

# run this rconutil in the same machine as the game server with rcon
# then connect to the game server rcon through the custom rcon server
# you now have encrypted rcon connection to your game server!
