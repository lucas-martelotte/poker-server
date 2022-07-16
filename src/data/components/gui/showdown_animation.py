from data.components.gui.card_button import CardButton
from data.utils.auxiliary import linear_animation
from data.components.mixer import Mixer
from config import FPS, HEIGHT

class ShowdownAnimation():
    def __init__(self, player_card, opponent_card, duration=3):
        self.player_card   = player_card
        self.opponent_card = opponent_card


        self.original_player_card_rect   = [40,  125, 240, 350]
        self.original_opponent_card_rect = [320, 125, 240, 350]
        self.player_card_button   = CardButton(self.original_player_card_rect, None, 'back')
        self.opponent_card_button = CardButton(self.original_opponent_card_rect, None, 'back')

        self.total_frames    = duration * FPS
        self.start_revealing = self.total_frames//3
        self.end_revealing   = (2*self.total_frames)//3
        self.mid_revealing   = (self.start_revealing + self.end_revealing)//2
        self.current_frame   = 0

    def render(self, screen):

        if self.current_frame <= self.start_revealing:
            pass
        elif self.current_frame <= self.mid_revealing:
            rect_x = int(linear_animation(self.current_frame, self.start_revealing, 40, self.mid_revealing, 160))
            rect_w = int(linear_animation(self.current_frame, self.start_revealing, 240, self.mid_revealing, 1))
            self.player_card_button.rect = [rect_x, 125, rect_w, 350]
            self.player_card_button.set_card('back')

            rect_x = int(linear_animation(self.current_frame, self.start_revealing, 320, self.mid_revealing, 440))
            rect_w = int(linear_animation(self.current_frame, self.start_revealing, 240, self.mid_revealing, 1))
            self.opponent_card_button.rect = [rect_x, 125, rect_w, 350]
            self.opponent_card_button.set_card('back')
        elif self.current_frame <= self.end_revealing:
            rect_x = int(linear_animation(self.current_frame, self.mid_revealing, 160, self.end_revealing, 40))
            rect_w = int(linear_animation(self.current_frame, self.mid_revealing, 1, self.end_revealing, 240))
            self.player_card_button.rect = [rect_x, 125, rect_w, 350]
            self.player_card_button.set_card(self.player_card)

            rect_x = int(linear_animation(self.current_frame, self.mid_revealing, 440, self.end_revealing, 320))
            rect_w = int(linear_animation(self.current_frame, self.mid_revealing, 1, self.end_revealing, 240))
            self.opponent_card_button.rect = [rect_x, 125, rect_w, 350]
            self.opponent_card_button.set_card(self.opponent_card)
        else:
            pass

        if self.current_frame == self.mid_revealing:
            Mixer.play(Mixer.CARD_REVEAL_SOUND, volume=0.03)

        self.player_card_button.render(screen)
        self.opponent_card_button.render(screen)

        if self.current_frame < self.total_frames:
            self.current_frame += 1


    def completed(self):
        return (self.current_frame == self.total_frames)