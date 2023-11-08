from pico2d import load_image, Image

from Math import Point


class Shadow:
    def __init__(self, caster, offset: Point = Point(0, 0)):
        self.image: Image = load_image('res/shadow_small.png')
        self.position = Point(0, 0)
        self.caster = caster
        self.offset = offset

    def draw(self):
        self.image.draw(self.position.x, self.position.y)

    def update(self):
        self.position = self.caster.position + self.offset
