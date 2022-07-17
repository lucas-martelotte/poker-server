from data.components.gui.showdown_animation import ShowdownAnimation
from data.components.gui.message_animation import MessageAnimation
from data.components.gui.match_result_box import MatchResultBox
from data.components.gui.zawa_generator import ZawaGenerator
from data.components.gui.card_button import CardButton
from data.components.gui.button import Button
from data.components.scenes.scene import *
from data.network.network import Network
from data.components.mixer import Mixer
from data.components.game import Game
from data.components.font import Font
from data.utils.auxiliary import *
from config import *
import pygame

class GameScene(Scene):

    backgrounds = [pygame.transform.smoothscale(pygame.image.load(f'./data/resources/img/sprites/match_bg_{i}.png'), (WIDTH, HEIGHT)) for i in range(1,6,1)]

    sidebar = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/general/sidebar.png"), (WIDTH, HEIGHT))
    stored_statues_marker = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/general/stored_statues_marker.png"), (WIDTH, HEIGHT))

    playing_phase_label = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/general/playing_phase_label.png"), (WIDTH, HEIGHT))
    betting_phase_label = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/general/betting_phase_label.png"), (WIDTH, HEIGHT))
    defeat_label  = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/general/defeat_label.png"), (WIDTH, HEIGHT))
    victory_label = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/general/victory_label.png"), (WIDTH, HEIGHT))

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

    up_up_img = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/up_up.png"), (87, 47))
    up_down_img = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/up_down.png"), (87, 47))
    down_down_img = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/down_down.png"), (87, 47))

    kaiji_bet_avatar = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/kaiji_bet_avatar.png"), (80, 80))
    kazuya_bet_avatar = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/kazuya_bet_avatar.png"), (80, 80))

    mini_silver_statue = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/mini_silver_statue.png"), (40, 80))
    mini_red_statue = pygame.transform.smoothscale(pygame.image.load("./data/resources/img/sprites/mini_red_statue.png"), (40, 80))

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

        self.showdown_animation = None
        self.message_animation = None
        self.hand_indicator_button = None
        self.zawa_generator = ZawaGenerator([0,0,600,600])
        self.silver_statue_button = Button([30, 260, 155, 163], image=GameScene.silver_statue)
        self.red_statue_button = Button([215, 260, 155, 163], image=GameScene.red_statue_disabled)
        self.bet_button = Button([400, 290, 176, 107], image=GameScene.bet_img)
        self.fold_button = Button([461, 427, 115, 65], image=GameScene.fold_img)
        self.up_button = Button([150, 260, 48, 42], image=GameScene.up_img)
        self.down_button = Button([150, 340, 48, 42], image=GameScene.down_img)
        self.current_bet_button = Button([150, 307, 48, 28], border=1, text='0')

        self.current_music = None

    def set_game_info(self, local_game):

        if self.current_music is None:
            # In this case, the game just started and we'll play the initial music
            self.current_music = Mixer.MAN_RACETRACK_MUSIC
            Mixer.play_music(self.current_music)

        print(local_game)
        prev_local_game = self.local_game
        self.local_game = local_game

        # Showdown animation
        transition_message = self.get_phase_text(prev_local_game, self.local_game)
        if transition_message == 'Showdown!':
            round_history = self.local_game.round_history
            player_card = round_history[len(round_history)-1][self.local_game.player_id+1]
            opponent_card = round_history[len(round_history)-1][(self.local_game.player_id+1)%2+1]
            self.showdown_animation = ShowdownAnimation(player_card, opponent_card)

        if (self.local_game.state == Game.PLAYER_0_WIN and self.local_game.player_id == 0) or \
           (self.local_game.state == Game.PLAYER_1_WIN and self.local_game.player_id == 1):
            self.match_result_box.set_state(MatchResultBox.VICTORY)
        elif (self.local_game.state == Game.PLAYER_1_WIN and self.local_game.player_id == 0) or \
             (self.local_game.state == Game.PLAYER_0_WIN and self.local_game.player_id == 1):
            self.match_result_box.set_state(MatchResultBox.DEFEAT)
        elif self.local_game.state == Game.DRAW:
            self.match_result_box.set_state(MatchResultBox.DRAW)
        else:
            # If the game is not over, we'll print a phase transition
            if transition_message != '':
                self.message_animation = MessageAnimation(transition_message)

        start_x = 200 if (self.local_game.player_id == GameScene.KAIJI_INDEX) else 10
        self.card_buttons = [
            CardButton([start_x, 420, 170,247], 0, local_game.hand[0]),
            CardButton([start_x + 190, 420, 170,247], 1, local_game.hand[1])
        ]

        if local_game.card_played is not None:
            self.played_card_button = CardButton([512, 20, 68, 100], None, local_game.card_played)
        else:
            self.played_card_button = None

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

        # Getting the opponent hand indicator image
        current_img = None
        if self.local_game.opponent_high_cards == [True, True]:
            current_img = GameScene.up_up_img
        elif self.local_game.opponent_high_cards in [[True, False], [False, True]]:
            current_img = GameScene.up_down_img
        elif self.local_game.opponent_high_cards == [False, False]:
            current_img = GameScene.down_down_img

        if self.local_game.state in [Game.PLAYER_0_BET, Game.PLAYER_1_BET]:
            screen.blit(GameScene.betting_phase_label, (0,0))
        elif self.local_game.state == Game.PLAY_CARDS:
            screen.blit(GameScene.playing_phase_label, (0,0))
        elif (self.local_game.state == Game.PLAYER_0_WIN and self.local_game.player_id == 0) or \
             (self.local_game.state == Game.PLAYER_1_WIN and self.local_game.player_id == 1):
            screen.blit(GameScene.victory_label, (0,0))
        elif (self.local_game.state == Game.PLAYER_0_WIN and self.local_game.player_id == 1) or \
             (self.local_game.state == Game.PLAYER_1_WIN and self.local_game.player_id == 0):
            screen.blit(GameScene.defeat_label, (0,0))

        screen.blit(GameScene.stored_statues_marker, (0,0))

        Button([674, 170, 20, 20], only_text=True, text_color=(255,255,255), font=Font.font_medium_plus,
               text=f'{self.local_game.stored_statues[(self.local_game.player_id+1)%2]}').render(screen)

        Button([700, 410, 20, 20], only_text=True, text_color=(255,255,255), font=Font.font_medium_plus,
               text=f'{self.local_game.stored_statues[self.local_game.player_id]}').render(screen)


        if self.local_game.player_id == GameScene.KAZUYA_INDEX:
            # Kazuya
            screen.blit(GameScene.kaiji_sprite, (0,0))
            screen.blit(GameScene.kazuya_table, (0,0))
            screen.blit(GameScene.kazuya_bottom, (0,0))
            screen.blit(GameScene.kaiji_top, (0,0))
            screen.blit(current_img, (225, 330))

            if self.local_game.state in [Game.PLAYER_0_BET, Game.PLAYER_1_BET]:
                screen.blit(GameScene.kazuya_bet_avatar, (10,10))
                screen.blit(GameScene.kaiji_bet_avatar, (10,100))

        elif self.local_game.player_id == GameScene.KAIJI_INDEX:
            # Kaiji
            screen.blit(GameScene.kazuya_sprite, (0,0))
            screen.blit(GameScene.kaiji_table, (0,0))
            screen.blit(GameScene.kaiji_bottom, (0,0))
            screen.blit(GameScene.kazuya_top, (0,0))
            screen.blit(current_img, (275, 330))

            if self.local_game.state in [Game.PLAYER_0_BET, Game.PLAYER_1_BET]:
                screen.blit(GameScene.kaiji_bet_avatar, (10,10))
                screen.blit(GameScene.kazuya_bet_avatar, (10,100))

        # Printing the betted statues
        if self.local_game.state in [Game.PLAYER_0_BET, Game.PLAYER_1_BET]:
            betted_red = self.local_game.red_betted_statues[self.local_game.player_id]
            total_amount = self.local_game.betted_statues[self.local_game.player_id]
            total_amount += 1 if betted_red else 0

            distance = min(15, 120//total_amount)
            for i in range(total_amount):
                if i == total_amount-1 and betted_red:
                    screen.blit(GameScene.mini_red_statue, (90+i*distance, 10))
                    continue
                screen.blit(GameScene.mini_silver_statue, (90+i*distance, 10))

            betted_red = self.local_game.red_betted_statues[(self.local_game.player_id+1)%2]
            total_amount = self.local_game.betted_statues[(self.local_game.player_id+1)%2]
            total_amount += 1 if betted_red else 0

            distance = min(15, 120//total_amount)
            for i in range(total_amount):
                if i == total_amount-1 and betted_red:
                    screen.blit(GameScene.mini_red_statue, (90+i*distance, 100))
                    continue
                screen.blit(GameScene.mini_silver_statue, (90+i*distance, 100))

        # Printing the betting buttons
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

        #=====================#
        #= MESSAGE ANIMATION =#
        #=====================#

        if self.message_animation is not None:
            self.message_animation.render(screen)
            if self.message_animation.completed():
                self.message_animation = None

        # Printing a separator line between the sidebar and the game area on the left
        pygame.draw.rect(screen, (0,0,0), [592, 0, 3, 600])

        #====================#
        #= MATCH RESULT BOX =#
        #====================#

        if self.match_result_box.is_active():
            self.match_result_box.render(screen)

        #====================#
        #===== SHOWDOWN =====#
        #====================#
        if self.showdown_animation is not None:
            pygame.draw.rect(screen, (0,0,0), [0,0,800,600])
            self.showdown_animation.render(screen)
            if self.showdown_animation.completed():
                self.showdown_animation = None

                # Here, we're goint to update the music
                statues = self.local_game.stored_statues[self.local_game.player_id]
                statue_percentage = statues/sum(self.local_game.stored_statues)

                if statue_percentage <= 0.2:
                    next_music = Mixer.PHOENIX_MUSIC
                elif statue_percentage <= 0.8:
                    next_music = Mixer.MAN_RACETRACK_MUSIC
                else:
                    next_music = Mixer.WHITE_HEAT_MUSIC

                if next_music != self.current_music:
                    self.current_music = next_music
                    Mixer.play_music(next_music)

        #===============#
        #=== LOGGING ===#
        #===============#

        #Button([10,0,200,20], only_text=True, text_color=(255,255,255),
        #       text=f'Stored: {self.local_game.stored_statues}').render(screen)
        #Button([10,20,200,20], only_text=True, text_color=(255,255,255),
        #       text=f'Betted: {self.local_game.betted_statues}, {self.local_game.red_betted_statues}').render(screen)

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

                self.reset_betting()

            if self.fold_button.collide(mouse_pos):
                data_type, data = self.control.send(Network.FOLD, timeout=0.1)
                if data_type == Network.SEND_GAME:
                    self.set_game_info(data)

                self.reset_betting()

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

    def reset_betting(self):
        self.red_statue_button.set_image(GameScene.red_statue_disabled)
        self.current_bet_button.text = '0'
        self.current_bet = 0
        self.current_red_bet = False

    def return_to_menu(self):
        self.control.disconnect()
        self.game = None
        self.match_result_box.set_state(MatchResultBox.IDLE)
        self.control.set_active_scene('MENU_SCENE')

    def get_phase_text(self, prev_local_game, next_local_game):
        if prev_local_game is None:
            return 'Game Starts!'

        player_id = prev_local_game.player_id

        if (next_local_game.state == Game.PLAYER_0_BET and player_id == 1) or \
            (next_local_game.state == Game.PLAYER_1_BET and player_id == 0):
            return 'Opponent is betting!'
        elif (next_local_game.state == Game.PLAYER_0_BET and player_id == 0) or \
                (next_local_game.state == Game.PLAYER_1_BET and player_id == 1):
            return 'Time to bet!'

        if prev_local_game.state == Game.PLAYER_0_BET or \
           prev_local_game.state == Game.PLAYER_1_BET:
            if next_local_game.state in [Game.PLAY_CARDS, Game.PLAYER_1_WIN, Game.PLAYER_0_WIN, Game.DRAW]:

                round_history = self.local_game.round_history
                print(round_history)
                opponent_card = round_history[len(round_history)-1][(self.local_game.player_id+1)%2+1]

                if (opponent_card is None):
                    # Fold situation
                    if (prev_local_game.state == Game.PLAYER_0_BET and player_id == 0) or \
                       (prev_local_game.state == Game.PLAYER_1_BET and player_id == 1):
                        return 'You folded!'
                    elif (prev_local_game.state == Game.PLAYER_0_BET and player_id == 1) or \
                         (prev_local_game.state == Game.PLAYER_1_BET and player_id == 0):
                        return 'Opponent folded!'

                return 'Showdown!'

        return ''