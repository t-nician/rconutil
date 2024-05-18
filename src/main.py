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


client = rconutil.client.RconClient(
    host=host,
    port=port,
    password=password
)

success = client.login()

empty_packet = rconutil.data.RconPacket(
    type=rconutil.data.SendPacketType.SERVERDATA_EXECCOMMAND,
    data=b"chatlog 7B24F811488928B4 10",
    id=2
)

while True:
    pprint.pprint(client.send(empty_packet).response_packets)