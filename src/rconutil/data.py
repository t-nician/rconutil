import enum
import random

from dataclasses import dataclass, field


class SendPacketType(enum.Enum):
    NONE = -1
    SERVERDATA_AUTH = b"\x00\x00\x00\x03"
    SERVERDATA_EXECCOMMAND = b"\x00\x00\x00\x02"


class ReceivePacketType(enum.Enum):
    NONE = -1
    SERVERDATA_AUTH_RESPONSE = b"\x00\x00\x00\x02"
    SERVERDATA_RESPONSE_VALUE = b"\x00\x00\x00\x00"


@dataclass
class RconPacket:
    id: bytes | int = field(default=0)
    data: bytes | str = field(default=b"")
    type: SendPacketType | ReceivePacketType = field(
        default=ReceivePacketType.NONE
    )

    def __post_init__(self):
        if type(self.type) is ReceivePacketType and self.id == b"":
            __id, __type, __data = self.__derive_bytes_packet_to_tuple(
                self.data
            )

            self.id = __id
            self.type = ReceivePacketType(__type)
            self.data = __data
        elif type(self.type) is SendPacketType:
            if type(self.id) is int:
                print("inty id!?")
                self.id = self.id.to_bytes(4, "big")


    def to_bytes(self) -> bytes:
        return self.__generate_bytes_packet(self.data)


    def __derive_bytes_packet_to_tuple(
            self, data: bytes
    ) -> tuple[bytes, bytes, bytes]:
        #print("HEY YOU GOTTA MAKE ME WORK. PROB DIDNT MEAN TO RUN ME!")

        id = data[1:5]
        _type = data[6:10]
        raw = data[11::]

        print("raw", data)

        return id, _type, data


    def __generate_bytes_packet(self, data: bytes | str) -> bytes:
        __data = data
        if type(__data) is str:
            __data = __data.encode()
        print(self.id)
        print(self.type.value)
        result = str(10 + len(__data)).encode() + self.id + self.type.value + b"\x00" + __data + b"\x00\x00"

        return result


@dataclass
class RconCommand:
    command_packet: RconPacket = field(default_factory=RconPacket)
    response_packets: list[RconPacket] = field(default_factory=list)

