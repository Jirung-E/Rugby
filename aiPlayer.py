from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_LEFT, SDL_KEYUP, SDLK_RIGHT, SDLK_a

import random


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def time_out(e):
    return e[0] == 'TIME_OUT'


class Idle:
    @staticmethod
    def enter(boy, e):
        print('Idle Enter')
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3
        boy.dir = 0
        boy.frame = 0
        boy.start_time = get_time()

    @staticmethod
    def exit(boy, e):
        print('Idle Exit')

    @staticmethod
    def do(boy):
        print('Idle Do')
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.handle_event(('TIME_OUT', None))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100,
                            100, 100,
                            boy.x, boy.y)


class Run:
    @staticmethod
    def enter(boy, e):
        if boy.action == 3:
            boy.dir = 1
            boy.action = 1
        elif boy.action == 2:
            boy.dir = -1
            boy.action = 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * boy.speed

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100,
                            100, 100,
                            boy.x, boy.y)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        # self.cur_state = Run
        self.table = {
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Run},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
        }

    def start(self):
        self.cur_state.enter(self.boy, ('START', None))

    def update(self):
        self.cur_state.do(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True  # 성공적으로 이벤트 변환
        return False  # 이벤트를 소모하지 못함

    def draw(self):
        self.cur_state.draw(self.boy)


class AIPlayer:
    image = None
    
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.dir = 0
        self.speed = random.uniform(1.0, 3.0)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        if AIPlayer.image is None:
            AIPlayer.image = load_image('res/animation_sheet.png')

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
