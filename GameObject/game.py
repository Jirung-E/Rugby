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

        team1 = [Player() for _ in range(0, 11)]
        for i in range(11):
            team1[i].position.x = random.randint(100-20, 100+20)
            team1[i].position.y = 50 + i * 30
            team1[i].controller = AIControl(team1[i])
            team1[i].image = team1_image
            team1[i].team = 1
        team2 = [Player() for _ in range(0, 11)]
        for i in range(11):
            team2[i].position.x = random.randint(700-20, 700+20)
            team2[i].position.y = 50 + i * 60
            team2[i].controller = AIControl(team2[i])
            team2[i].controller.flip = True
            team2[i].image = team2_image
            team2[i].team = 2
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

        self.ball = Ball()
        self.ball.position = Point(400, 300)
        self.world.append(self.ball)

    def addObject(self, obj):
        self.world.append(obj)

    def __throwBall(self):
        if self.ball.owner.team == 1 and self.ball.owner.direction.x > 0:
            return
        if self.ball.owner.team == 2 and self.ball.owner.direction.x < 0:
            return
        
        self.ball.owner.caught = False
        self.ball.velocity.x = self.ball.owner.direction.x * self.ball.owner.run_speed.x
        self.ball.velocity.y = self.ball.owner.direction.y * self.ball.owner.run_speed.y
        self.ball.owner = None
        self.ball.velocity_z = 3
        self.ball.rotate_power = random.uniform(0.1, 0.15)

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