from pico2d import *

import Game.game_framework as game_framework
import Game.play_scene as play_scene
import Game.lobby_scene as lobby_scene


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(lobby_scene)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_scene)

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

