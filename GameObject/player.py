from GameObject.controller import Controller

from Math import *

from pico2d import Image
import math
import random


class Player:
    def __init__(self):
        self.position = Point(0, 0)
        self.direction = Vector(0, 0)
        self.run_speed = Vector(5, 3)

        self.controller: Controller = None

        self.image: Image = None
        self.pivot = Point(0, -50)

        self.ball = None
        self.team = 0

    def update(self):
        self.position.x += self.direction.x * self.run_speed.x
        self.position.y += self.direction.y * self.run_speed.y
        self.controller.update()

    def handle_event(self, event):
        self.controller.handle_event(event)

    def draw(self):
        self.controller.draw()

    def catch(self, ball):
        if self.ball is not None:
            return
        if ball.owner is not None:
            return
        if ball.height > 70:
            return
        if Point.distance2(self.position, ball.position) < 30**2:
            print(Point.distance(self.position, ball.position))
            print('catch')
            ball.owner = self
            self.ball = ball
            ball.rotate = 0

    def throw(self, x, y):
        if self.ball is None:
            return
        
        direction = Vector(x - self.position.x, y - self.position.y)
        if self.team == 1 and direction.x > 0:
            return
        if self.team == 2 and direction.x < 0:
            return
        
        # y = ax**2 + b
        h = self.ball.height
        D = direction.length()
        r = math.tan(math.radians(45))
        d = (D**2 * r) / (h + D*r)
        a = -r/d
        b = h - a * d**2 / 4
        vz = math.sqrt(2 * self.ball.gravity * (b-h))
        self.ball.velocity_z = vz
        vf = vz / r
        self.ball.velocity = direction.unit() * vf
        
        self.ball.rotate_power = random.uniform(0.1, 0.15)
        self.ball.owner = None
        self.ball = None

'''
## AI & 플레이어
겹치는 부분: +, 다른 부분: -
+ 이동속도
+ 애니메이션
+ 상태변화
+ 이미지..?
- 플레이어는 키보드로 조작, AI는 자동으로 움직임
'''