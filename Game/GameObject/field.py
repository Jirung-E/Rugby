from pico2d import load_image

import Game.play_scene as play_scene      # 플레이어 위치에 따라 배경 스크롤
from Math import Point


class Field:
    def __init__(self):
        self.image = load_image('res/field.jpg')

    def draw(self):
        draw_position = -play_scene.player.position + Point(400, 300)
        size = 2
        self.image.draw(draw_position.x+400, draw_position.y+300, self.image.w*size, self.image.h*size)

    def update(self):
        pass
