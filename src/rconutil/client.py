import socket

from rconutil import data
from dataclasses import dataclass, field


@dataclass
class RconClient:
    host: str = field(default="")
    port: int = field(default=-1)
    password: str = field(default="")

    _socket: socket.socket = field(
        default_factory=lambda: socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
    )

    def connect(self, password: str | None = None) -> bool:
        assert self.host != "", "No host provided to rcon!"
        assert self.port != -1, "No port provided to rcon!"

        self._socket.connect((self.host, self.port))

        assert password or self.password != "", "No password provided to rcon!"

        __password = password or self.password

        

        



