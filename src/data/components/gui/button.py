from data.components.font import *
import numpy as np
import pygame
import time

class Button():

    max_time_for_double_click = 0.15

    def __init__(self, rect, border=0, text=None, image=None, only_text = False,
                 font=Font.font_medium, image_alpha=None, color=(255,255,255), border_color=(0,0,0),
                 velocity=60, text_color=(0,0,0), target_pos=None, enabled=True):
        self.rect = rect
        self.original_pos = self.rect[0:2] # First position
        self.target_pos = target_pos # For animations
        self.velocity = velocity

        self.border = border
        self.text = text
        self.text_color = text_color
        self.set_image(image)
        self.only_text = only_text
        self.font = font
        self.image_alpha = image_alpha
        self.color = color
        self.border_color = border_color

        self.last_time_clicked = time.time()
        self.was_double_clicked = False

        self.enabled = enabled

    def render(self, screen):
        if not self.enabled:
            return

        # Moving to target pos
        if not self.target_pos is None:
            if self.target_pos != self.rect[0:2]:
                delta = np.array(self.target_pos) - np.array(self.rect[0:2])
                delta_norm = np.linalg.norm(delta)
                if delta_norm <= self.velocity:
                    self.rect = [self.target_pos[0], self.target_pos[1], self.rect[2], self.rect[3]]
                    self.target_pos = None
                else:
                    delta = delta*self.velocity/np.linalg.norm(delta)
                    self.rect = [self.rect[0]+delta[0], self.rect[1]+delta[1], self.rect[2], self.rect[3]]

        if not self.only_text:
            if self.border > 0:
                b = self.border
                r = self.rect
                border_rect = [r[0]-b, r[1]-b, b, r[3]+2*b]
                pygame.draw.rect(screen, self.border_color, border_rect)
                border_rect = [r[0]-b, r[1]-b, r[2]+2*b, b]
                pygame.draw.rect(screen, self.border_color, border_rect)
                border_rect = [r[0]+r[2], r[1]-b, b, r[3]+2*b]
                pygame.draw.rect(screen, self.border_color, border_rect)
                border_rect = [r[0]-b, r[1]+r[3], r[2]+2*b, b]
                pygame.draw.rect(screen, self.border_color, border_rect)

            if not self.image is None:
                image_to_render = self.image

                if not self.image_alpha is None:
                    image_to_render = image_to_render.copy().convert(24)
                    image_to_render.set_alpha(self.image_alpha)
                    #image_to_render.fill((255, 255, 255, self.image_alpha), None, pygame.BLEND_RGBA_MULT)

                screen.blit(image_to_render, (self.rect[0], self.rect[1]))
            else:
                pygame.draw.rect(screen, self.color, self.rect)

        # Rendering the text
        if not self.text is None:
            text = self.font.render(self.text, 1, self.text_color)
            text_rect = text.get_rect(center=(self.rect[0] + self.rect[2]//2, self.rect[1]+self.rect[3]//2))
            screen.blit(text, text_rect)

    def set_image(self, image):
        if image is None:
            self.image = None
        else:
            self.image = pygame.transform.smoothscale(image, (self.rect[2], self.rect[3]))

    def collide(self, mouse_pos):
        if self.rect[0] <= mouse_pos[0] <= self.rect[0] + self.rect[2] and \
           self.rect[1] <= mouse_pos[1] <= self.rect[1] + self.rect[3]:
            return True
        else:
            return False

    def click(self, mouse_pos):
        self.was_double_clicked = False
        if self.collide(mouse_pos):
            current_time = time.time()
            delta_time = current_time - self.last_time_clicked
            self.last_time_clicked = current_time

            if delta_time <= self.max_time_for_double_click:
                self.double_click(mouse_pos)

    def double_click(self, mouse_pos):
        self.was_double_clicked = True
        pass

    def unclick(self, pos):
        pass
