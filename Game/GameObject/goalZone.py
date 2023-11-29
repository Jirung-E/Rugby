from Math import *
import Game.game_framework as game_framework
import Game.play_scene as play_scene

import random
from pico2d import draw_rectangle


class GoalZone:
    def __init__(self, team):
        self.position = Point(0, 0)
        self.width = 2
        self.height = play_scene.field.height/2
        self.team = team

    def update(self):
        pass

    def draw(self):
        draw_position = -play_scene.player.position * game_framework.PIXEL_PER_METER + play_scene.window_center
        
        x1, y1, x2, y2 = self.get_bb()
        x1 = x1 * game_framework.PIXEL_PER_METER
        y1 = y1 * game_framework.PIXEL_PER_METER
        x2 = x2 * game_framework.PIXEL_PER_METER
        y2 = y2 * game_framework.PIXEL_PER_METER
        x1 += draw_position.x
        y1 += draw_position.y
        x2 += draw_position.x
        y2 += draw_position.y
        
        draw_rectangle(x1, y1, x2, y2)

    def get_bb(self):
        return (self.position.x - self.width/2, self.position.y - self.height, 
                self.position.x + self.width/2, self.position.y + self.height)
    
    def handle_collision(self, group, other):
        if group == "ball:goal_zone":
            if other.owner is not None:
                if other.owner.team == self.team:
                    return
                play_scene.score_board[self.team & 1].score += 1
                throw_y = random.uniform(play_scene.field.height/2, -play_scene.field.height/2)
                if other.owner.team == 1:
                    other.owner.throw_half_power(0, throw_y)
                elif other.owner.team == 2:
                    other.owner.throw_half_power(0, throw_y)
                return
            else:
                if self.team == 1:
                    other.velocity.x = abs(other.velocity.x)
                elif self.team == 2:
                    other.velocity.x = -abs(other.velocity.x)
                return
