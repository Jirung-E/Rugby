from GameObject import *
from Math import *

import random

from pico2d import *


class Game:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600
        open_canvas(self.WIDTH, self.HEIGHT)
        self.background = Field()
        self.resetWorld()

    def __del__(self):
        close_canvas()

    def resetWorld(self):
        self.playing = True
        self.world = []

        team1_image = load_image('res/player1.png')
        team2_image = load_image('res/player2.png')

        self.team1 = [Player() for _ in range(0, 11)]
        for i in range(11):
            self.team1[i].position.x = random.randint(100-20, 100+20)
            self.team1[i].position.y = 50 + i * 50
            self.team1[i].controller = AIControl(self.team1[i])
            self.team1[i].image = team1_image
            self.team1[i].team = 1
        self.team2 = [Player() for _ in range(0, 11)]
        for i in range(11):
            self.team2[i].position.x = random.randint(700-20, 700+20)
            self.team2[i].position.y = 50 + i * 50
            self.team2[i].controller = AIControl(self.team2[i])
            self.team2[i].controller.flip = True
            self.team2[i].image = team2_image
            self.team2[i].team = 2
        self.world += self.team1
        self.world += self.team2

        num = random.randrange(11)
        team = random.randrange(2)
        if team == 0:
            self.player = self.team1[num]
        else:
            self.player = self.team2[num]
        self.player.position = Point(400, 300)
        self.player.controller = Controllable(self.player)

        self.ball = Ball()
        self.ball.position = Point(400, 300)
        self.world.append(self.ball)

    def addObject(self, obj):
        self.world.append(obj)

    def handleEvents(self):
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                self.playing = False
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                self.playing = False
                
            elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
                self.player.catch(self.ball)
            elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
                self.player.throw(event.x, self.HEIGHT - event.y)
            else:
                self.player.handle_event(event)

    def update(self):
        for o in self.world:
            o.update()
        if self.ball.owner is None:
            for o in self.team1:
                if o is self.player:
                    continue
                if Point.distance2(o.position, self.ball.position) < 30**2:
                    o.catch(self.ball)
                    return
            for o in self.team2:
                if o is self.player:
                    continue
                if Point.distance2(o.position, self.ball.position) < 30**2:
                    o.catch(self.ball)
                    return

    def render(self):
        clear_canvas()
        self.background.draw()
        self.world.sort(key=lambda o: o.position.y, reverse=True)
        self.ball.drawShadow()
        for o in self.world:
            o.draw()
        update_canvas()

    def play(self):
        while self.playing:
            self.handleEvents()
            self.update()
            self.render()
            delay(0.01)