from Math import *
import Game.game_framework as game_framework
import Game.play_scene as play_scene

from pico2d import draw_rectangle


class GoalZone:
    def __init__(self):
        self.position = Point(0, 0)

    def update(self):
        pass

    def draw(self):
        x1, y1, x2, y2 = self.get_bb()
        x1 = x1 + -play_scene.player.position.x + play_scene.window_center.x
        y1 = y1 + -play_scene.player.position.y + play_scene.window_center.y
        x2 = x2 + -play_scene.player.position.x + play_scene.window_center.x
        y2 = y2 + -play_scene.player.position.y + play_scene.window_center.y
        draw_rectangle(x1, y1, x2, y2)

    def get_bb(self):
        return (self.position.x - 80, self.position.y - 160, self.position.x + 80, self.position.y + 160)
    
    def handle_collision(self, group, other):
        pass
