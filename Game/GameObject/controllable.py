from Game.GameObject.controller import Controller
import Game.play_scene as play_scene
import Game.game_framework as game_framework
import Game.world as world
from Math import Point

from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDLK_LSHIFT, SDLK_SPACE, \
    SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT, SDL_BUTTON_RIGHT
from pico2d import get_canvas_height


class Controllable(Controller):
    def __init__(self, client):
        super().__init__(client)
        self.dash = False
        self.a_pressed = False
        self.d_pressed = False
        self.w_pressed = False
        self.s_pressed = False

    def update(self):
        pass

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            self.handle_keydown(event.key)
        elif event.type == SDL_KEYUP:
            self.handle_keyup(event.key)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            self.handle_mousedown(event.button, event.x, event.y)

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

    def handle_keydown(self, key):
        if key == SDLK_a:
            self.client.direction.x -= 1
            self.a_pressed = True
        elif key == SDLK_d:
            self.client.direction.x += 1
            self.d_pressed = True
        elif key == SDLK_w:
            self.client.direction.y += 1
            self.w_pressed = True
        elif key == SDLK_s:
            self.client.direction.y -= 1
            self.s_pressed = True
        elif key == SDLK_LSHIFT:
            if self.client.stemina > 0:
                self.dash = True
        elif key == SDLK_SPACE:
            if self.client.ball is not None:
                return
            if self.client.grabbed_opponent is not None:
                return
            
            if play_scene.ball.owner is None:
                if world.collide(self.client, play_scene.ball):
                    self.client.catch(play_scene.ball)
                    return

            for other in play_scene.team[self.client.team & 1]:     # 0001 & 0001 = 0001, 0010 & 0001 = 0000
                if world.collide(self.client, other):
                    self.client.grab(other)
                    break

    def handle_keyup(self, key):
        if key == SDLK_a:
            if self.d_pressed:
                self.client.direction.x += 1
            else:
                self.client.direction.x = 0
            self.a_pressed = False
        elif key == SDLK_d:
            if self.a_pressed:
                self.client.direction.x -= 1
            else:
                self.client.direction.x = 0
            self.d_pressed = False
        elif key == SDLK_w:
            if self.s_pressed:
                self.client.direction.y -= 1
            else:
                self.client.direction.y = 0
            self.w_pressed = False
        elif key == SDLK_s:
            if self.w_pressed:
                self.client.direction.y += 1
            else:
                self.client.direction.y = 0
            self.s_pressed = False
        elif key == SDLK_LSHIFT:
            self.dash = False
        elif key == SDLK_SPACE:
            self.client.release()

    def handle_mousedown(self, button, x, y):
        # 클릭 좌표에서 플레이어 기준 좌표계로 변환
        HEIGHT = get_canvas_height()
        y = HEIGHT - y

        player_position = play_scene.field.draw_position + play_scene.player.position * game_framework.PIXEL_PER_METER
        click_point = Point(x, y) + -play_scene.field.draw_position
        click_point /= game_framework.PIXEL_PER_METER
        if button == SDL_BUTTON_LEFT:
            self.client.throw_double_power(click_point.x, click_point.y)
        elif button == SDL_BUTTON_RIGHT:
            self.client.tackle(click_point.x, click_point.y)

    def handle_collision(self, group, other):
        pass
