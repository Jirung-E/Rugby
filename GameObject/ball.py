from Math import *

import random

from pico2d import Image, load_image


class Ball:
    def __init__(self):
        self.position = Point(0, 0)
        self.height = 5     # position z
        self.velocity = Vector(0, 0)
        self.velocity_z = random.uniform(5, 10)
        self.gravity = 0.1
        self.rotate = 0
        self.rotate_power = random.uniform(0.05, 0.3)
        self.rotate_dir = random.choice([-1, 1])

        self.image: Image = load_image('res/ball_small.png')

    def update(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        
        self.height += self.velocity_z
        self.velocity_z -= self.gravity
        if self.height <= 0:
            self.height = 0

            if abs(self.velocity_z) < 1:
                self.velocity_z = 0
            else:
                self.velocity_z = -self.velocity_z * 0.7

            self.rotate_power -= 0.002
            if self.rotate_power < 0:
                self.rotate_power = 0

        self.rotate += self.rotate_power * self.rotate_dir


    def draw(self):
        self.image.composite_draw(self.rotate, '', self.position.x, self.position.y + self.height)