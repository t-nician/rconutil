import json
import rconutil


host, port, password = "", -1, ""


with open("creds.json", "r") as file:
    content = file.read()
    data = json.loads(content)

    host = data["host"]
    port = data["port"]
    password = data["password"]


print(rconutil.data.Packet(
    type=rconutil.data.SendPacketType.SERVERDATA_AUTH,
    data=b"serverpassword"
))