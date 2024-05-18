import rconutil
import pprint

client = rconutil.client.RconClient()

client.load_creds_from_json_file("./creds.json")
client.connect()

print(
    client.send(
        packet=rconutil.data.RconPacket(
            type=rconutil.data.SendPacketType.SERVERDATA_EXECCOMMAND,
            data=b"banlist",
            id=4
        )
    ).response_packets[0].to_bytes()
)

#client.keep_alive()