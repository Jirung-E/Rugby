from Math import *

from pico2d import Image, load_image


class Ball:
    def __init__(self):
        self.position = Point(0, 0)
        self.direction = Vector(0, 0)
        self.run_speed = Vector(5, 3)

        self.image: Image = load_image('res/ball_small.png')

    def update(self):
        self.position.x += self.direction.x * self.run_speed.x
        self.position.y += self.direction.y * self.run_speed.y

    def draw(self):
        self.image.draw(self.position.x, self.position.y)