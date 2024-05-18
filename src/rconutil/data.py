import enum
import random

from dataclasses import dataclass, fields, field


class SendPacketType(enum.IntEnum):
    SERVERDATA_AUTH = 3
    SERVERDATA_EXECCOMMAND = 2


class ReceivePacketType(enum.IntEnum):
    UNKNOWN_RESPONSE = -1
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_RESPONSE_VALUE = 0


@dataclass
class RconPacket:
    data: bytes | str
    type: SendPacketType | ReceivePacketType = field(
        default=ReceivePacketType.UNKNOWN_RESPONSE
    )

    id: int = field(default=0)

    def __post_init__(self):
        if type(self.type) is ReceivePacketType:
            self.id = int.from_bytes(self.data[1:5], "big")
            self.type = ReceivePacketType(
                int.from_bytes(self.data[5:9], "big")
            )
            self.data = self.data[11::]


    def to_bytes(self) -> bytes:
        return (10 + len(self.data)).to_bytes(1, "big") + (
            self.id.to_bytes(4, "big") 
                + self.type.value.to_bytes(4, "big")
                + b"\x00\x00\x00" 
                + self.data 
                + b"\x00\x00"
        )
