from pico2d import load_image, Image

from Math import Point
import Game.play_scene as play_scene


class Shadow:
    def __init__(self, caster, offset: Point = Point(0, 0)):
        self.image: Image = load_image('res/shadow_small.png')
        self.position = Point(0, 0)
        self.caster = caster
        self.offset = offset

    def draw(self):
        draw_position = self.position + self.offset + -play_scene.player.position + Point(400, 300)
        self.image.draw(draw_position.x, draw_position.y)

    def update(self):
        self.position = self.caster.position + self.offset
