from pico2d import *

import Game.game_framework as game_framework
import Game.play_scene as play_scene


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.change_mode(play_scene)

def init():
    global bg_image
    bg_image = load_image('res/bg_image.png')

def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    aspect = game_framework.height / bg_image.h
    bg_image.draw(get_canvas_width()//2+50, get_canvas_height()//2, bg_image.w * aspect, game_framework.height)
    update_canvas()


def pause():
    pass


def resume():
    pass

