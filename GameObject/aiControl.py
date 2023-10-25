from GameObject.controller import Controller
from GameObject.state import *

import random


class AIControl(Controller):
    def __init__(self, client):
        super().__init__(client)
        self._idle_state = IdleState(self)
        self._run_state = RunState(self)
        self.current_state: State = self._idle_state
        self.flip = False
        self.start()

    def getIdleState(self):
        return self._idle_state
    
    def getRunState(self):
        return self._run_state

    def start(self):
        self.current_state.enter()
        self.current_state.frame = random.randrange(0, len(self.current_state._clip_points))

    def update(self):
        if self.client.ball is not None:
            self.current_state.run()
            if self.flip:
                self.client.direction.x = -1
            else:
                self.client.direction.x = 1

    def handle_event(self, event):
        if self.client.direction.x == 0 and self.client.direction.y == 0:
            self.current_state.idle()
        else:
            self.current_state.run()
            if self.client.direction.x > 0:
                self.flip = False
            elif self.client.direction.x < 0:
                self.flip = True

    def draw(self):
        self.current_state.draw()
    