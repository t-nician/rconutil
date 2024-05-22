from enum import Enum
from dataclasses import dataclass, field

class ResponseValue(Enum):
    SERVERDATA_EMPTY = b"\x00\x00\x00\x00"


class SendPacketType(Enum):
    SERVERDATA_AUTH = b"\x00\x00\x00\x03"
    SERVERDATA_EXECCOMMAND = b"\x00\x00\x00\x02"


class ReceivePacketType(Enum):
    UNKNOWN_RESPONSE = -1
    SERVERDATA_AUTH_SUCCESS = b"\x00\x00\x00\x02"
    SERVERDATA_AUTH_FAILURE = b"\xff\xff\xff\x02"
    SERVERDATA_RESPONSE_VALUE = b"\x00\x00\x00\x00"


@dataclass
class RconPacket:
    id: int = field(default=0)
    data: bytes | str = field(default=b"")
    type: SendPacketType | ReceivePacketType = field(
        default=ReceivePacketType.UNKNOWN_RESPONSE
    )

    def __post_init__(self):
        if type(self.data) is str:
            self.data = self.data.encode()

        if self.type is ReceivePacketType.UNKNOWN_RESPONSE:
            if self.data != b"":
                self.id = int.from_bytes(self.data[1:5], "big")
                self.type = ReceivePacketType(self.data[5:9])
                self.data = self.data[10::]
    

    def to_bytes(self) -> bytes:
        return (10 + len(self.data)).to_bytes(1, "big") + (
            self.id.to_bytes(4, "big") 
                + self.type.value
                + b"\x00\x00\x00" 
                + self.data 
                + b"\x00\x00"
        )
        
