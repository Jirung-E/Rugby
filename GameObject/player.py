from GameObject.controller import Controller

from Math import *

from pico2d import Image


class Player:
    def __init__(self):
        self.position = Point(0, 0)
        self.direction = Vector(0, 0)
        self.run_speed = Vector(5, 3)

        self.controller: Controller = None

        self.image: Image = None

        self.caught = False

    def update(self):
        self.position.x += self.direction.x * self.run_speed.x
        self.position.y += self.direction.y * self.run_speed.y
        self.controller.update()

    def handle_event(self, event):
        self.controller.handle_event(event)

    def draw(self):
        self.controller.draw()

'''
## AI & 플레이어
겹치는 부분: +, 다른 부분: -
+ 이동속도
+ 애니메이션
+ 상태변화
+ 이미지..?
- 플레이어는 키보드로 조작, AI는 자동으로 움직임
'''