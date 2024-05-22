import rconutil
import socket
import json

host, port, password = "", -1, ""

with open("./creds.json", "r") as file:
    content = file.read()
    json_data = json.loads(content)
    
    host = json_data["host"]
    port = json_data["port"]
    password = json_data["password"]


client = rconutil.core.client.RconClient(
    host=host,
    port=port,
    password=password
)

client.login()

print(client.send(rconutil.core.data.RconPacket(
    type=rconutil.core.data.SendPacketType.SERVERDATA_EXECCOMMAND,
    data=b"stats"
)))