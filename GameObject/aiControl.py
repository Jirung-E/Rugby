from GameObject.controller import Controller

import random


class AIControl(Controller):
    def __init__(self, client):
        super().__init__(client)

    def update(self):
        if self.client.ball is not None:
            if self.client.position.x > 700:
                self.client.throw(500, 300)
            elif self.client.position.x < 100:
                self.client.throw(300, 300)
            self.client.current_state.run()
            self.client.dash = True
            if self.client.team == 1:
                self.client.direction.x = 1
                self.client.flip = False
            else:
                self.client.direction.x = -1
                self.client.flip = True
        else:
            self.client.current_state.idle()
            self.client.direction.x = 0
            self.client.direction.y = 0

    def handle_event(self, event):
        if self.client.direction.x == 0 and self.client.direction.y == 0:
            self.client.current_state.idle()
        else:
            self.client.current_state.run()
            if self.client.direction.x > 0:
                self.client.flip = False
            elif self.client.direction.x < 0:
                self.client.flip = True
                