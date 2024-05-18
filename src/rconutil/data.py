import enum
import struct
import random

from dataclasses import dataclass, field


class SendPacketType(enum.IntEnum):
    NONE = -1
    SERVERDATA_AUTH = 3
    SERVERDATA_EXECCOMMAND = 2


class ReceivePacketType(enum.IntEnum):
    NONE = -1
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_RESPONSE_VALUE = 0


@dataclass
class RconPacket:
    id: int = field(default_factory=lambda: random.randint(0, 9))
    data: bytes | str = field(default=b"")
    type: SendPacketType | ReceivePacketType = field(
        default=ReceivePacketType.NONE
    )

    def __post_init__(self):
        if type(self.type) is SendPacketType and self.data != b"":
            self.data = self.__generate_bytes_packet(self.data)
        elif type(self.type) is ReceivePacketType and self.data != b"":
            __id, __type, __data  = self.__derive_bytes_packet_to_tuple(
                self.data
            )

            self.id = __id
            self.type = ReceivePacketType(__type)
            self.data = __data


    def to_bytes(self) -> bytes:
        return self.__generate_bytes_packet(self.data)


    def __derive_bytes_packet_to_tuple(
            self, data: bytes
    ) -> tuple[int, int, bytes]:
        print("HEY YOU GOTTA MAKE ME WORK. PROB DIDNT MEAN TO RUN ME!")
        return 0, 0, b""


    def __generate_bytes_packet(self, data: bytes | str) -> bytes:
        """
        Glad I found this!
        
        https://github.com/Ch4r0ne/python-rcon-client/blob/main/python-rcon-client.py#L31
        """
        __data = data
        if type(__data) is str:
            __data = __data.encode()

        return struct.pack(
            "<3i",
            10 + len(__data),
            self.id,
            self.type.value,
        ) + __data + b"\x00\x00"


@dataclass
class RconCommand:
    command_packet: RconPacket = field(default_factory=RconPacket)
    response_packets: list[RconPacket] = field(default_factory=list)

