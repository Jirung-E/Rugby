from Game.GameObject.controller import Controller
import Game.world as world
from Game.GameObject.ball import Ball
from Game.GameObject.player import Player
from Math import Point

from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDLK_LSHIFT, SDLK_SPACE, \
    SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT
from pico2d import get_canvas_height


class Controllable(Controller):
    def __init__(self, client):
        super().__init__(client)
        self.dash = False
        self.handling = False

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
            elif event.key == SDLK_LSHIFT:
                if self.client.stemina > 0:
                    self.dash = True
            elif event.key == SDLK_SPACE:
                self.handling = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                self.client.direction.x += 1
            elif event.key == SDLK_d:
                self.client.direction.x -= 1
            elif event.key == SDLK_w:
                self.client.direction.y -= 1
            elif event.key == SDLK_s:
                self.client.direction.y += 1
            elif event.key == SDLK_LSHIFT:
                self.dash = False
            elif event.key == SDLK_SPACE:
                self.handling = False
                self.client.release()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            HEIGHT = get_canvas_height()
            if event.button == SDL_BUTTON_LEFT:
                self.client.throw(event.x, HEIGHT - event.y)
            elif event.button == SDL_BUTTON_RIGHT:
                self.client.tackle(event.x, HEIGHT - event.y)

        if self.client.direction.x == 0 and self.client.direction.y == 0:
            self.client.current_state.idle()
        else:
            if self.dash:
                self.client.current_state.dash()
            else:
                self.client.current_state.run()

            if self.client.direction.x > 0:
                self.client.flip = False
            elif self.client.direction.x < 0:
                self.client.flip = True

    def handle_collision(self, group, other):
        if not self.handling:
            return
        
        if group == "ball:player":
            self.client.catch(other)
        elif group == "player:player":
            self.client.grab(other)
