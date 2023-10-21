from pico2d import *

import random

# from Player import AIPlayer
# from Player import Player
from GameObject import *
from Math import *


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
    global ball

    running = True
    world = []

    field = Field()
    # world.append(field)

    team1_image = load_image('res/player1.png')
    team2_image = load_image('res/player2.png')

    team1 = [Player() for _ in range(0, 11)]
    for i in range(11):
        team1[i].position.x = random.randint(100-20, 100+20)
        team1[i].position.y = 50 + i * 60
        team1[i].controller = AIControl(team1[i])
        team1[i].image = team1_image
    team2 = [Player() for _ in range(0, 11)]
    for i in range(11):
        team2[i].position.x = random.randint(700-20, 700+20)
        team2[i].position.y = 50 + i * 60
        team2[i].controller = AIControl(team2[i])
        team2[i].controller.flip = True
        team2[i].image = team2_image
    world += team1
    world += team2

    num = random.randrange(11)
    team = random.randrange(2)
    if team == 0:
        player = team1[num]
    else:
        player = team2[num]
    player.position = Point(400, 300)
    player.controller = Controllable(player)

    ball = Ball()
    ball.position = Point(400, 300)
    world.append(ball)


def update_world():
    for o in world:
        o.update()


def render_world():
    clear_canvas()
    field.draw()
    world.sort(key=lambda o: o.position.y, reverse=True)
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
