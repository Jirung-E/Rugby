from Math import *
import Game.game_framework as game_framework
import Game.play_scene as play_scene

from pico2d import load_image, Image, get_canvas_width, get_canvas_height


class ScoreBoard:       # 2자리까지 표현
    image: Image = None

    def __init__(self, team):
        self.w = 192
        self.h = 240
        self.draw_w = self.w/4
        self.draw_h = self.h/4
        self.position = Point(get_canvas_width()/2 - self.draw_w*2 * (3 - team*2), self.draw_h)
        self.score = 0
        if ScoreBoard.image is None:
            ScoreBoard.image = load_image('res/numbers.png')

    def update(self):
        pass

    def draw(self):
        print(self.score)

        digit10 = self.score // 10
        digit1 = self.score % 10

        ScoreBoard.image.clip_draw(int(digit10%5)*(self.w+10), int(1-digit10//5)*self.h, self.w-20, self.h-20, self.position.x - self.draw_w/2, self.position.y, self.draw_w, self.draw_h)
        ScoreBoard.image.clip_draw(int(digit1%5)*(self.w+10), int(1-digit1//5)*self.h, self.w-20, self.h-20, self.position.x + self.draw_w/2, self.position.y, self.draw_w, self.draw_h)
