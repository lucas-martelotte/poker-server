from data.components.scenes.menu_scene import MenuScene
from data.components.scenes.game_scene import GameScene
from data.components.control import Control
from data.components.mixer import Mixer
from config import WIDTH, HEIGHT, NUMBER_OF_CHANNELS
import pygame
import os

#====================#
#=== PYGAME SETUP ===#
#====================#

pygame.init()
pygame.font.init()

pygame.mixer.init()
pygame.mixer.set_num_channels(NUMBER_OF_CHANNELS)
Mixer.initialize()

pygame.display.set_caption("One Poker Online")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#====================#
#======= MAIN =======#
#====================#

if __name__=='__main__':
    control = Control(screen, clock)
    control.add_scene(GameScene('GAME_SCENE'))
    control.add_scene(MenuScene('MENU_SCENE'))
    control.set_active_scene('MENU_SCENE')
    control.main_loop()