from logger import Logger

logger = Logger(2).get_logger()

class EventHandler:
    events_list = dict()

    def add_event(self, event_type: str, func):
        if not event_type in self.events_list:
            self.events_list[event_type] = []
        self.events_list[event_type].append(func)

    def on(self, event_type: str, data, index = None):
        if not event_type in self.events_list:
            raise Exception(f'{event_type} as not been defined as an Event')
        for func in self.events_list[event_type]:
            func(data, index) if index != None else func(data)

