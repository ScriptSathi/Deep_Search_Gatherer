from logger import Logger
from message import Message

logger = Logger(2).get_logger()

class EventHandler:
    events_list = dict()

    def __init__(self) -> None:
        self.setup_events()

    def add_event(self, event_type: str, func):
        if not event_type in self.events_list:
            self.events_list[event_type] = []
        self.events_list[event_type].append(func)

    def do(self, event_type: str, data, index_of_current_feed = None):
        if not event_type in self.events_list:
            raise Exception(f'{event_type} as not been defined as an Event')
        for func in self.events_list[event_type]:
            func(data, index_of_current_feed) if index_of_current_feed != None else func(data)

    def setup_events(self):
        Message.add_events(self)