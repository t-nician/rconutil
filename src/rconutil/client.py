import socket
import random
import time
import json
import os

from rconutil import data
from dataclasses import dataclass, field


KEEP_ALIVE_TIMEOUT_SECONDS = 1
SEND_RECEIVE_TIMEOUT_THRESHOLD = 5


@dataclass
class RconClient:
    host: str = field(default="")
    port: int = field(default=-1)
    password: str = field(default="")
    _socket: socket.socket = field(
        default_factory=lambda: socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
    )

    def __post_init__(self):
        self._socket.settimeout(SEND_RECEIVE_TIMEOUT_THRESHOLD)


    def load_creds_from_json_file(self, path: str):
        if os.path.exists(path):
            with open(path, "r") as file:
                content = file.read()
                json_data = json.loads(content)

                self.host = json_data["host"]
                self.port = json_data["port"]
                self.password = json_data["password"]


    def connect(
        self,
        host: str | None = None,
        port: int | None = None,
        password: str | None = None
    ):
        __host = host or self.host
        __port = port or self.port
        __password = password or self.password

        assert __host != "", f"Invalid host ip given! '{__host}'"
        assert __port != -1, f"Invalid port given! '{str(__port)}'"

        self._socket.connect((__host, __port))

        response_data = self.send(
            data.RconPacket(
                type=data.SendPacketType.SERVERDATA_AUTH,
                data=__password
            )
        )
        
        print(response_data.response_packets[0])
        
        return True
    

    def send(self, packet: data.RconPacket) -> data.RconCommand:
        rcon_command = data.RconCommand(command_packet=packet)
        
        self._socket.send(packet.to_bytes())

        rcon_command.response_packets.append(
            data.RconPacket(
                type=data.ReceivePacketType.SERVERDATA_RESPONSE_VALUE,
                data=self._socket.recv(4096)
            )
        )

        return rcon_command
    

    def keep_alive(self):
        next_beat = time.time() + KEEP_ALIVE_TIMEOUT_SECONDS
        keep_alive_packet = data.RconPacket(
            type=data.SendPacketType.SERVERDATA_EXECCOMMAND,
            data=b"stats"
        )


        while True:
            if time.time() < next_beat:
                continue
            
            print(self.send(keep_alive_packet).response_packets[0].data)
            next_beat = time.time() + KEEP_ALIVE_TIMEOUT_SECONDS

            
