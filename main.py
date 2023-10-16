from pico2d import *

import random

from field import Field
from boy import Boy
from aiPlayer import AIPlayer


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            boy.handle_event(event)


def reset_world():
    global running
    global grass
    global team
    global world
    global boy
    global team1
    global team2

    running = True
    world = []

    field = Field()
    world.append(field)

    boy = Boy()
    world.append(boy)

    team1 = [AIPlayer() for i in range(0, 11)]
    for i in range(0, 11):
        team1[i].x = random.randint(100-20, 100+20)
        team1[i].y = 50 + i * 60
        team1[i].action = 3
    team2 = [AIPlayer() for i in range(0, 11)]
    for i in range(0, 11):
        team2[i].x = random.randint(700-20, 700+20)
        team2[i].y = 50 + i * 60
        team2[i].action = 2
    world += team1
    world += team2


def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
