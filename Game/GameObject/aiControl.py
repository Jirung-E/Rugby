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
        if self.client.grabbed_opponent is not None:
            if self.client.ball is None:
                self.client.release()
        if self.client.ball is not None:
            self.run_to_goal()
            if self.client.position.x > play_scene.field.width/2-2:
                self.client.throw_half_power(0, 0)
            elif self.client.position.x < -play_scene.field.width/2+2:
                self.client.throw_half_power(0, 0)
        else:
            self.client.current_state.idle()
            if play_scene.ball.owner is None:
                # 가장 가까운 한명이 공을 가지러 간다. -> aiControl에서 처리하면 비효율적임 -> handle_event에서 넘겨주기?
                # 아니면 월드에서 업데이트 할때마다 거리정보 업데이트?
                # self.run_to_ball()
                pass
            else:
                if play_scene.ball.owner.team == self.client.team:
                    self.client.current_state.idle()
                # else:
                #     self.run_to_ball()

        if self.client.team == 1:
            self.client.direction.x = 1
            self.client.flip = False
        else:
            self.client.direction.x = -1
            self.client.flip = True

    def handle_event(self, event):
        if self.client.direction.x == 0 and self.client.direction.y == 0:
            self.client.current_state.idle()
        else:
            # self.client.current_state.run()
            if self.client.direction.x > 0:
                self.client.flip = False
            elif self.client.direction.x < 0:
                self.client.flip = True

    def run_to_goal(self):
        if self.client.stemina > 50:
            self.client.current_state.run()
            # self.client.current_state.dash()
        # elif self.client.stemina > 0:
        #     self.client.current_state.run()
        else:
            self.client.throw_half_power(0, 0)

    def run_to_home(self):
        pass

    def run_to_ball(self):
        target = play_scene.ball.position
        self.client.direction.x = target.x - self.client.position.x
        self.client.direction.y = target.y - self.client.position.y
        self.client.direction.normalize()
        self.client.current_state.run()
                    
    def handle_collision(self, group, other):
        if group == "ball:player":
            self.client.catch(other)
            return
        
        if group == "player:player":
            if other.ball is None:
                return
            self.client.grab(other)
