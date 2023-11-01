from GameObject.controller import Controller
from GameObject.state import *

from Math import *
from GameObject.ball import Ball

from pico2d import Image
import math
import random
import time
from typing import List


class Player:
    def __init__(self):
        self.position = Point(0, 0)
        self.direction = Vector(0, 0)
        self.run_speed = Vector(5, 3)
        self.stemina = 100
        self.dash = False

        self.state = None
        self.controller: Controller = None

        self.image: Image = None
        self.pivot = Point(0, -50)
        self.flip = False

        self.ball = None
        self.team = 0

        self.grabbed_opponent = None            # 지금 잡고있는 상대방
        self.grabbed_offset = Point(0, 0)       # 잡고있는 상대방의 상대좌표
        self.attackers: List[Player] = []       # 공격하는 상대방들

        self.idle_state = IdleState(self)
        self.run_state = RunState(self)
        self.grab_state = GrabState(self)
        self.grabbed_state = GrabbedState(self)
        self.tackle_state = TackleState(self)
        self.current_state: State = self.idle_state
        self.startAnimation()

        self.__prev_draw_time = time.time()

    def update(self):
        speed = self.run_speed
        for a in self.attackers:
            speed = speed - a.run_speed * random.uniform(0.8, 1.2)
            self.stemina -= 1
            if self.stemina <= 0:
                self.stemina = 0
        if self.grabbed_opponent is not None:
            self.position.x = self.grabbed_opponent.position.x - self.grabbed_offset.x
            self.position.y = self.grabbed_opponent.position.y - self.grabbed_offset.y
            self.stemina -= 1
            if self.stemina <= 0:
                self.stemina = 0
                self.release()
        else:
            if self.dash:
                if self.direction.x != 0 or self.direction.y != 0:
                    self.stemina -= 1
                    print(self.stemina)
                    if self.stemina <= 0:
                        self.stemina = 0
                        self.dash = False
                    speed = speed * 1.5
            self.position.x += self.direction.x * speed.x
            self.position.y += self.direction.y * speed.y
            self.stemina += 1
            if self.stemina >= 100:
                self.stemina = 100
        self.controller.update()

    def handle_event(self, event):
        self.controller.handle_event(event)

    def startAnimation(self):
        self.current_state.enter()
        self.current_state.frame = random.randrange(0, len(self.current_state._clip_points))

    def draw(self):
        size = 1
        if self.flip:
            self.image.clip_composite_draw(
                self.current_state._clip_points[self.current_state.frame].x, 
                self.current_state._clip_points[self.current_state.frame].y, 
                self.current_state._clip_width[self.current_state.frame], 
                self.current_state._clip_height, 
                0,
                'h',
                self.position.x - self.pivot.x, 
                self.position.y - self.pivot.y, 
                self.current_state._clip_width[self.current_state.frame] * size, 
                self.current_state._clip_height * size
            )
        else:
            self.image.clip_draw(
                self.current_state._clip_points[self.current_state.frame].x, 
                self.current_state._clip_points[self.current_state.frame].y, 
                self.current_state._clip_width[self.current_state.frame], 
                self.current_state._clip_height, 
                self.position.x - self.pivot.x, 
                self.position.y - self.pivot.y, 
                self.current_state._clip_width[self.current_state.frame] * size, 
                self.current_state._clip_height * size
            )
            
        if time.time() - self.__prev_draw_time > 1 / self.current_state.fps:
            self.current_state.frame = (self.current_state.frame + 1) % len(self.current_state._clip_points)
            self.__prev_draw_time = time.time()

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
        a = -r/d if d != 0 else 0
        b = h - a * d**2 / 4
        vz = math.sqrt(2 * self.ball.gravity * (b-h))
        self.ball.velocity_z = vz
        vf = vz / r
        self.ball.velocity = direction.unit() * vf
        
        self.ball.rotate_power = random.uniform(0.1, 0.15)
        self.ball.owner = None
        self.ball = None

    def grab(self, objects):
        if self.ball is not None:
            return
        if self.grabbed_opponent is not None:
            return
        
        for o in objects:
            if isinstance(o, Ball):
                self.catch(o)
                if self.ball is not None:
                    return
        
        for o in objects:
            if o is self:
                continue
            if isinstance(o, Player):
                if o.team == self.team:
                    continue
                if Point.distance2(self.position, o.position) < 30**2:
                    self.grabbed_opponent = o
                    o.attackers.append(self)
                    self.grabbed_offset = Point(o.position.x - self.position.x, o.position.y - self.position.y)
                    return
                
    def release(self):
        if self.grabbed_opponent is None:
            return
        
        self.grabbed_opponent.attackers.remove(self)
        self.grabbed_opponent = None
        self.grabbed_offset = Point(0, 0)


'''
## AI & 플레이어
겹치는 부분: +, 다른 부분: -
+ 이동속도
+ 애니메이션
+ 상태변화
+ 이미지..?
- 플레이어는 키보드로 조작, AI는 자동으로 움직임
'''