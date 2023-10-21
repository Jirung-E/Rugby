from GameObject import *
from Math import *

import random

from pico2d import *


class Game:
    def __init__(self):
        open_canvas(800, 600)
        self.background = Field()
        self.resetWorld()

    def __del__(self):
        close_canvas()

    def resetWorld(self):
        self.playing = True
        self.world = []

        team1_image = load_image('res/player1.png')
        team2_image = load_image('res/player2.png')

        team1 = [Player() for _ in range(0, 11)]
        for i in range(11):
            team1[i].position.x = random.randint(100-20, 100+20)
            team1[i].position.y = 50 + i * 60
            team1[i].controller = AIControl(team1[i])
            team1[i].image = team1_image
        team2 = [Player() for _ in range(0, 11)]
        for i in range(11):
            team2[i].position.x = random.randint(700-20, 700+20)
            team2[i].position.y = 50 + i * 60
            team2[i].controller = AIControl(team2[i])
            team2[i].controller.flip = True
            team2[i].image = team2_image
        self.world += team1
        self.world += team2

        num = random.randrange(11)
        team = random.randrange(2)
        if team == 0:
            self.player = team1[num]
        else:
            self.player = team2[num]
        self.player.position = Point(400, 300)
        self.player.controller = Controllable(self.player)

        ball = Ball()
        ball.position = Point(400, 300)
        self.world.append(ball)

    def addObject(self, obj):
        self.world.append(obj)

    def handleEvents(self):
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                self.playing = False
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                self.playing = False
            else:
                self.player.handle_event(event)

    def update(self):
        for o in self.world:
            o.update()

    def render(self):
        clear_canvas()
        self.background.draw()
        self.world.sort(key=lambda o: o.position.y, reverse=True)
        for o in self.world:
            o.draw()
        update_canvas()

    def play(self):
        while self.playing:
            self.handleEvents()
            self.update()
            self.render()
            delay(0.01)