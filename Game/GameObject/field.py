from pico2d import load_image

import Game.play_scene as play_scene      # 플레이어 위치에 따라 배경 스크롤
import Game.game_framework as game_framework
from Math import Point


class Field:
    def __init__(self):
        self.image = load_image('res/field.jpg')
        self.width = 100 / 3.6
        self.height = 50 / 3.6

    def draw(self):
        draw_position = -play_scene.player.position * game_framework.PIXEL_PER_METER + game_framework.window_center
        w = self.width * game_framework.PIXEL_PER_METER
        h = self.height * game_framework.PIXEL_PER_METER
        self.image.draw(draw_position.x, draw_position.y, w, h)

    def update(self):
        pass
