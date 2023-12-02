from Math import *
import Game.game_framework as game_framework
import Game.play_scene as play_scene

import random

from pico2d import Image, load_image, draw_rectangle, clamp


class Ball:
    def __init__(self):
        self.position = Point(0, 0)
        self.height = 2     # position z
        self.velocity = Vector(0, 0)
        self.velocity_z = random.uniform(1.0, 2.0)
        self.gravity = 10.0     # m/s^2
        self.rotate = 0
        self.rotate_power = random.uniform(5, 10)
        self.rotate_dir = random.choice([-1, 1])

        self.image: Image = load_image('res/ball_small.png')

        self.owner = None

    def update(self):
        if self.owner is not None:
            self.position.x = self.owner.position.x
            self.position.y = self.owner.position.y
            self.height = 1
            return

        dt = game_framework.dt

        self.position += self.velocity * dt
        w = play_scene.field.width // 2
        h = play_scene.field.height // 2
        if self.position.x < -w+1 or self.position.x > w-1:
            self.velocity.x = -self.velocity.x
        if self.position.y < -h+1.5 or self.position.y > h-1.5:
            self.velocity.y = -self.velocity.y
        self.position.x = clamp(-w+1, self.position.x, w-1)
        self.position.y = clamp(-h+1.5, self.position.y, h-1.5)

        self.height += self.velocity_z * dt
        self.velocity_z -= self.gravity * dt
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

            self.rotate_power -= 0.2
            if self.rotate_power < 0:
                self.rotate_power = 0

        # if self.position.x < 0:
        #     self.velocity.x = abs(self.velocity.x)
        # elif self.position.x > 800:
        #     self.velocity.x = -abs(self.velocity.x)
        # if self.position.y < 0:
        #     self.velocity.y = abs(self.velocity.y)
        # elif self.position.y > 600:
        #     self.velocity.y = -abs(self.velocity.y)

        self.rotate += self.rotate_power * self.rotate_dir * dt

    def draw(self):
        draw_position = play_scene.field.draw_position + (Point(0, self.height) + self.position) * game_framework.PIXEL_PER_METER + Point(0, 30)
        self.image.composite_draw(self.rotate, '', draw_position.x, draw_position.y)

        # x1, y1, x2, y2 = self.get_bb()
        # x1 += -play_scene.player.position.x
        # x1 *= game_framework.PIXEL_PER_METER
        # x1 += game_framework.window_center.x
        # y1 += -play_scene.player.position.y
        # y1 *= game_framework.PIXEL_PER_METER
        # y1 += game_framework.window_center.y
        # x2 += -play_scene.player.position.x
        # x2 *= game_framework.PIXEL_PER_METER
        # x2 += game_framework.window_center.x
        # y2 += -play_scene.player.position.y
        # y2 *= game_framework.PIXEL_PER_METER
        # y2 += game_framework.window_center.y
        # draw_rectangle(x1, y1, x2, y2)

    def get_bb(self):
        return (self.position.x - 0.5, self.position.y - 0.5, self.position.x + 0.5, self.position.y + 0.5)
    
    def handle_collision(self, group, other):
        if group == "ball:player":
            pass
