import enum
import struct

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
class Packet:
    type: SendPacketType | ReceivePacketType = field(
        default=ReceivePacketType.NONE
    )

    data: bytes = field(default=b"")
    id: int = field(default=0)


    def __post_init__(self):
        if type(self.type) is SendPacketType:
            self.data = self.__raw_data_to_packet_format(self.data)
    

    def set_data(self, data: bytes):
        self.data = self.__raw_data_to_packet_format(data)


    def __raw_data_to_packet_format(self, data: bytes):
        """
        Glad I found this!
        
        https://github.com/Ch4r0ne/python-rcon-client/blob/main/python-rcon-client.py#L31
        """
        return struct.pack(
            "<3i",
            10 + len(data),
            self.id,
            self.type.value,
        ) + data + b"\x00\x00"

    