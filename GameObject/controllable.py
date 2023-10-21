from GameObject.controller import Controller
from GameObject.state import *

from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d


class Controllable(Controller):
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

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.client.direction.x -= 1
            elif event.key == SDLK_d:
                self.client.direction.x += 1
            elif event.key == SDLK_w:
                self.client.direction.y += 1
            elif event.key == SDLK_s:
                self.client.direction.y -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                self.client.direction.x += 1
            elif event.key == SDLK_d:
                self.client.direction.x -= 1
            elif event.key == SDLK_w:
                self.client.direction.y -= 1
            elif event.key == SDLK_s:
                self.client.direction.y += 1

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