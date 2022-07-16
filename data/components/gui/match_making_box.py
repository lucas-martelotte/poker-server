from data.components.gui.button import *
from data.components.font import *
from config import *
import config

class MatchMakingBox():

    SEARCHING = 0
    CONNECTED = 1
    FAILED = 2
    IDLE = 3
    FOUND = 4

    searching_image = pygame.image.load('data/resources/img/general/match_making_searching.png')
    failed_image = pygame.image.load('data/resources/img/general/match_making_failed.jpg')
    found_image = pygame.image.load('data/resources/img/general/match_making_found.png')

    def __init__(self):
        self.box = Button([WIDTH//2 - 200, HEIGHT//2-150, 400, 300], border=2)
        self.cancel_button = Button([WIDTH//2 - 100, HEIGHT//2+90, 200, 40], text='CANCEL', border=1)
        self.image_box = Button([WIDTH//2 - 150, HEIGHT//2-100, 300, 170], border=1)
        self.state = self.IDLE

        self.set_state(self.IDLE)

    def render(self, screen):
        self.box.render(screen)

        text = Font.font_medium.render(self.text.upper(), 1, (15, 41, 61))
        text_rect = text.get_rect(midtop=(self.box.rect[0] + self.box.rect[2]//2, self.box.rect[1]+15))
        screen.blit(text, text_rect)
        self.image_box.render(screen)
        self.cancel_button.render(screen)

    def set_state(self, state):
        self.state = state

        if state == self.FAILED:
            self.text = 'Failed to connect'
            self.image_box.set_image(self.failed_image)
        elif state == self.SEARCHING:
            self.text = 'Searching for a match...'
            self.image_box.set_image(self.searching_image)
        elif state == self.FOUND:
            self.text = 'Match found!'
            self.image_box.set_image(self.found_image)
        elif state == self.IDLE:
            self.text = ''
            self.image_box.set_image(None)

    def is_active(self):
        return (self.state != self.IDLE)