from abc import ABC, abstractmethod


class Controller(ABC):
    def __init__(self, client):
        self.client = client

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def handle_event(self, event):
        pass

    @abstractmethod
    def handle_collision(self, group, other):
        pass
    