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
    global win_text
    global lose_text
    global win_bg
    global lose_bg
    win_text = load_image('res/win.png')
    lose_text = load_image('res/lose.png')
    win_bg = load_image('res/win_bg.png')
    lose_bg = load_image('res/lose_bg.jpg')

def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    if play_scene.score_board[play_scene.player.team-1].score > play_scene.score_board[play_scene.player.team & 1].score:
        aspect = game_framework.height / win_bg.h
        win_bg.draw(game_framework.window_center.x, game_framework.window_center.y, win_bg.w * aspect, game_framework.height)
        win_text.draw(game_framework.window_center.x, game_framework.window_center.y)
    else:
        aspect = game_framework.height / lose_bg.h
        lose_bg.draw(game_framework.window_center.x, game_framework.window_center.y, lose_bg.w * aspect, game_framework.height)
        lose_text.draw(game_framework.window_center.x, game_framework.window_center.y)
    update_canvas()


def pause():
    pass


def resume():
    pass

