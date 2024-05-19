import rconutil
import asyncio
import json

host, port, password = "", -1, ""

with open("./creds.json", "r") as file:
    content = file.read()
    json_data = json.loads(content)
    
    host = json_data["host"]
    port = json_data["port"]
    password = json_data["password"]



async def main():
    rcon_client = rconutil.client.RconClient(
        host=host,
        port=port,
        password=password
    )

    await rcon_client.login()
    
    response = await rcon_client.send(
        command_packet=rconutil.data.RconPacket(
            type=rconutil.data.SendPacketType.SERVERDATA_EXECCOMMAND,
            data=b"stats",
            id=99
        )
    )

    print(response)



asyncio.run(main())