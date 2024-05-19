import socket
import time

from rconutil import data
from dataclasses import dataclass, field

DEFAULT_SOCKET_TIMEOUT = 1

# id, expiry_time
receive_packet_id_timeout: dict[int, data.RconCommand] = {}


@dataclass
class RconClient:
    host: str
    port: int
    password: str
    _socket: socket.socket = field(
        default_factory=lambda: socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM
        )
    )

    def __post_init__(self):
        self._socket.settimeout(DEFAULT_SOCKET_TIMEOUT)


    async def send(self, command_packet: data.RconPacket) -> data.RconCommand:
        if receive_packet_id_timeout.get(command_packet.id) is not None:
            raise Exception(
                "A packet with that id is already waiting for responses!"
            )
        
        rcon_command = data.RconCommand(
            command_packet=command_packet
        )

        receive_packet_id_timeout[command_packet.id] = rcon_command

        self._socket.send(await command_packet.to_bytes())

        while True:
            try:
                received_packet = data.RconPacket(
                    data=self._socket.recv(4096)
                )
                
                if received_packet.id == command_packet.id:
                    rcon_command.response_packets.append(received_packet)
                elif receive_packet_id_timeout.get(received_packet.id):
                    receive_packet_id_timeout[received_packet.id].response_packets.append(
                        received_packet
                    )
                elif received_packet.id == 255:
                    rcon_command.response_packets.append(received_packet)

            except socket.error as _:
                break

        return rcon_command


    async def connect(self):
        self._socket.connect((self.host, self.port))


    async def login(self, password: str | None = None) -> data.RconCommand:
        await self.connect()
        return await self.send(
            command_packet=data.RconPacket(
                type=data.SendPacketType.SERVERDATA_AUTH,
                data=password or self.password
            )
        )
        