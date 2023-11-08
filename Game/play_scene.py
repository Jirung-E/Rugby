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
    global team1, team2
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

    team1_image = load_image('res/player1.png')
    team2_image = load_image('res/player2.png')

    team1 = [Player() for _ in range(0, 11)]
    for i in range(11):
        team1[i].position.x = random.randint(100-20, 100+20)
        team1[i].position.y = 20 + i * 50
        team1[i].controller = AIControl(team1[i])
        team1[i].image = team1_image
        team1[i].team = 1
        world.add_collision_pair("ball:player", None, team1[i])
    team2 = [Player() for _ in range(0, 11)]
    for i in range(11):
        team2[i].position.x = random.randint(700-20, 700+20)
        team2[i].position.y = 20 + i * 50
        team2[i].controller = AIControl(team2[i])
        team2[i].flip = True
        team2[i].image = team2_image
        team2[i].team = 2
        world.add_collision_pair("ball:player", None, team2[i])
    world.add_objects(team1, world.OBJECT_LAYER)
    world.add_objects(team2, world.OBJECT_LAYER)

    num = random.randrange(11)
    team = random.randrange(2)
    if team == 0:
        player = team1[num]
    else:
        player = team2[num]
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

