import random

from pico2d import *

import Game.game_framework as game_framework
import Game.world as world
from Game.GameObject import *
from Math import *


WIDTH = 800
HEIGHT = 600


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)

def init():
    global background
    global ball
    global ball_shadow
    global team
    global player

    background = Field()
    world.add_object(background, world.BACKGROUND_LAYER)

    ball = Ball()
    ball.position = Point(400, 300)
    world.add_object(ball, world.OBJECT_LAYER)
    world.add_collision_pair("ball:player", ball, None)

    ball_shadow = Shadow(ball, Point(0, -10))
    ball_shadow.position = Point(400, 300)
    world.add_object(ball_shadow, world.SHADOW_LAYER)

    team_image = [ load_image('res/player1.png'), load_image('res/player2.png') ]

    team = {}
    for t in range(2):
        team[t] = [Player() for _ in range(0, 11)]
        for i in range(11):
            x = 100 + t * 600
            team[t][i].position.x = random.randint(x-20, x+20)
            team[t][i].position.y = 20 + i * 50
            team[t][i].controller = AIControl(team[t][i])
            team[t][i].image = team_image[t]
            team[t][i].team = t+1
            world.add_collision_pair("ball:player", None, team[t][i])
            if t == 0:
                world.add_collision_pair("player:player", team[0][i], None)
            else:
                world.add_collision_pair("player:player", None, team[1][i])
    world.add_objects(team[0], world.OBJECT_LAYER)
    world.add_objects(team[1], world.OBJECT_LAYER)

    num = random.randrange(11)
    t = random.randrange(2)
    player = team[t][num]
    player.position = Point(400, 300)
    player.controller = Controllable(player)
    world.collision_pairs["ball:player"][1].remove(player)


def finish():
    world.clear()
    pass


def update():
    world.update()
    world.handle_collisions()


def draw():
    clear_canvas()
    world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass

