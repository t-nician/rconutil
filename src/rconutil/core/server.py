from rconutil.core.packet import RconPacket, SendPacketType, ReceivePacketType


from socket import socket, AF_INET, SOCK_STREAM
from dataclasses import dataclass, field


@dataclass
class RconServer:
    host: str = field(default="")
    port: int = field(default=5000)
    password: str = field(default="password")
    
    _binded: bool = field(default=False)
    _socket: socket = field(
        default_factory=lambda: socket(
            family=AF_INET,
            type=SOCK_STREAM
        )
    )


    def run(self):
        self._socket.bind((self.host, self.port))
        self._socket.listen(5)

        while True:
            client_socket, _ = self._socket.accept()

            rcon_packet = RconPacket(
                data=client_socket.recv(4096)
            )

            print(rcon_packet)

            if rcon_packet.type is ReceivePacketType.UNKNOWN_RESPONSE:
                client_socket.send(b"BAD PACKET FORMAT")
            elif rcon_packet.type is ReceivePacketType.SERVERDATA_RESPONSE_VALUE:
                print("we empty!")
                client_socket.send(b"")
            else:
                print("good packet")
                response_packet = RconPacket(
                    id=rcon_packet.id,
                    type=ReceivePacketType.SERVERDATA_RESPONSE_VALUE,
                    data=b"hello there :o"
                )

                client_socket.send(response_packet.to_bytes())
                client_socket.recv(4096) 
                client_socket.send(b"")
