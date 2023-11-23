from pico2d import Image, load_image


class SteminaBar:
    def __init__(self):
        self.stemina_image: Image = load_image('res/stemina_bar_high.png')
        self.frame_image: Image = load_image('res/stemina_bar_frame_high.png')

    def draw(self, stemina, max_stemina, x, y):
        # self.frame_image.draw(x, y, 64, 16)
        self.frame_image.draw_to_origin(x-32, y, 64, 16)
        r = stemina / max_stemina
        # self.stemina_image.draw(x-int(32*(1-r)), y, int(64*r), 16)
        self.stemina_image.draw_to_origin(x-32, y, int(64*r), 16)
