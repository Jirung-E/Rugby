from Game.GameObject.controller import Controller
import Game.play_scene as play_scene
import Game.world as world
from Game.GameObject.ball import Ball
from Game.GameObject.player import Player
from Math import Point

import random


class AIControl(Controller):
    def __init__(self, client):
        super().__init__(client)

    def update(self):
        if self.client.ball is not None:
            self.run_to_goal()
            if len(self.client.attackers) > 1:      # 안던지는거같은데...
                self.client.throw(self.client.position.x - (self.client.team*2-1)*100, 300)
            if self.client.position.x > 700:
                self.client.throw(500, 300)
            elif self.client.position.x < 100:
                self.client.throw(300, 300)
        else:
            if play_scene.ball.owner is None:
                # 가장 가까운 한명이 공을 가지러 간다. -> aiControl에서 처리하면 비효율적임 -> handle_event에서 넘겨주기?
                # 아니면 월드에서 업데이트 할때마다 거리정보 업데이트?
                self.run_to_ball()
            else:
                if play_scene.ball.owner.team == self.client.team:
                    self.client.current_state.idle()
                else:
                    distance = Point.distance(self.client.position, play_scene.ball.owner.position)
                    if distance < 10:
                        self.try_grab()
                    else:
                        self.run_to_ball()

            # self.run_to_ball()
            # self.client.current_state.idle()
            # self.client.direction.x = 0
            # self.client.direction.y = 0

    def handle_event(self, event):
        if self.client.direction.x == 0 and self.client.direction.y == 0:
            self.client.current_state.idle()
        else:
            self.client.current_state.run()
            if self.client.direction.x > 0:
                self.client.flip = False
            elif self.client.direction.x < 0:
                self.client.flip = True

    def run_to_goal(self):
        if self.client.stemina > 50:
            self.client.current_state.dash()
        elif self.client.stemina > 0:
            self.client.current_state.run()
        else:
            self.client.throw(400, 300)

        if self.client.team == 1:
            self.client.direction.x = 1
            self.client.flip = False
        else:
            self.client.direction.x = -1
            self.client.flip = True

    def run_to_ball(self):
        target = play_scene.ball.position
        self.client.direction.x = target.x - self.client.position.x
        self.client.direction.y = target.y - self.client.position.y
        self.client.direction.normalize()
        self.client.current_state.run()

    def try_grab(self):
        if self.client.ball is not None:
            return
        if self.client.grabbed_opponent is not None:
            return
        
        for o in world.objects[world.OBJECT_LAYER]:
            if o is self.client:
                continue
            elif isinstance(o, Player):
                if o.ball is not None:
                    if o.team != self.client.team:
                        self.client.grabbed_opponent = o
                        o.attackers.append(self.client)
                        self.client.grabbed_offset = Point(o.position.x - self.client.position.x, o.position.y - self.client.position.y)
                        return
                    
    def handle_collision(self, group, other):
        if group == "ball:player":
            self.client.catch(other)
        elif group == "player:player":
            if other.ball is not None:
                self.client.grab(other)
