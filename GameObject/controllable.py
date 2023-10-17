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


def w_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w


def w_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w


def s_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s


def s_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s


class Idle:
    @staticmethod
    def enter(client, e):
        print('Idle Enter')
        if client.action == 0:
            client.action = 2
        elif client.action == 1:
            client.action = 3
        client.frame = 0
        # client.start_time = get_time()

    @staticmethod
    def exit(client, e):
        print('Idle Exit')

    @staticmethod
    def do(client):
        print('Idle Do')
        client.frame = (client.frame + 1) % 8
        # if get_time() - client.start_time > 3:
        #     client.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(client):
        client.image.clip_draw(client.frame * 100, client.action * 100,
                            100, 100,
                            client.x, client.y)
        

class Run:
    @staticmethod
    def enter(client, e):
        if client.dir_x > 0:
            client.action = 1
        elif client.dir_x < 0:
            client.action = 0
        else:
            if client.action == 2:
                client.action = 0
            elif client.action == 3:
                client.action = 1

    @staticmethod
    def exit(client, e):
        pass

    @staticmethod
    def do(client):
        client.frame = (client.frame + 1) % 8
        client.x += client.dir_x * client.run_speed_x
        client.y += client.dir_y * client.run_speed_y

    @staticmethod
    def draw(client):
        client.image.clip_draw(client.frame * 100, client.action * 100,
                                100, 100,
                                client.x, client.y)


class Controllable(Controller):
    def __init__(self, client):
        super().__init__(client)
        self.current_state = Idle
        # self.table = {
        #     Idle: {d_down: Run, a_down: Run, d_up: Run, a_up: Run, w_down: Run, s_down: Run, w_up: Run, s_up: Run},
        #     Run: {d_down: Run, a_down: Run, d_up: Run, a_up: Run, w_down: Run, s_down: Run, w_up: Run, s_up: Run},
        # }
        self.start()

    def start(self):
        self.current_state.enter(self.client, None)

    def update(self):
        self.current_state.do(self.client)

    def handle_event(self, event):
        # for check_event, next_state in self.table[self.cur_state].items():
        #     if check_event(event):
        #         self.cur_state.exit(self.client, event)
        #         self.cur_state = next_state
        #         self.cur_state.enter(self.client, event)
        #         return True  # 성공적으로 이벤트 변환
        # return False  # 이벤트를 소모하지 못함
    
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.client.dir_x -= 1
            elif event.key == SDLK_d:
                self.client.dir_x += 1
            elif event.key == SDLK_w:
                self.client.dir_y += 1
            elif event.key == SDLK_s:
                self.client.dir_y -= 1
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_a:
                self.client.dir_x += 1
            elif event.key == SDLK_d:
                self.client.dir_x -= 1
            elif event.key == SDLK_w:
                self.client.dir_y -= 1
            elif event.key == SDLK_s:
                self.client.dir_y += 1

        if self.client.dir_x == 0 and self.client.dir_y == 0:
            self.current_state.exit(self.client, event)
            self.current_state = Idle
            self.current_state.enter(self.client, event)
        else:
            self.current_state.exit(self.client, event)
            self.current_state = Run
            self.current_state.enter(self.client, event)

    def draw(self):
        self.current_state.draw(self.client)