from GameObject.controller import Controller


class AIControl(Controller):
    def __init__(self, character):
        super().__init__(character)

    def update(self):
        pass

    def handle_event(self, event):
        pass

    def draw(self):
        self.client.image.clip_draw(100, 100,
                                    100, 100,
                                    self.client.position.x, self.client.position.y)