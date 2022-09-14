from typing import ClassVar, List
from src.logger import Logger
logger = Logger.get_logger()

class RegisteredFeed:
    uid: ClassVar[int]
    type: ClassVar[int]
    name: ClassVar[str]
    link: ClassVar[str]
    registered_channels: ClassVar[List[int]]

    def __init__(self, uid: int, type: int, name: str, link: str, registered_channel: int) -> None:
        self.uid = uid
        self.type = type
        self.name = name
        self.link = link
        self.registered_channels = [registered_channel]

class RegisteredServer:
    id: ClassVar[int]
    name: ClassVar[str]
    feeds: ClassVar[List[RegisteredFeed]]

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name
        self.feeds = []
