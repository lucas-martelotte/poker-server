from data.components.gui.button import Button
import pygame

class CardButton(Button):

    card_path = 'data/resources/img/cards/'

    def __init__(self, rect, index, card):
        self.index = index
        self.card  = card
        image = pygame.image.load(CardButton.card_path + card + '.png')
        super().__init__(rect = rect, image = image, border=1, velocity=30)

    def set_card(self, card):
        self.set_image(pygame.image.load(CardButton.card_path + card + '.png'))