from Math import *

from abc import ABC, abstractmethod
from typing import List


class State(ABC):
    def __init__(self, client):
        self.client = client
        self.frame = 0
        self._clip_points: List[Point]
        self._clip_width: List[int]
        self._clip_height: int
        self.fps = 5

    def enter(self, event=None):
        self.frame = 0

    def exit(self, event=None):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def idle(self):
        pass


class IdleState(State):
    def __init__(self, client):
        super().__init__(client)
        self.fps = 10
        y = 582-120
        self._clip_points: List[Point] = [Point(x, y) for x in range(0, 400, 81)]
        self._clip_width = [72, 72, 72, 72, 72]
        self._clip_height = 120

    def run(self):
        self.exit()
        self.client.current_state = self.client.run_state
        self.client.startAnimation()

    def idle(self):
        pass


class RunState(State):
    def __init__(self, client):
        super().__init__(client)
        self.fps = 15
        y = 318
        self._clip_points: List[Point] = [Point(481, y), Point(550, y), Point(625, y), 
                                          Point(713, y), Point(794, y), Point(794+72+1, y)]
        self._clip_width = [68, 74, 87, 80, 72, 80]
        self._clip_height = 120

    def run(self):
        pass

    def idle(self):
        self.exit()
        self.client.current_state = self.client.idle_state
        self.client.startAnimation()


class GrabState(State):
    def __init__(self, client):
        super().__init__(client)
        pass

    def run(self):
        pass

    def idle(self):
        pass


class TackleState(State):
    def __init__(self, client):
        super().__init__(client)
        pass

    def run(self):
        pass

    def idle(self):
        pass
