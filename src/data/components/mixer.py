from config import NUMBER_OF_CHANNELS
import pygame

class Mixer():

    base_path = 'data/resources/sound/'

    # The number indicate the sound channel it
    # will be played in. Channel 0 is reserved for music.
    CLICK_SOUND       = 1
    ZAWA_SOUND        = 2
    CARD_REVEAL_SOUND = 3
    NEW_PHASE_SOUND   = 4

    # Music enum
    MAN_RACETRACK_MUSIC = base_path + 'music/man_racetrack.mp3'
    PHOENIX_MUSIC       = base_path + 'music/phoenix.mp3'
    WHITE_HEAT_MUSIC    = base_path + 'music/white_heat.mp3'

    sound_to_file_dict = {}

    def initialize():
        Mixer.sound_to_file_dict = {
            Mixer.CLICK_SOUND         : pygame.mixer.Sound(Mixer.base_path + 'click.ogg'),
            Mixer.ZAWA_SOUND          : pygame.mixer.Sound(Mixer.base_path + 'zawa.flac'),
            Mixer.CARD_REVEAL_SOUND   : pygame.mixer.Sound(Mixer.base_path + 'Magic3.ogg'),
            Mixer.NEW_PHASE_SOUND     : pygame.mixer.Sound(Mixer.base_path + 'Sword5.ogg')
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
        if not music in [Mixer.MAN_RACETRACK_MUSIC, Mixer.PHOENIX_MUSIC, Mixer.WHITE_HEAT_MUSIC]:
            return
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(loops=-1)

    def __init__(self):
        pass
