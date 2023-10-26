from GameObject.controller import Controller
from Math import *

from abc import ABC, abstractmethod
from typing import List
import time


class State(ABC):
    def __init__(self, controller: Controller):
        self.controller = controller
        self.frame = 0
        self._clip_points: List[Point]
        self._clip_width: List[int]
        self._clip_height: int
        self.fps = 5

    def enter(self, event=None):
        self.frame = 0
        self.prev_draw_time = time.time()

    def exit(self, event=None):
        pass
        
    def draw(self):
        size = 1
        client = self.controller.client
        if self.controller.flip:
            client.image.clip_composite_draw(
                self._clip_points[self.frame].x, 
                self._clip_points[self.frame].y, 
                self._clip_width[self.frame], 
                self._clip_height, 
                0,
                'h',
                client.position.x - client.pivot.x, 
                client.position.y - client.pivot.y, 
                self._clip_width[self.frame] * size, 
                self._clip_height * size
            )
        else:
            client.image.clip_draw(
                self._clip_points[self.frame].x, 
                self._clip_points[self.frame].y, 
                self._clip_width[self.frame], 
                self._clip_height, 
                client.position.x - client.pivot.x, 
                client.position.y - client.pivot.y, 
                self._clip_width[self.frame] * size, 
                self._clip_height * size
            )
            
        if time.time() - self.prev_draw_time > 1 / self.fps:
            self.frame = (self.frame + 1) % len(self._clip_points)
            self.prev_draw_time = time.time()

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def idle(self):
        pass


class IdleState(State):
    def __init__(self, controller):
        super().__init__(controller)
        self.fps = 10
        y = 582-120
        self._clip_points: List[Point] = [Point(x, y) for x in range(0, 400, 81)]
        self._clip_width = [72, 72, 72, 72, 72]
        self._clip_height = 120

    def run(self):
        self.exit()
        self.controller.current_state = self.controller.getRunState()
        self.controller.start()

    def idle(self):
        pass

class RunState(State):
    def __init__(self, controller):
        super().__init__(controller)
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
        self.controller.current_state = self.controller.getIdleState()
        self.controller.start()
