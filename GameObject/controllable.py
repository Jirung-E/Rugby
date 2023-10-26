from GameObject.controller import Controller

from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d


class Controllable(Controller):
    def __init__(self, client):
        super().__init__(client)

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
            self.client.current_state.idle()
        else:
            self.client.current_state.run()
            if self.client.direction.x > 0:
                self.client.flip = False
            elif self.client.direction.x < 0:
                self.client.flip = True
