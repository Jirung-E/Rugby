from Game.GameObject.controller import Controller
from Game.GameObject.state import *
from Game.GameObject.ball import Ball
import Game.game_framework as game_framework
import Game.world as world
import Game.play_scene as play_scene

from Math import *

from pico2d import Image, draw_rectangle, clamp
import math
import random
import time
from typing import List


class Player:
    def __init__(self):
        self.position = Point(0, 0)
        self.direction = Vector(0, 0)
        self.run_speed = Vector(5, 3)/2
        self.stemina_max = 400
        self.stemina = self.stemina_max
        self.stemina_regen = 1  # per second
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

        self.tackle_to = None
        self.fall_to = None

        self.idle_state = IdleState(self)
        self.run_state = RunState(self)
        self.dash_state = DashState(self)
        self.grab_state = GrabState(self)
        self.tackle_state = TackleState(self)
        self.fall_state = FallState(self)
        self.current_state: State = self.idle_state
        self.startAnimation()

        self.__prev_draw_time = time.time()

    def update(self):
        if self.grabbed_opponent is not None:
            # print(self.grabbed_opponent.stemina)
            self.position = self.grabbed_opponent.position + -self.grabbed_offset
            self.stemina -= 2
            if self.stemina <= 0:
                self.stemina = 0
                # self.release()
                
        self.stemina += 1
        if self.stemina >= self.stemina_max:
            self.stemina = self.stemina_max

        self.controller.update()
        self.current_state.update()

        w = play_scene.field.width // 2
        h = play_scene.field.height // 2
        self.position.x = clamp(-w+1, self.position.x, w-1)
        self.position.y = clamp(-h+1.5, self.position.y, h-1.5)

    def handle_event(self, event):
        self.controller.handle_event(event)

    def startAnimation(self):
        self.current_state.enter()
    
    def draw(self):
        size = 1
        flip = ''
        if self.flip:
            flip = 'h'

        draw_position = self.position + -play_scene.player.position
        draw_position *= game_framework.PIXEL_PER_METER
        draw_position += play_scene.window_center + -self.pivot
        clip_data = self.current_state.clip_data()

        self.image.clip_composite_draw(
            clip_data.x, clip_data.y, 
            clip_data.width, clip_data.height, 
            0, flip,
            draw_position.x, draw_position.y, 
            clip_data.width * size, clip_data.height * size
        )

        if time.time() - self.__prev_draw_time > 1 / self.current_state.fps:
            self.current_state.nextFrame()
            self.__prev_draw_time = time.time()

        x1, y1, x2, y2 = self.get_bb()
        x1 += -play_scene.player.position.x
        x1 *= game_framework.PIXEL_PER_METER
        x1 += play_scene.window_center.x
        y1 += -play_scene.player.position.y 
        y1 *= game_framework.PIXEL_PER_METER
        y1 += play_scene.window_center.y
        x2 += -play_scene.player.position.x 
        x2 *= game_framework.PIXEL_PER_METER
        x2 += play_scene.window_center.x
        y2 += -play_scene.player.position.y
        y2 *= game_framework.PIXEL_PER_METER
        y2 += play_scene.window_center.y
        draw_rectangle(x1, y1, 
                       x2, y2)

    def catch(self, ball):
        if self.ball is not None:
            return
        if ball.owner is not None:
            return
        if ball.height > 0.8:
            return
        # if Point.distance2(self.position, ball.position) < 30**2:
            # print(Point.distance(self.position, ball.position))
        print('catch')
        ball.owner = self
        self.ball = ball
        ball.rotate = 0

    def throw_double_power(self, x, y):
        if self.ball is None:
            return
        self.throw_direction(Vector(x - self.position.x, y - self.position.y) * 2)

    def throw_half_power(self, x, y):
        if self.ball is None:
            return
        self.throw_direction(Vector(x - self.position.x, y - self.position.y) * 0.5)

    def throw(self, x, y):
        if self.ball is None:
            return
        self.throw_direction(Vector(x - self.position.x, y - self.position.y))

    def throw_direction(self, direction):
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
        
        self.ball.rotate_power = random.uniform(3, 8)
        self.ball.owner = None
        self.ball = None

    def drop_ball(self):
        if self.ball is None:
            return
        
        self.ball.velocity.x = self.direction.x * self.run_speed.x
        self.ball.velocity.y = self.direction.y * self.run_speed.y
        self.ball.velocity_z = 4
        self.ball.owner = None
        self.ball = None

    def grab(self, other):
        if self.grabbed_opponent is not None:
            return
        
        if other.team != self.team:
            self.grabbed_opponent = other
            other.attackers.append(self)
            self.grabbed_offset = other.position + -self.position

    def release(self):
        if self.grabbed_opponent is None:
            return
        
        self.grabbed_opponent.attackers.remove(self)
        self.grabbed_opponent = None
        self.grabbed_offset = Point(0, 0)

    def tackle(self, x, y):
        to = Vector(x - self.position.x, y - self.position.y)
        if self.position.x < x:
            self.flip = False
        else:
            self.flip = True
        self.tackle_to = to.unit()
        self.current_state.tackle()

    def get_bb(self):
        return (self.position.x-0.25, self.position.y, self.position.x+0.25, self.position.y+0.5)
    
    def handle_collision(self, group, other):
        self.controller.handle_collision(group, other)
                