from pico2d import open_canvas, close_canvas

import Game.game_framework as game_framework
import Game.play_scene as start_scene


open_canvas(start_scene.width, start_scene.height)
game_framework.run(start_scene)
close_canvas()
