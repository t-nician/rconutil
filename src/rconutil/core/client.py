from rconutil.core import packet

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
        self, packet: packet.RconPacket,
        ignore_multipacket: bool | None = False
    ) -> packet.RconPacket | list[packet.RconPacket]:
        stream_packet = packet.RconPacket(
            type=packet.ReceivePacketType.SERVERDATA_RESPONSE_VALUE,
            data=b"",
            id=1,
        )

        return_packets = []
        
        self._socket.send(packet.to_bytes())

        if not ignore_multipacket:
            self._socket.send(stream_packet.to_bytes())

        while True:
            if not ignore_multipacket:
                self._socket.send(stream_packet.to_bytes())

            response_packet = packet.RconPacket(
                data=self._socket.recv(4096)
            )

            match response_packet.type:
                case packet.ReceivePacketType.SERVERDATA_AUTH_FAILURE:
                    return_packets.append(response_packet)
                    break
                case packet.ReceivePacketType.SERVERDATA_AUTH_SUCCESS:
                    if response_packet.id == packet.id:
                        return_packets.append(response_packet)
                        break
                case packet.ReceivePacketType.SERVERDATA_RESPONSE_VALUE:
                    if response_packet.id == packet.id:
                        return_packets.append(response_packet)
                        if ignore_multipacket:
                            break
                        if response_packet.data == b"":
                            break
                case packet.ReceivePacketType.UNKNOWN_RESPONSE:
                    break


        return len(return_packets) == 1 and return_packets[0] or return_packets


    def connect(self):
        self._socket.connect((self.host, self.port))
    

    def login(self, password_override: str | None = None):
        self.connect()
        self.send(
            packet.RconPacket(
                type=packet.SendPacketType.SERVERDATA_AUTH,
                data=password_override or self.password,
            ),
            ignore_multipacket=True
        )
        