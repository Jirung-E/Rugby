from pico2d import open_canvas, close_canvas

import Game.game_framework as game_framework
import Game.lobby_scene as start_scene


open_canvas(game_framework.width, game_framework.height)
game_framework.run(start_scene)
close_canvas()
