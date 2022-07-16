from data.components.gui.match_result_box import MatchResultBox
from data.components.gui.zawa_generator import ZawaGenerator
from data.components.gui.card_button import CardButton
from data.components.gui.button import Button
from data.components.scenes.scene import *
from data.network.network import Network
from data.components.game import Game
from data.components.font import Font
from data.utils.auxiliary import *
from config import *
import pygame

class GameScene(Scene):

    backgrounds = [pygame.transform.smoothscale(pygame.image.load(f'./data/resources/img/sprites/match_bg_{i}.png'), (WIDTH, HEIGHT)) for i in range(1,6,1)]

    sidebar = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/general/sidebar.png"), (WIDTH, HEIGHT))

    kaiji_sprite  = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/kaiji.png"), (WIDTH, HEIGHT))
    kazuya_sprite = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/kazuya.png"), (WIDTH, HEIGHT))

    kaiji_table   = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/table_kaiji.png"), (WIDTH, HEIGHT))
    kazuya_table  = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/table_kazuya.png"), (WIDTH, HEIGHT))

    kaiji_top = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/kaiji_top.png"), (WIDTH, HEIGHT))
    kaiji_bottom = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/kaiji_bottom.png"), (WIDTH, HEIGHT))
    kazuya_top = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/kazuya_top.png"), (WIDTH, HEIGHT))
    kazuya_bottom = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/kazuya_bottom.png"), (WIDTH, HEIGHT))

    silver_statue = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/silver_statue.png"), (155, 163))
    red_statue = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/red_statue.png"), (155, 163))
    red_statue_disabled = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/red_statue_disabled.png"), (155, 163))

    up_img = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/up.png"), (48, 42))
    down_img = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/down.png"), (48, 42))

    bet_img = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/bet.png"), (176, 107))
    fold_img = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/fold.png"), (115, 65))

    KAIJI_INDEX  = 1
    KAZUYA_INDEX = 0

    def __init__(self, name):
        super().__init__(name)
        self.card_buttons = []
        self.played_card_button = None

        self.selected_card = None

        self.zawa_generator = None
        self.local_game = None

        self.current_bet = 0
        self.current_red_bet = False

        self.match_result_box = MatchResultBox()

    def set_game_info(self, local_game):
        print(local_game)
        self.local_game = local_game

        if (self.local_game.state == Game.PLAYER_0_WIN and self.local_game.player_id == 0) or \
           (self.local_game.state == Game.PLAYER_1_WIN and self.local_game.player_id == 1):
            self.match_result_box.set_state(MatchResultBox.VICTORY)
        elif (self.local_game.state == Game.PLAYER_1_WIN and self.local_game.player_id == 0) or \
             (self.local_game.state == Game.PLAYER_0_WIN and self.local_game.player_id == 1):
            self.match_result_box.set_state(MatchResultBox.DEFEAT)
        elif self.local_game.state == Game.DRAW:
            self.match_result_box.set_state(MatchResultBox.DRAW)

        start_x = 200 if (self.local_game.player_id == GameScene.KAIJI_INDEX) else 10
        self.card_buttons = [
            CardButton([start_x, 420, 170,247], 0, local_game.hand[0]),
            CardButton([start_x + 190, 420, 170,247], 1, local_game.hand[1])
        ]

        if local_game.card_played is not None:
            self.played_card_button = CardButton([512, 20, 68, 100], None, local_game.card_played)
        else:
            self.played_card_button = None

        self.zawa_generator = ZawaGenerator([0,0,600,600])

        self.silver_statue_button = Button([30, 260, 155, 163], image=GameScene.silver_statue)
        self.red_statue_button = Button([215, 260, 155, 163], image=GameScene.red_statue_disabled)
        self.bet_button = Button([400, 290, 176, 107], image=GameScene.bet_img)
        self.fold_button = Button([461, 427, 115, 65], image=GameScene.fold_img)
        self.up_button = Button([150, 260, 48, 42], image=GameScene.up_img)
        self.down_button = Button([150, 340, 48, 42], image=GameScene.down_img)
        self.current_bet_button = Button([150, 307, 48, 28], border=1, text='0')


    def render_contents(self, screen):

        screen.fill((255,255,255))
        if not self.local_game:
            return

        #==================#
        #=== BACKGROUND ===#
        #==================#

        statues = self.local_game.stored_statues
        background_index = int(4*(statues[self.local_game.player_id]/(statues[0] + statues[1])))
        if background_index <= 4 and background_index >= 0:
            screen.blit(GameScene.backgrounds[background_index], (0,0))
        else:
            print(f'ERROR: Background index out of bounds ({background_index}).')

        #=========================#
        #=== UI and CHARACTERS ===#
        #=========================#

        screen.blit(GameScene.sidebar, (0,0))

        if self.local_game.player_id == GameScene.KAZUYA_INDEX:
            # Kazuya
            screen.blit(GameScene.kaiji_sprite, (0,0))
            screen.blit(GameScene.kazuya_table, (0,0))
            screen.blit(GameScene.kazuya_bottom, (0,0))
            screen.blit(GameScene.kaiji_top, (0,0))
        elif self.local_game.player_id == GameScene.KAIJI_INDEX:
            # Kaiji
            screen.blit(GameScene.kazuya_sprite, (0,0))
            screen.blit(GameScene.kaiji_table, (0,0))
            screen.blit(GameScene.kaiji_bottom, (0,0))
            screen.blit(GameScene.kazuya_top, (0,0))

        if (self.local_game.state == Game.PLAYER_1_BET and self.local_game.player_id == 1) or \
           (self.local_game.state == Game.PLAYER_0_BET and self.local_game.player_id == 0):
            self.silver_statue_button.render(screen)
            self.red_statue_button.render(screen)
            self.bet_button.render(screen)
            self.fold_button.render(screen)
            self.up_button.render(screen)
            self.down_button.render(screen)
            self.current_bet_button.render(screen)


        #if self.selected_card is not None:
        #    Button([250,250,100,100], only_text=True, text_color=(255,255,255), font=Font.font_big,
        #        text=f'Play {self.local_game.hand[self.selected_card]}. Confirm?').render(screen)

        #===============#
        #==== CARDS ====#
        #===============#

        if self.played_card_button:
            self.played_card_button.render(screen)

        if self.local_game.state == Game.PLAY_CARDS and \
           self.local_game.card_played is None:
            for card_button in self.card_buttons:
                card_button.render(screen)

        #==============#
        #==== ZAWA ====#
        #==============#

        self.zawa_generator.render(screen)


        #====================#
        #= MATCH RESULT BOX =#
        #====================#

        if self.match_result_box.is_active():
            self.match_result_box.render(screen)

        #===============#
        #=== LOGGING ===#
        #===============#

        Button([10,0,200,20], only_text=True, text_color=(255,255,255),
               text=f'Stored: {self.local_game.stored_statues}').render(screen)
        Button([10,20,200,20], only_text=True, text_color=(255,255,255),
               text=f'Betted: {self.local_game.betted_statues}, {self.local_game.red_betted_statues}').render(screen)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for card_button in self.card_buttons:
            if card_button.collide(mouse_pos):
                card_button.target_pos = [card_button.original_pos[0],
                                          card_button.original_pos[1] -80]
            else:
                card_button.target_pos = card_button.original_pos

        if self.zawa_generator:
            self.zawa_generator.generate_zawa()


    def click(self, mouse_pos, event):
        if event.button != 1:
            # not left click
            return
        if not self.local_game:
            # No game running
            return

        if self.local_game.state == Game.PLAY_CARDS:
            if self.local_game.card_played is None:
                card_collided = False

                for card_button_index, card_button in enumerate(self.card_buttons):
                    if card_button.collide(mouse_pos):
                        if card_button_index != self.selected_card:
                            self.selected_card = card_button_index
                            card_button.border = 4
                            card_button.border_color = (0,100,255)

                        elif card_button_index == self.selected_card:
                            data_type, data = self.control.send(Network.PLAY_CARD,
                                                    data=self.local_game.hand[self.selected_card],
                                                    timeout=0.1)
                            if data_type == Network.SEND_GAME:
                                self.set_game_info(data)

                        card_collided = True
                        break

                if not card_collided:
                    self.selected_card = None

                for card_button_index, card_button in enumerate(self.card_buttons):
                    if self.selected_card != card_button_index:
                        card_button.border = 1
                        card_button.border_color = (0,0,0)

        elif ((self.local_game.state == Game.PLAYER_0_BET) and (self.local_game.player_id == 0)) or\
             ((self.local_game.state == Game.PLAYER_1_BET) and (self.local_game.player_id == 1)):
            # You need to bet
            total_bet = self.current_bet + self.local_game.betted_statues[self.local_game.player_id]

            if self.up_button.collide(mouse_pos):
                if total_bet < self.local_game.stored_statues[self.local_game.player_id]:
                    self.current_bet += 1
                    self.current_bet_button.text = str(self.current_bet)
            if self.down_button.collide(mouse_pos):
                if self.current_bet > 0:
                    self.current_bet -= 1
                    self.current_bet_button.text = str(self.current_bet)
            if self.red_statue_button.collide(mouse_pos):
                self.current_red_bet = not self.current_red_bet
                if self.current_red_bet:
                    self.red_statue_button.set_image(GameScene.red_statue)
                else:
                    self.red_statue_button.set_image(GameScene.red_statue_disabled)
            if self.bet_button.collide(mouse_pos):
                data_type, data = self.control.send(Network.PLACE_BET,
                                                    data=(self.current_bet, self.current_red_bet),
                                                    timeout=0.1)
                if data_type == Network.SEND_GAME:
                    self.set_game_info(data)

                self.current_bet = 0
                self.current_red_bet = False

            if self.fold_button.collide(mouse_pos):
                data_type, data = self.control.send(Network.FOLD, timeout=0.1)
                if data_type == Network.SEND_GAME:
                    self.set_game_info(data)

                self.current_bet = 0
                self.current_red_bet = False

        elif (self.local_game.state == Game.PLAYER_0_BET and self.local_game.player_id == 1) or\
             (self.local_game.state == Game.PLAYER_1_BET and self.local_game.player_id == 0):
            # Opponent is betting
            pass
        elif self.local_game.state in [Game.PLAYER_0_WIN, Game.PLAYER_1_WIN, Game.DRAW]:
            # Game is over
            if self.match_result_box.cancel_button.collide(mouse_pos):
                self.return_to_menu()


    def handle_server_data(self, data_type, data=None):
        if data_type == Network.SEND_GAME:
            self.set_game_info(data)

    def return_to_menu(self):
        self.control.disconnect()
        self.game = None
        self.match_result_box.set_state(MatchResultBox.IDLE)
        self.control.set_active_scene('MENU_SCENE')