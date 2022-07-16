from data.components.gui.button import *
from data.components.font import *
from config import *
import config

class MatchResultBox():

    VICTORY = 0
    DEFEAT  = 1
    DRAW    = 2
    IDLE    = 3

    victory_image = pygame.image.load('data/resources/img/general/match_result_victory.jpg')
    defeat_image  = pygame.image.load('data/resources/img/general/match_result_defeat.jpg')
    draw_image    = pygame.image.load('data/resources/img/general/match_result_draw.jpg')

    def __init__(self):
        self.box = Button([WIDTH//2 - 300, HEIGHT//2-150, 400, 300], border=2)
        self.cancel_button = Button([WIDTH//2 - 200, HEIGHT//2+90, 200, 40], text='RETURN TO MENU', border=1)
        self.image_box = Button([WIDTH//2 - 250, HEIGHT//2-100, 300, 170], border=1)
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

        if state == self.VICTORY:
            self.text = 'YOU WIN!'
            self.image_box.set_image(self.victory_image)
        elif state == self.DEFEAT:
            self.text = 'YOU LOSE!'
            self.image_box.set_image(self.defeat_image)
        elif state == self.DRAW:
            self.text = 'IT\'S A DRAW!'
            self.image_box.set_image(self.draw_image)
        elif state == self.IDLE:
            self.text = ''
            self.image_box.set_image(None)

    def is_active(self):
        return (self.state != self.IDLE)