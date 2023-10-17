from GameObject.controller import Controller

from pico2d import get_time
from sdl2 import SDL_KEYDOWN, SDL_KEYUP, SDLK_w, SDLK_a, SDLK_s, SDLK_d


def d_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d


def d_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def a_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a


class Idle:
    @staticmethod
    def enter(client, e):
        print('Idle Enter')
        if client.action == 0:
            client.action = 2
        elif client.action == 1:
            client.action = 3
        client.dir = 0
        client.frame = 0
        client.start_time = get_time()

    @staticmethod
    def exit(client, e):
        print('Idle Exit')

    @staticmethod
    def do(client):
        print('Idle Do')
        client.frame = (client.frame + 1) % 8
        if get_time() - client.start_time > 3:
            client.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(client):
        client.image.clip_draw(client.frame * 100, client.action * 100,
                            100, 100,
                            client.x, client.y)
        

class Run:
    @staticmethod
    def enter(client, e):
        if d_down(e) or a_up(e):
            client.dir, client.action = 1, 1
        elif a_down(e) or d_up(e):
            client.dir, client.action = -1, 0

    @staticmethod
    def exit(client, e):
        pass

    @staticmethod
    def do(client):
        client.frame = (client.frame + 1) % 8
        client.x += client.dir * 5

    @staticmethod
    def draw(client):
        client.image.clip_draw(client.frame * 100, client.action * 100,
                            100, 100,
                            client.x, client.y)


class Controllable(Controller):
    def __init__(self, client):
        super().__init__(client)
        self.cur_state = Idle
        self.table = {
            Idle: {d_down: Run, a_down: Run, d_up: Run, a_up: Run},
            Run: {d_down: Idle, a_down: Idle, d_up: Idle, a_up: Idle},
        }
        self.start()

    def start(self):
        self.cur_state.enter(self.client, ('START', 0))

    def update(self):
        self.cur_state.do(self.client)

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.client, e)
                self.cur_state = next_state
                self.cur_state.enter(self.client, e)
                return True  # 성공적으로 이벤트 변환
        return False  # 이벤트를 소모하지 못함

    def draw(self):
        self.cur_state.draw(self.client)