import json
import sys

from rconutil.core import server, client, packet

host, port, password = "", -1, ""

with open("./creds.json", "r") as file:
    content = file.read()
    json_data = json.loads(content)
    
    host = json_data["host"]
    port = json_data["port"]
    password = json_data["password"]


if sys.argv[1] == "server":
    rcon_server = server.RconServer(
        host='127.0.0.1',
        port=5000,
        password=password
    )

    rcon_server.run()
else:
    rcon_client = client.RconClient(
        host='127.0.0.1',
        port=port,
        password=password
    )

    #rcon_client.login()
    rcon_client._socket.connect((rcon_client.host, rcon_client.port))
    print(
        rcon_client.send(
            packet.RconPacket(
                type=packet.SendPacketType.SERVERDATA_EXECCOMMAND, 
                data=b"stats"
            )
        )
    )