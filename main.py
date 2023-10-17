from pico2d import *

import random

# from Player import AIPlayer
# from Player import Player
from GameObject import *


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)


def reset_world():
    global running
    global field
    global world
    global team1
    global team2
    global player

    running = True
    world = []

    field = Field()
    world.append(field)

    # 여기서 이미지 로드해서 인자로 넘겨주기
    team1_image = load_image('res/animation_sheet.png')
    team2_image = load_image('res/animation_sheet.png')

    team1 = [Player() for _ in range(0, 11)]
    for i in range(11):
        team1[i].x = random.randint(100-20, 100+20)
        team1[i].y = 50 + i * 60
        team1[i].controller = AIControl(team1[i])
        team1[i].action = 3
        team1[i].image = team1_image
    team2 = [Player() for _ in range(0, 11)]
    for i in range(11):
        team2[i].x = random.randint(700-20, 700+20)
        team2[i].y = 50 + i * 60
        team2[i].controller = AIControl(team2[i])
        team2[i].action = 2
        team2[i].image = team2_image
    world += team1
    world += team2

    num = random.randrange(11)
    team = random.randrange(2)
    if team == 0:
        player = team1[num]
    else:
        player = team2[num]
    player.controller = Controllable(player)


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

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
