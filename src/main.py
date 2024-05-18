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


login_packet = rconutil.data.RconPacket(
    type=rconutil.data.SendPacketType.SERVERDATA_AUTH,
    data=password.encode(),
)


sesh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sesh.connect((host, port))
print(login_packet.to_bytes())
sesh.send(login_packet.to_bytes())

print("a", sesh.recv(4096))