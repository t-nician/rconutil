import socket
import time

from rconutil import data
from dataclasses import dataclass, field


SOCKET_TIMEOUT = 1


@dataclass
class RconClient:
    host: str
    port: int
    password: str = field(default="")

    _connected: bool = field(default=False)
    _socket: socket.socket = field(
        default_factory=lambda: socket.socket(
            family=socket.AF_INET, 
            type=socket.SOCK_STREAM,
        )
    )

    def __post_init__(self):
        self._socket.settimeout(SOCKET_TIMEOUT)


    def send(self, command_packet: data.RconPacket) -> data.RconCommand:
        rcon_command = data.RconCommand(
            command_packet=command_packet
        )
        
        self._socket.send(command_packet.to_bytes())

        # TODO this is problematic.
        # Using this in tandem with async functionality will cause dropped packets.
        # Need to create a pool of packet response listeners in the future.
        # We'll call this the sync version.
        while True:
            try:
                received_packet = data.RconPacket(
                    data=self._socket.recv(4096)
                )

                if received_packet.id == command_packet.id:
                    match command_packet.type:
                        case data.SendPacketType.SERVERDATA_AUTH:
                            if received_packet.type is data.ReceivePacketType.SERVERDATA_AUTH_RESPONSE:
                                rcon_command.response_packets.append(received_packet)

                        case data.SendPacketType.SERVERDATA_EXECCOMMAND:
                            if received_packet.type is data.ReceivePacketType.SERVERDATA_RESPONSE_VALUE:
                                rcon_command.response_packets.append(received_packet)

            except socket.error as _:
                break

        return rcon_command

    
    def connect(self):
        if self._connected:
            return None
        self._socket.connect((self.host, self.port))
        self._connected = True
    

    def login(self, password: str | None = None) -> bool:
        self.connect()

        rcon_response = self.send(
            command_packet=data.RconPacket(
                type=data.SendPacketType.SERVERDATA_AUTH,
                data=password or self.password,
                id=99
            )
        )

        login_response = rcon_response.response_packets[0]

        print(login_response)



       

