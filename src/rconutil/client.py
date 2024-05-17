import socket
import random

from rconutil import data
from dataclasses import dataclass, field


@dataclass
class RconClient:
    host: str = field(default="")
    port: int = field(default=-1)
    password: str | bytes = field(default="")

    _socket: socket.socket = field(
        default_factory=lambda: socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
    )

    def connect(self, password: str | bytes | None = None) -> bool:
        assert self.host != "", "No host provided to rcon!"
        assert self.port != -1, "No port provided to rcon!"

        self._socket.connect((self.host, self.port))

        assert password or self.password != "", "No password provided to rcon!"

        __password = password or self.password
        __id = random.randint(1, 100)

        if type(__password) is str:
            __password = __password.encode()

        login_packet = data.Packet(
            id=__id,
            data=__password,
            type=data.SendPacketType.SERVERDATA_AUTH,
        )
        
        self._socket.send(login_packet.data)

        response_packet: data.ReceivePacketType = None
        
        while response_packet is None:
            response = self._socket.recv(4096)
            print(response.decode("utf-8"))
            # TODO grab id from respones value and compare against target id
            break
        
        command_packet = data.Packet(
            id=__id,
            data="playerlist",
            type=data.SendPacketType.SERVERDATA_EXECCOMMAND
        )

        self._socket.send(command_packet.data)

        print(self._socket.recv(4096))
        



