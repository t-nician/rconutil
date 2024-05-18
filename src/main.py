import rconutil
import json

host, port, password = "", -1, ""

with open("./creds.json", "r") as file:
    content = file.read()
    json_data = json.loads(content)
    
    host = json_data["host"]
    port = json_data["port"]
    password = json_data["password"]


login_packet = rconutil.data.RconPacket(
    type=rconutil.data.SendPacketType.SERVERDATA_AUTH,
    data=password,
    id=5
)
