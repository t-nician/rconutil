import enum
import random

from dataclasses import dataclass, fields, field


class SendPacketType(enum.Enum):
    SERVERDATA_AUTH = b"\x00\x00\x00\x03"
    SERVERDATA_EXECCOMMAND = b"\x00\x00\x00\x02"


class ReceivePacketType(enum.Enum):
    UNKNOWN_RESPONSE = -1
    SERVERDATA_AUTH_RESPONSE = b"\x00\x00\x00\x02"
    SERVERDATA_RESPONSE_VALUE = b"\x00\x00\x00\x00"


@dataclass
class RconPacket:
    """
        Main container for rcon data.
        
        Passing a int to id will convert it to a bytes value after init.

        Example:
            id: 5 -> id: b"\x00\x00\x00\x05"
            id: 3 -> id: b"\x00\x00\x00\x03"
    """
    data: bytes | str
    type: SendPacketType | ReceivePacketType = field(
        default=ReceivePacketType.UNKNOWN_RESPONSE
    )

    id: bytes | int = field(default=0)

    def __post_init__(self):
        if type(self.id) is int:
            self.id = self.id.to_bytes(4, "big")

        if type(self.type) is ReceivePacketType:
            self.id = self.data[1:5]
            self.type = ReceivePacketType(self.data[5:9])
            self.data = self.data[11::]


    def to_bytes(self) -> bytes:
        return str(
            10 + len(self.data)
        ).encode() + (
            self.id + self.type.value + b"\x00" + self.data + b"\x00\x00"
        )
