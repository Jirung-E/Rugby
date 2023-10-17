from GameObject.controller import Controller


class AIControl(Controller):
    def __init__(self, character):
        super().__init__(character)

    def draw(self):
        self.client.image.clip_draw(self.client.frame * 100, self.client.action * 100,
                                    100, 100,
                                    self.client.x, self.client.y)