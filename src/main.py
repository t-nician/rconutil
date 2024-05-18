import rconutil

client = rconutil.client.RconClient()



client.load_creds_from_json_file("./creds.json")

client.connect()

response = client.send(
    rconutil.data.RconPacket(
        type=rconutil.data.SendPacketType.SERVERDATA_EXECCOMMAND,
        data=b"stats"
    )
)

print(response.response_packets[0])

client.keep_alive()