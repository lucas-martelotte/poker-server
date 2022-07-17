from data.components.mixer import Mixer
from data.components.font import Font
from config import FPS, WIDTH, HEIGHT
import pygame

class MessageAnimation():
    def __init__(self, text, duration=1):
        self.total_frames  = duration * FPS
        self.transition_percent = 10

        # At what frame the message will arrise fully in the screen
        self.end_start_animation = (self.transition_percent*self.total_frames)//100
        # At what frame the message will start leaving the screen
        self.start_end_animation = self.total_frames - self.end_start_animation

        self.font = Font.font_big
        self.total_width = 595
        self.rect_height = 40
        self.rect_border = 5

        self.current_frame = 0
        self.text = text

    def render(self, screen):

        if self.current_frame == 0:
            Mixer.play(Mixer.NEW_PHASE_SOUND)

        if self.current_frame <= self.end_start_animation:
            rect_width = (self.current_frame*self.total_width)//self.end_start_animation
            start_down_rect = self.total_width - rect_width
            start_up_rect   = 0
        elif self.current_frame > self.end_start_animation and \
             self.current_frame < self.start_end_animation:
            rect_width = self.total_width
            start_down_rect = 0
            start_up_rect = 0
        else:
            rect_width = ((self.total_frames-self.current_frame)*self.total_width)//self.end_start_animation
            start_down_rect = 0
            start_up_rect   = self.total_width - rect_width

        pygame.draw.rect(screen, (255,255,255), [start_up_rect, HEIGHT//2-self.rect_height-self.rect_border, rect_width, self.rect_border])
        pygame.draw.rect(screen, (0,0,0), [start_up_rect, HEIGHT//2-self.rect_height, rect_width, self.rect_height])
        pygame.draw.rect(screen, (255,255,255), [start_down_rect, HEIGHT//2+self.rect_height, rect_width, self.rect_border])
        pygame.draw.rect(screen, (0,0,0), [start_down_rect, HEIGHT//2, rect_width, self.rect_height])

        # Rendering the Text
        if self.current_frame >= self.end_start_animation:
            text = self.font.render(self.text, 1, (255,255,255))
            text_rect = text.get_rect(center=(self.total_width//2, HEIGHT//2))
            screen.blit(text, text_rect)

        if self.current_frame < self.total_frames:
            self.current_frame += 1

    def completed(self):
        return (self.current_frame == self.total_frames)