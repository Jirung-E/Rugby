from abc import ABC, abstractmethod


class Controller(ABC):
    def __init__(self, client):
        self.client = client

    # @abstractmethod
    def update(self):
        pass

    # @abstractmethod
    def handle_event(self, event):
        pass

    # @abstractmethod
    def draw(self):
        self.client.image.clip_draw(self.client.frame * 100, self.client.action * 100,
                                    100, 100,
                                    self.client.x, self.client.y)