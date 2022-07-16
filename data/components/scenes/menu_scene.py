from data.components.gui.match_making_box import MatchMakingBox
from data.components.gui.button import Button
from data.components.scenes.scene import Scene
from data.components.mixer import Mixer
from data.network.network import Network
from config import WIDTH, HEIGHT
import pygame

class MenuScene(Scene):

    background = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/general/menu_bg.png"), (WIDTH, HEIGHT))

    def __init__(self, name):
        super().__init__(name)

        self.quick_play_button = Button([WIDTH-190, 35, 160, 60], border=2, text='QUICK PLAY')
        self.settings_button   = Button([WIDTH-190, 115, 160, 60], border=2, text='SETTINGS')
        self.credits_button    = Button([WIDTH-190, 195, 160, 60], border=2, text='CREDITS')
        self.quit_button       = Button([WIDTH-190, 275, 160, 60], border=2, text='QUIT')
        self.version_text      = Button([WIDTH-150, HEIGHT-60, 160, 60], border=2, only_text=True, text='Version 0.0.1', text_color=(255,255,255))

        self.gui_list.extend([self.quick_play_button,
                              self.settings_button,
                              self.credits_button,
                              self.quit_button,
                              self.version_text])

        # Stuff to handle networking
        self.match_making_box = MatchMakingBox()


    def render_contents(self, screen):
        screen.blit(MenuScene.background, (0,0))

        # Drawing the match making box
        if self.match_making_box.is_active():
            self.match_making_box.render(screen)


    def click(self, mouse_pos, event):

        Mixer.play(Mixer.CLICK_SOUND)

        if event.button != 1:
            return

        # Handling Quit
        if self.quit_button.collide(mouse_pos):
            exit()

        # Here we handle the state where a match is being searched/failed
        # In this case, the only component the player can interact is
        # the match_making_box
        if self.match_making_box.state != MatchMakingBox.IDLE:
            if self.match_making_box.cancel_button.collide(mouse_pos):
                self.match_making_box.set_state(MatchMakingBox.IDLE)
                self.control.disconnect()
            return

        # Bellow is the overall treatment for the rest of the components
        # Here, the player is not seraching for a match, therefore he can
        # interact with everything except the match_making_box
        if self.quick_play_button.collide(mouse_pos):
            self.match_making_box.set_state(MatchMakingBox.SEARCHING)
            self.render(self.control.screen)
            # Trying to connect to a quick_play match
            if not self.control.connect():
                # If it fails, we'll change the match making box to the FAILED state
                self.match_making_box.set_state(MatchMakingBox.FAILED)
            else:
                # If it succeeds, we'll send a request to enter the quick play queue to the server
                data_type, data = self.control.send(Network.ENTER_MATCH_QUEUE, timeout=3)
                if data_type != Network.SUCCESS:
                    self.match_making_box.set_state(MatchMakingBox.FAILED)


    def handle_server_data(self, data_type, data=None):
        # We'll do a switch case on the possible server messages
        # In the case a match is aborted, we'll cancel the wait
        if data_type == Network.MATCH_ABORTED:
            self.match_making_box.set_state(MatchMakingBox.FAILED)
        # In the case a match is found, we'll send the game info and change
        # the scene when the match starts
        elif data_type == Network.MATCH_FOUND:
            print('Match Found!')
            self.match_making_box.set_state(MatchMakingBox.FOUND)
            self.render(self.control.screen)

            if not data_type or data_type == Network.FAILED:
                # If we failed to send the game data, we'll cancel the match
                self.match_making_box.set_state(MatchMakingBox.FAILED)
                return

            print('Success in sending the quick match data.')
            # Now we'll wait for the game object and ID
            try:
                data_type, local_game = self.control.recv(timeout=5)
                if data_type != Network.SEND_GAME:
                    print(f'Error. Unexpected data_type in handle_server_msg. Expected {Network.data_type_to_str(Network.SEND_GAME)}, got {Network.data_type_to_str(data_type)}.')
            except:
                print('Quick Match timed out.')
                self.match_making_box.set_state(MatchMakingBox.FAILED)
                return

            print(f'Game info received. Player ID: {local_game.get_player_id()}. Game Object: {local_game}.')
            print(f'Switching to the Game Scene.')

            # Switching to the game scene
            self.match_making_box.set_state(MatchMakingBox.IDLE)
            self.control.scene_dict['GAME_SCENE'].set_game_info(local_game)
            self.control.active_scene = 'GAME_SCENE'

