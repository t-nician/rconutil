import enum

from dataclasses import dataclass, field


class LoginMessage(enum.Enum):
    SUCCESS = b"\x00\x00\x00"
    FAILURE = b"\xff\xff\xff\xff"


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
        if type(self.data) is str:
            self.data = self.data.encode()
            
        if self.type is ReceivePacketType.UNKNOWN_RESPONSE:
            self.id = int.from_bytes(self.data[1:5], "big")

            if self.data[4:8] == LoginMessage.FAILURE.value:
                self.data = LoginMessage.FAILURE.value
                self.type = ReceivePacketType.SERVERDATA_AUTH_RESPONSE
            else:
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


@dataclass
class RconCommand:
    command_packet: RconPacket
    response_packets: list[RconPacket] = field(
        default_factory=list
    )