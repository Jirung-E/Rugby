from Math import *

import Game.game_framework as game_framework

import random
from abc import ABC, abstractmethod
from typing import List


class ClipData:
    def __init__(self, point, width, height):
        self.x = point.x
        self.y = point.y
        self.width = width
        self.height = height


class State(ABC):
    def __init__(self, client):
        self.client = client
        self.frame = 0
        self._clip_points: List[Point]
        self._clip_width: List[int]
        self._clip_height: int
        self.fps = 5

    def clip_data(self):
        return ClipData(self._clip_points[self.frame], self._clip_width[self.frame], self._clip_height)

    def enter(self, event=None):
        self.frame = random.randrange(0, len(self._clip_points))

    def exit(self, event=None):
        pass

    def update(self, event=None):
        pass

    def nextFrame(self):
        self.frame = (self.frame + 1) % len(self._clip_points)

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def dash(self):
        pass

    @abstractmethod
    def idle(self):
        pass

    @abstractmethod
    def grab(self):
        pass

    @abstractmethod
    def grabbed(self):
        pass

    @abstractmethod
    def tackle(self):
        pass

    @abstractmethod
    def release(self):
        pass

    @abstractmethod
    def fall(self):
        pass


class IdleState(State):
    def __init__(self, client):
        super().__init__(client)
        self.fps = 10
        y = 582-120
        self._clip_points: List[Point] = [Point(x, y) for x in range(0, 400, 81)]
        self._clip_width = [72, 72, 72, 72, 72]
        self._clip_height = 120

    def run(self):
        self.exit()
        self.client.current_state = self.client.run_state
        self.client.startAnimation()

    def dash(self):
        self.exit()
        self.client.current_state = self.client.dash_state
        self.client.startAnimation()

    def idle(self):
        pass

    def grab(self):
        self.exit()
        self.client.current_state = self.client.grab_state
        self.client.startAnimation()

    def grabbed(self):
        pass

    def tackle(self):
        self.exit()
        self.client.current_state = self.client.tackle_state
        self.client.startAnimation()

    def release(self):
        pass

    def fall(self):
        self.exit()
        self.client.current_state = self.client.fall_state
        self.client.startAnimation()


class RunState(State):
    def __init__(self, client):
        super().__init__(client)
        self.fps = 15
        y = 318
        self._clip_points: List[Point] = [Point(481, y), Point(550, y), Point(625, y), 
                                          Point(713, y), Point(794, y), Point(794+72+1, y)]
        self._clip_width = [68, 74, 87, 80, 72, 80]
        self._clip_height = 120

    def update(self, event=None):
        dir = self.client.direction
        if self.client.direction.x != 0 and self.client.direction.y != 0:
            dir = self.client.direction.unit()
        speed = Vector(self.client.run_speed.x * dir.x, 
                       self.client.run_speed.y * dir.y)
        self._update(speed)

    def _update(self, speed):
        d = self.client.team * 2 - 3    # 끌고갈 방향
        for a in self.client.attackers:
            other_speed = Vector(a.run_speed.x * -d, 
                                 a.run_speed.y * self.client.direction.y)
            speed = speed - other_speed * random.uniform(0.5, 1.5)
            if speed.length() > self.client.run_speed.length():
                speed = speed.unit() * self.client.run_speed.length()
            if self.client.stemina <= 0:
                self.client.stemina = 0
                return
            self.client.stemina -= 2

        self.client.position += speed * game_framework.dt

    def run(self):
        pass

    def dash(self):
        self.exit()
        self.client.current_state = self.client.dash_state
        self.client.startAnimation()
        self.client.current_state.frame = self.frame

    def idle(self):
        self.exit()
        self.client.current_state = self.client.idle_state
        self.client.startAnimation()

    def grab(self):
        self.exit()
        self.client.current_state = self.client.grab_state
        self.client.startAnimation()

    def grabbed(self):
        pass

    def tackle(self):
        self.exit()
        self.client.current_state = self.client.tackle_state
        self.client.startAnimation()

    def release(self):
        pass

    def fall(self):
        self.exit()
        self.client.current_state = self.client.fall_state
        self.client.startAnimation()


class DashState(RunState):
    def __init__(self, client):
        super().__init__(client)

    def update(self):
        if self.client.stemina <= 0:
            self.client.stemina = 0
            self.run()
            return
        self.client.stemina -= 2
        
        speed = Vector(self.client.run_speed.x * self.client.direction.x, 
                       self.client.run_speed.y * self.client.direction.y) * 1.5
        
        self._update(speed)

    def run(self):
        self.exit()
        self.client.current_state = self.client.run_state
        self.client.startAnimation()
        self.client.current_state.frame = self.frame

    def dash(self):
        pass


class GrabState(State):
    def __init__(self, client):
        super().__init__(client)

    def run(self):
        pass

    def dash(self):
        pass

    def idle(self):
        pass

    def grab(self):
        pass

    def grabbed(self):
        pass

    def tackle(self):
        self.exit()
        self.client.current_state = self.client.tackle_state
        self.client.startAnimation()

    def release(self):
        self.exit()
        self.client.current_state = self.client.idle_state
        self.client.startAnimation()

    def fall(self):
        self.exit()
        self.client.current_state = self.client.fall_state
        self.client.startAnimation()


class TackleState(State):
    def __init__(self, client):
        super().__init__(client)
        self.fps = 20
        self._clip_points: List[Point] = [Point(420, 0)] * 5
        y = 318
        self._clip_points += [Point(481, y), Point(550, y), Point(625, y), 
                              Point(713, y), Point(794, y), Point(794+72+1, y)]
        self._clip_width = [70]*5 + [68, 74, 87, 80, 72, 80]
        self._clip_height = 120

        self.RUN_SPEED_MPS = 10

    def enter(self, event=None):
        self.frame = 0

    def update(self, event=None):
        if self.frame >= len(self._clip_points)-1:
            self.frame = 0
            self.exit()
            self.client.current_state = self.client.idle_state
            self.client.startAnimation()
        elif self.frame >= 5:
            self.client.position += self.client.tackle_to * self.RUN_SPEED_MPS * game_framework.dt
        
        if self.client.tackle_to.x > 0:
            self.client.flip = False
        elif self.client.tackle_to.x < 0:
            self.client.flip = True

    def run(self):
        pass

    def dash(self):
        pass

    def idle(self):
        pass

    def grab(self):
        pass

    def grabbed(self):
        pass

    def tackle(self):
        pass

    def release(self):
        pass

    def fall(self):
        self.exit()
        self.client.current_state = self.client.fall_state
        self.client.startAnimation()


class FallState(State):
    def __init__(self, client):
        super().__init__(client)
        self.fps = 5
        self._clip_points = [Point(620, 0), Point(695, 0), Point(695, 0), 
                             Point(805, 0), Point(805, 0), Point(805, 0)]
        self._clip_width = [68, 110, 110, 85, 85, 85]
        self._clip_height = 120

    def enter(self, event=None):
        if self.client.fall_to.x > 0:
            self.client.flip = False
        elif self.client.fall_to.x < 0:
            self.client.flip = True
        self.frame = 0

    def update(self, event=None):
        self.client.release()
        if self.frame >= len(self._clip_points)-1:
            self.exit()
            self.client.current_state = self.client.idle_state
            self.client.startAnimation()
            return
        
        self.client.position += self.client.fall_to * game_framework.dt

    def run(self):
        pass        # 넘여져 있을때는 아무것도 못함

    def dash(self):
        pass

    def idle(self):
        pass

    def grab(self):
        pass

    def grabbed(self):
        pass

    def tackle(self):
        pass

    def release(self):
        pass

    def fall(self):
        pass
