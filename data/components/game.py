import itertools
import random

class Game():

    # Game States
    PLAY_CARDS   = 0
    PLAYER_0_BET = 1
    PLAYER_1_BET = 2
    PLAYER_0_WIN = 3
    PLAYER_1_WIN = 4
    DRAW         = 5

    state_to_str_dict = {
        PLAY_CARDS : 'PLAY_CARDS',
        PLAYER_0_BET : 'PLAYER_0_BET',
        PLAYER_1_BET : 'PLAYER_1_BET',
        PLAYER_0_WIN : 'PLAYER_0_WIN',
        PLAYER_1_WIN : 'PLAYER_1_WIN',
        DRAW         : 'DRAW'
    }

    CARD_NUMBERS = ['1','2','3','4','5','6','7','8','9','10','11','12','13']
    CARD_SUITS   = ['h','d','c','s'] # In order
    NUMBER_OF_ROUNDS = 10

    def state_to_str(state):
        if not state in Game.state_to_str_dict:
            return None
        return Game.state_to_str_dict[state]

    def is_valid_card(card):
        if type(card) != str:
            return False

        if len(card) not in [2, 3]:
            return False

        number = card[:-1]
        suit   = card[len(card)-1]

        if (number in Game.CARD_NUMBERS) and (suit in Game.CARD_SUITS):
            return True

        return False

    def card_wins_against(card1, card2):
        card1_number = int(card1[:-1])
        card1_suit   = card1[len(card1)-1]
        card2_number = int(card2[:-1])
        card2_suit   = card2[len(card2)-1]

        # Checking by number
        if card1_number == 1:
            if card2_number != 2:
                return True
            else:
                return False
        elif card1_number == 2:
            if card2_number == 1:
                return True
            else:
                return False
        else:
            if card1_number > card2_number:
                return True
            elif card1_number < card2_number:
                return False
            else:
                # In this case, the numbers are equal
                # resolving by suit
                suit1_power = Game.CARD_SUITS.index(card1_suit)
                suit2_power = Game.CARD_SUITS.index(card2_suit)

                if suit1_power > suit2_power:
                    return True
                elif suit1_power < suit2_power:
                    return False
                else:
                    # In this case, they are the same card
                    return None

    def __init__(self):
        self.deck = list(''.join(e) for e in itertools.product(Game.CARD_NUMBERS, Game.CARD_SUITS))
        self.deck = self.deck*3
        random.shuffle(self.deck)

        self.current_round      = 0
        self.round_history      = []
        self.stored_statues     = [10, 10]
        self.betted_statues     = [0, 0]
        self.red_betted_statues = [False, False]
        self.cards_played       = [None, None]
        self.hands              = [[self.deck.pop(), self.deck.pop()],
                                   [self.deck.pop(), self.deck.pop()]]
        self.first_to_bet       = 0
        self.last_bet           = None
        self.player_ended_showdown = [False, False] # Ended showdown phase
        self.state = Game.PLAY_CARDS

    def showdown(self):
        # Determining the round winner
        player_0_card = self.cards_played[0]
        player_1_card = self.cards_played[1]

        player_0_wins_round = Game.card_wins_against(player_0_card, player_1_card)

        if player_0_wins_round is None:
            # Then it is a draw
            self.next_turn((None, None, None))
        elif player_0_wins_round:
            # If the other player played a red statue, they lose
            if self.red_betted_statues[1]:
                self.state = Game.PLAYER_0_WIN
                return

            self.stored_statues[1] -= self.betted_statues[1]
            self.stored_statues[0] += self.betted_statues[1]
            self.next_turn((0, player_0_card, player_1_card))
        else:
            # If the other player played a red statue, they lose
            if self.red_betted_statues[0]:
                self.state = Game.PLAYER_1_WIN
                return

            self.stored_statues[0] -= self.betted_statues[0]
            self.stored_statues[1] += self.betted_statues[0]
            self.next_turn((1, player_0_card, player_1_card))

        if self.stored_statues[0] == 0 or self.stored_statues[1] == 0:
            self.end_game()
            return

    def next_turn(self, history):
        # Refill the hands
        for current_id in [0,1]:
            self.hands[current_id].remove(self.cards_played[current_id])
            if len(self.deck) == 0:
                self.end_game()
                return True
            self.hands[current_id].append(self.deck.pop())


        self.last_bet           = None
        self.cards_played       = [None, None]
        self.betted_statues     = [0, 0]
        self.red_betted_statues = [False, False]
        self.state = Game.PLAY_CARDS

        self.current_round += 1
        self.round_history.append(history)
        if self.current_round >= Game.NUMBER_OF_ROUNDS:
            self.end_game()

    def end_game(self):
        if self.stored_statues[0] > self.stored_statues[1]:
            self.state = Game.PLAYER_0_WIN
        elif self.stored_statues[0] < self.stored_statues[1]:
            self.state = Game.PLAYER_1_WIN
        else:
            self.state = Game.DRAW

    def get_local_game(self, player_id):
        opponent_high_cards = [(int(card[0]) >= 8 or int(card[0]) == 1) for card in self.hands[(player_id+1)%2]]

        return LocalGame(player_id,
                         self.current_round,
                         self.round_history,
                         self.stored_statues,
                         self.betted_statues,
                         self.red_betted_statues,
                         self.cards_played[player_id],
                         self.hands[player_id],
                         opponent_high_cards,
                         self.state)

    def __str__(self):
        return f'-----\nRemaining cards in deck: {len(self.deck)}.\n' +\
               f'{self.deck}.\n'+\
               f'Round: {self.current_round}.\n' +\
               f'Round history: {self.round_history}.\n' +\
               f'Stored statues: {self.stored_statues}.\n' +\
               f'Stored statues: {self.stored_statues}.\n' +\
               f'Statues betted: {self.betted_statues}.\n' +\
               f'Red statues betted: {self.red_betted_statues}.\n' +\
               f'Cards played: {self.cards_played}.\n' +\
               f'Hands: {self.hands}.\n' +\
               f'Game state: {Game.state_to_str(self.state)}.\n-----'

class LocalGame():
    def __init__(self, player_id, current_round, round_history, stored_statues,
                 betted_statues, red_betted_statues, card_played, hand,
                 opponent_high_cards, state):
        self.player_id = player_id
        self.current_round = current_round
        self.round_history = round_history
        self.stored_statues = stored_statues
        self.betted_statues = betted_statues
        self.red_betted_statues = red_betted_statues
        self.card_played = card_played
        self.hand = hand
        self.opponent_high_cards = opponent_high_cards
        self.state = state

    def get_player_id(self):
        return self.player_id

    def __str__(self):
        return f'-----\nRound: {self.current_round}.\n' +\
               f'Round history: {self.round_history}.\n' +\
               f'Stored statues: {self.stored_statues}.\n' +\
               f'Stored statues: {self.stored_statues}.\n' +\
               f'Statues betted: {self.betted_statues}.\n' +\
               f'Red statues betted: {self.red_betted_statues}.\n' +\
               f'Card played: {self.card_played}.\n' +\
               f'Hand: {self.hand}.\n' +\
               f'Opponent high cards: {self.opponent_high_cards}.\n' +\
               f'Game state: {Game.state_to_str(self.state)}.\n-----'