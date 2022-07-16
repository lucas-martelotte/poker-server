from config import NUMBER_OF_CHANNELS
import pygame

class Mixer():

    base_path = 'data/resources/sound/'

    # The number indicate the sound channel it
    # will be played in. Channel 0 is reserved for music.
    CLICK_SOUND = 1
    ZAWA_SOUND  = 2

    sound_to_file_dict = {}

    def initialize():
        Mixer.sound_to_file_dict = {
            Mixer.CLICK_SOUND : pygame.mixer.Sound(Mixer.base_path + 'click.ogg'),
            Mixer.ZAWA_SOUND  : pygame.mixer.Sound(Mixer.base_path + 'zawa.flac')
        }

    def sound_to_file(sound):
        if not sound in Mixer.sound_to_file_dict:
            return None
        return Mixer.sound_to_file_dict[sound]

    def play(sound, volume=0.01):
        if sound < 1 or sound >= NUMBER_OF_CHANNELS:
            return
        sound_file = Mixer.sound_to_file(sound)
        if not sound_file:
            return
        pygame.mixer.Channel(sound).set_volume(volume)
        pygame.mixer.Channel(sound).play(sound_file)

    def play_music(music, volume=0.01):
        music_file = Mixer.sound_to_file(music)
        if not sound_file:
            return
        pygame.mixer.Channel(0).set_volume(volume)
        pygame.mixer.Channel(0).play(music_file)

    def __init__(self):
        pass
