from rconutil.core import data

from dataclasses import dataclass, field
from socket import socket, AF_INET, SOCK_STREAM


@dataclass
class RconClient:
    host: str = field(default="")
    port: int = field(default=-1)
    password: str = field(default="")
    _socket: socket = field(
        default_factory=lambda: socket(
            family=AF_INET, 
            type=SOCK_STREAM
        )
    )

    def send(
        self, packet: data.RconPacket
    ) -> data.RconPacket | list[data.RconPacket]:
        stream_packet = data.RconPacket(
            type=data.ReceivePacketType.SERVERDATA_RESPONSE_VALUE,
            data=b"\x00\x00\x00\x01"
        )
        return_packets = []
        
        self._socket.send(packet.to_bytes())
        
        while True:
            response_packet = data.RconPacket(
                data=self._socket.recv(4096)
            )

            print("response", response_packet)

            match response_packet.type:
                case data.ReceivePacketType.SERVERDATA_AUTH_FAILURE:
                    return_packets.append(response_packet)
                    break
                case data.ReceivePacketType.SERVERDATA_AUTH_SUCCESS:
                    if response_packet.id == packet.id:
                        return_packets.append(response_packet)
                        break
                case data.ReceivePacketType.SERVERDATA_RESPONSE_VALUE:
                    if response_packet.id == packet.id:
                        return_packets.append(response_packet)
                        self._socket.send(stream_packet.to_bytes())


        return len(return_packets) == 1 and return_packets[0] or return_packets


    def connect(self):
        self._socket.connect((self.host, self.port))
    

    def login(self, password_override: str | None = None):
        self.connect()
        self.send(
            data.RconPacket(
                type=data.SendPacketType.SERVERDATA_AUTH,
                data=password_override or self.password
            )
        )
        