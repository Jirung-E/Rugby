import random

from pico2d import *

import Game.game_framework as game_framework
import Game.world as world
from Game.GameObject import *
from Math import *


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()

def init():
    pass

def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    
    update_canvas()


def pause():
    pass


def resume():
    pass

