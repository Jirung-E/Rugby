from GameObject.controller import Controller


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir_x = 0
        self.dir_y = 0
        self.run_speed_x = 5
        self.run_speed_y = 2

        self.controller: Controller = None

        self.frame = 0
        self.action = 3

        self.image = None

    def update(self):
        self.controller.update()

    def handle_event(self, event):
        self.controller.handle_event(('INPUT', event))

    def draw(self):
        self.controller.draw()

'''
## AI & 플레이어
겹치는 부분: +, 다른 부분: -
+ 이동속도
+ 애니메이션
+ 상태변화
+ 이미지..?
- 플레이어는 키보드로 조작, AI는 자동으로 움직임
'''