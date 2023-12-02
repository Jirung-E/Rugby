from pico2d import load_image, clamp

import Game.play_scene as play_scene      # 플레이어 위치에 따라 배경 스크롤
import Game.game_framework as game_framework
from Math import Point


class Field:
    def __init__(self):
        self.image = load_image('res/field.jpg')
        self.width = 100 / 3.6
        self.height = 50 / 3.6
        self.draw_position = Point(0, 0)

    def draw(self):
        self.draw_position = -play_scene.player.position * game_framework.PIXEL_PER_METER + game_framework.window_center
        w = self.width * game_framework.PIXEL_PER_METER
        h = self.height * game_framework.PIXEL_PER_METER
        self.draw_position.x = clamp(game_framework.width-w/2, self.draw_position.x, w/2)
        self.draw_position.y = clamp(game_framework.height-h/2, self.draw_position.y, h/2)
        self.image.draw(self.draw_position.x, self.draw_position.y, w, h)

    def update(self):
        pass
