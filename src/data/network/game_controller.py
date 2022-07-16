from data.network.network import Network
from data.components.game import Game


class GameController():
    def __init__(self, player_clients, network):
        self.player_client_to_id = {player_clients[0] : 0,
                                    player_clients[1] : 1}
        self.network = network
        self.game = Game()

    def update(self):
        pass

    def get_player_clients(self):
        return [i for i in self.player_client_to_id.keys()]

    def get_game_to_client(self, client):
        return self.game.get_local_game(self.player_client_to_id[client])

    def handle_in_game_message(self, client, data_type, data):

        if not client in self.player_client_to_id:
             self.network.send(client, Network.FAILED)
             return
        player_id = self.player_client_to_id[client]

        if data_type == Network.PLAY_CARD:
            status = self.handle_play_card(player_id, data)
        elif data_type == Network.PLACE_BET:
            status = self.handle_place_bet(player_id, data)
        elif data_type == Network.FOLD:
            status = self.handle_fold(player_id)
        elif data_type == Network.SURRENDER:
            status = self.handle_surrender(player_id)

        if status:
            for c in self.get_player_clients():
                local_game = self.get_game_to_client(c)
                self.network.send(c, Network.SEND_GAME, data=local_game)
        else:
            self.network.send(client, Network.FAILED)

    def handle_surrender(self, player_id):
        if player_id == 0:
            self.game.state = Game.PLAYER_1_WIN
        elif player_id == 1:
            self.game.state = Game.PLAYER_0_WIN
        return True

    def handle_fold(self, player_id):

        # Can't fold out of your betting phasde
        if (player_id == 0 and self.game.state != Game.PLAYER_0_BET) or \
           (player_id == 1 and self.game.state != Game.PLAYER_1_BET):
            print('Invalid message: Can\'t fold out of your betting phase.')
            return False

        # You can't fold if you've betted a red statue
        if self.game.red_betted_statues[player_id]:
            print('Invalid message: Can\'t fold when you\'ve betted a red statue.')
            return False

        self.game.stored_statues[player_id] -= self.game.betted_statues[player_id]
        self.game.stored_statues[(player_id+1)%2] += self.game.betted_statues[player_id]

        if self.game.stored_statues[player_id] <= 0:
            self.game.end_game()
            return True

        self.game.next_turn(((player_id+1)%2, None, None))

        return True

    def handle_place_bet(self, player_id, pair):
        statues = pair[0]
        red_statue = pair[1]

        # The bet must be valid
        if type(statues) != int or type(red_statue) != bool:
            print(f'Invalid message: Bet must be a pair of type (Int, Bool). Got {(type(statues), type(red_statue))}')
            return False
        if statues < 0:
            print(f'Invalid message: Bet must be non-negative. Got {statues}.')
            return False

        # You can't bet out of your betting phase
        if (player_id == 0 and self.game.state != Game.PLAYER_0_BET) or \
           (player_id == 1 and self.game.state != Game.PLAYER_1_BET):
            print(f'Invalid message: Can\'t bet out of your betting phase.')
            return False

        # You can't bet more than you have
        if self.game.betted_statues[player_id] + statues > self.game.stored_statues[player_id]:
            print(f'Invalid message: Can\'t bet more than you have. Got {statues}.')
            return False
        # You can't bet a red statue twice
        if self.game.red_betted_statues[player_id] and red_statue:
            print(f'Invalid message: Can\'t bet more than one red statue.')
            return False

        betted_amount = statues + (1 if red_statue else 0)

        # You can't bet more than your opponent has
        if betted_amount > self.game.stored_statues[(player_id+1)%2]:
            print(f'Invalid message: Can\'t bet more than your opponent has. Got {betted_amount}. Need at most {self.game.stored_statues[(player_id+1)%2]}.')
            return False

        # You can't bet less than your opponent
        if self.game.last_bet is not None:
            if betted_amount < self.game.last_bet:
                print(f'Invalid message: Can\'t bet less than your opponent. Got {betted_amount}. Need at least {self.game.last_bet}.')
                return False
        else:
            print(f'Betted: {betted_amount} and the last bet was {self.game.last_bet}.')

        # Valid bet
        self.game.betted_statues[player_id] += statues
        self.game.red_betted_statues[player_id] =\
            self.game.red_betted_statues[player_id] or red_statue

        if self.game.last_bet is not None and betted_amount == self.game.last_bet:
            # In this case, the bet is a call and the betting phase is over
            self.game.showdown()
        else:
            # In this case the best is either a raise, or the first bet
            # We'll handle it and then proceed to the next betting turn
            if self.game.last_bet is None:
                # Then this is the first bet of the round
                self.game.last_bet = betted_amount
            else:
                # Then this is a raise
                self.game.last_bet = betted_amount - self.game.last_bet

            if self.game.state == Game.PLAYER_0_BET:
                self.game.state = Game.PLAYER_1_BET
            elif self.game.state == Game.PLAYER_1_BET:
                self.game.state = Game.PLAYER_0_BET

        return True

    def handle_play_card(self, player_id, card):

        if self.game.state != Game.PLAY_CARDS:
            print(f'Invalid message: Can\'t play cards out of playing phase.')
            return False

        if self.game.cards_played[player_id] is not None:
            print(f'Invalid message: You already played a card.')
            return False

        if card not in self.game.hands[player_id]:
            print(f'Invalid message: Can\'t play a card that is not in your hand.')
            return False

        if not Game.is_valid_card(card):
            print(f'Invalid message: Card is invalid. Got {card}.')
            return False

        # Valid play
        self.game.cards_played[player_id] = card
        if self.game.cards_played[(player_id+1)%2] is None:
            return True

        # In this case, the PLAY_CARDS phase is over
        if self.game.first_to_bet == 0:
            self.game.state = Game.PLAYER_0_BET
            self.game.first_to_bet = 1
        else:
            self.game.state = Game.PLAYER_1_BET
            self.game.first_to_bet = 0

        self.game.betted_statues = [1, 1]

        return True