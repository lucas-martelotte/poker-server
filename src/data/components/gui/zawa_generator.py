from data.components.gui.button import Button
from data.components.mixer import Mixer
import pygame
import random

class ZawaGenerator():

    ZAWA_BASE_WIDTH  = 146
    ZAWA_BASE_HEIGHT = 64

    zawa_image = pygame.image.load("./data/resources/img/general/zawa.png")


    def __init__(self, rect):
        self.zawas = []
        self.rect = rect

    def render(self, screen):
        indexes_to_delete = []
        for zawa_index, zawa in enumerate(self.zawas):
            zawa.render(screen)
            if not zawa.target_pos:
                indexes_to_delete.append(zawa_index)
        indexes_to_delete.sort(reverse=True)
        for index in indexes_to_delete:
            del self.zawas[index]

    def generate_zawa(self, probability=0.001):
        seed = random.uniform(0, 1)
        if seed <= probability:
            x_pos = self.rect[0] + random.uniform(0, 1)*(self.rect[2] - 2*ZawaGenerator.ZAWA_BASE_WIDTH)
            y_pos = self.rect[1] + random.uniform(0, 1)*self.rect[3]//2
            self.zawas.append(Button([x_pos, y_pos, ZawaGenerator.ZAWA_BASE_WIDTH, ZawaGenerator.ZAWA_BASE_HEIGHT],
                                     target_pos =  [x_pos + ZawaGenerator.ZAWA_BASE_WIDTH, y_pos],
                                     image=ZawaGenerator.zawa_image, velocity=5))
            Mixer.play(Mixer.ZAWA_SOUND, volume=0.05)