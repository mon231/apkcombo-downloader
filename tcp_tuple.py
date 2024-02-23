from dataclasses import dataclass


@dataclass
class TcpTuple:
    ip: str
    port: int

    def __str__(self) -> str:
        return f'{self.ip}:{self.port}'
