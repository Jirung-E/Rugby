from pico2d import load_image

# import Game.play_scene as play_scene      # 플레이어 위치에 따라 배경 스크롤


class Field:
    def __init__(self):
        self.image = load_image('res/field.jpg')

    def draw(self):
        self.image.draw(400, 300, 800, 600)

    def update(self):
        pass
