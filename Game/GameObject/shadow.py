from pico2d import load_image, Image

from Math import Point
import Game.play_scene as play_scene
import Game.game_framework as game_framework


class Shadow:
    def __init__(self, caster, offset: Point = Point(0, 0)):
        self.image: Image = load_image('res/shadow_small.png')
        self.position = Point(0, 0)
        self.caster = caster
        self.offset = offset

    def draw(self):
        draw_position = self.position + -play_scene.player.position
        draw_position *= game_framework.PIXEL_PER_METER
        draw_position += game_framework.window_center + self.offset
        self.image.draw(draw_position.x, draw_position.y)

    def update(self):
        self.position = self.caster.position
