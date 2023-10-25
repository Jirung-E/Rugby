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
        self.shadow: Image = load_image('res/shadow_small.png')

        self.owner = None

    def update(self):
        if self.owner is not None:
            self.position.x = self.owner.position.x
            self.position.y = self.owner.position.y
            self.height = 80
            return
        
        print(self.velocity.x, self.velocity.y)

        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        
        self.height += self.velocity_z
        self.velocity_z -= self.gravity
        if self.height <= 0:
            self.height = 0

            if abs(self.velocity.x) < 0.1:
                self.velocity.x = 0
            else:
                self.velocity.x *= 0.9

            if abs(self.velocity.y) < 0.1:
                self.velocity.y = 0
            else:
                self.velocity.y *= 0.9

            if abs(self.velocity_z) < 1:
                self.velocity_z = 0
            else:
                self.velocity_z = -self.velocity_z * 0.7

            self.rotate_power -= 0.002
            if self.rotate_power < 0:
                self.rotate_power = 0

        if self.position.x < 0:
            self.velocity.x = abs(self.velocity.x)
        elif self.position.x > 800:
            self.velocity.x = -abs(self.velocity.x)
        if self.position.y < 0:
            self.velocity.y = abs(self.velocity.y)
        elif self.position.y > 600:
            self.velocity.y = -abs(self.velocity.y)

        self.rotate += self.rotate_power * self.rotate_dir


    def draw(self):
        self.image.composite_draw(self.rotate, '', self.position.x, self.position.y-20 + self.height)

    def drawShadow(self):
        self.shadow.draw(self.position.x, self.position.y-50)