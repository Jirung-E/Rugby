import random

from pico2d import *

import Game.game_framework as game_framework
import Game.world as world
import Game.lobby_scene as lobby_scene
import Game.result_scene as result_scene
from Game.GameObject import *
from Math import *

window_center = Point(game_framework.width/2, game_framework.height/2)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(lobby_scene)
        else:
            player.handle_event(event)

def init():
    global field
    global ball
    global ball_shadow
    global team
    global player
    global stemina_bar
    global goal_zone
    global score_board

    field = Field()
    world.add_object(field, world.BACKGROUND_LAYER)

    ball = Ball()
    ball.position = Point(0, 0)
    world.add_object(ball, world.OBJECT_LAYER)
    world.add_collision_pair("ball:player", ball, None)

    ball_shadow = Shadow(ball, Point(0, -10))
    ball_shadow.position = Point(0, 0)
    world.add_object(ball_shadow, world.SHADOW_LAYER)

    team_image = [ load_image('res/player1.png'), load_image('res/player2.png') ]

    team = {}
    player_team = random.randrange(2)
    left_end = -field.width / 2
    bottom_end = -field.height / 2
    dist = field.height / 12
    member = 11
    for t in range(2):
        team[t] = [Player() for _ in range(member)]
        for i in range(member):
            x = left_end+3 + t * (field.width-6)
            team[t][i].position.x = x
            team[t][i].position.y = bottom_end + dist * (i+1)
            team[t][i].y_fix = team[t][i].position.y
            team[t][i].controller = AIControl(team[t][i])
            if t == player_team:
                team[t][i].controller.__bt_update_delay = 0.5
            else:
                team[t][i].controller.__bt_update_delay = 0.3
                # team[t][i].stemina_regen = 7
                team[t][i].run_speed *= 1.05
            team[t][i].image = team_image[t]
            team[t][i].team = t+1
            world.add_collision_pair("ball:player", None, team[t][i])
            if t == 0:
                world.add_collision_pair("player:player", team[0][i], None)
            else:
                world.add_collision_pair("player:player", None, team[1][i])
    world.add_objects(team[0], world.OBJECT_LAYER)
    world.add_objects(team[1], world.OBJECT_LAYER)

    num = random.randrange(member)
    player = team[player_team][num]
    player.controller = Controllable(player)

    stemina_bar = SteminaBar()
    score_board = [ScoreBoard(1), ScoreBoard(2)]
    world.add_objects(score_board, world.UI_LAYER)

    goal_zone = [GoalZone(1), GoalZone(2)]
    goal_zone[0].position = Point(left_end+1, 0)
    world.add_collision_pair("ball:goal_zone", ball, goal_zone[0])
    goal_zone[1].position = Point(field.width/2-1, 0)
    world.add_collision_pair("ball:goal_zone", None, goal_zone[1])
    world.add_objects(goal_zone, world.BACKGROUND_LAYER)


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

