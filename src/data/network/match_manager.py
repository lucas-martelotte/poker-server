from data.network.game_controller import GameController
from data.network.network import Network
from config import MAX_CONNECTIONS
from queue import Queue
import socket

class MatchManager():

    def __init__(self, network):
        self.network = network

        self.match_dict = {} # Dict in the form (client : game_object)
        self.match_queue = Queue(MAX_CONNECTIONS)

        self.ready_players = [None, None] # Pair of players ready to play
        self.match_found = False

    def update(self):
        #=====================#
        #=== Game Creation ===#
        #=====================# # Area to handle new matches being created
        self.check_disconnections() # Check if a ready/match player disconnected
        self.dequeue_player() # Try to dequeue a player and put them in the "ready players"
        if self.check_ready_players(): # Check if there are 2 ready players
            print(f'Creating a match between {self.ready_players[0].getsockname()} and {self.ready_players[1].getsockname()}.')
            self.create_match()
        #=====================#
        #== Game Management ==#
        #=====================# # Area to handle ongoing matches
        for game_controller in self.match_dict.values():
            game_controller.update()

    def check_disconnections(self):
        # Checking if someone accepted disconnected from the queue
        for i in range(len(self.ready_players)):
            if not self.ready_players[i] is None:
                if not self.network.is_client_connected(self.ready_players[i]):
                    print(f'Player {i+1} lost connection.')
                    self.ready_players[i] = None
                    print(f'Current Ready Players: {[(not i is None) for i in self.ready_players]}.')

                    # If a match was being started, abort it and notify the remaining player
                    if self.match_found:
                        self.match_found = False
                        for j in range(len(self.ready_players)):
                            if not self.ready_players[j] is None:
                                print(f'Removing player {j+1} since match was aborted.')
                                self.network.send(self.ready_players[j], Network.MATCH_ABORTED)
                                self.ready_players[j] = None
        # Checking if someone disconnected from the match
        clients_to_delete = []
        for key, value in self.match_dict.items():
            if not self.network.is_client_connected(key):
                game_controller = self.match_dict[key]
                # Sending the winning message to the opponent
                for client in game_controller.get_player_clients():
                    if not client is key and self.network.is_client_connected(client):
                        self.network.send(client, Network.VICTORY)
                    clients_to_delete.append(client)
        # Deleting the dict entries
        for client in clients_to_delete:
            del self.match_dict[client]

    def create_match(self):
        # This function creates a new match between the 2 ready players, sends a message
        # to them containing the game object and then empties ready_players

        print(f'Starting the game between {self.ready_players[0]} and {self.ready_players[1]}.')

        # Creating the game controller
        game_controller = GameController(self.ready_players, self.network)

        print(game_controller.game)

        # Puting the game_controller in the quick_match_dict
        self.match_dict[self.ready_players[0]] = game_controller
        self.match_dict[self.ready_players[1]] = game_controller

        # Sending the game information and the id to the clients
        self.network.send(self.ready_players[0], Network.SEND_GAME, data=(game_controller.get_game_to_client(self.ready_players[0])))
        self.network.send(self.ready_players[1], Network.SEND_GAME, data=(game_controller.get_game_to_client(self.ready_players[1])))

        # Cleaning the lists and waiting for new matches
        self.ready_players = [None, None]
        self.match_found = False

        print('Game was created. Match info was cleared. Waiting for new matches.')

    #================================================#
    #=================== QUEUEING ===================#
    #================================================#

    def dequeue_player(self):
        # Trying to match a player in the quick_play_queue
        for i in range(len(self.ready_players)):
            if not self.match_queue.empty() and self.ready_players[i] is None:
                print(f'Searching for a player {i+1}.')
                self.ready_players[i] = self.match_queue.get()
                if not self.network.is_client_connected(self.ready_players[i]):
                    print(f'Player {s.getsockname()} not connected. Removing from queue.')
                    print(f'Current Ready Players: {[(not i is None) for i in self.ready_players]}.')
                    self.ready_players[i] = None
                else:
                    print(f'Found a player {i+1}: {self.ready_players[i].getsockname()}')
                    print(f'Current Ready Players: {[(not i is None) for i in self.ready_players]}.')

    def check_ready_players(self):
        # Checking if we can start a match
        if (not None in self.ready_players):
            if not self.match_found:
                # In this case, both players are ready to play! We will send a
                # request to get both players' teams and then start the game
                print('Match found!')
                self.match_found = True
                for i in range(len(self.ready_players)):
                    self.network.send(self.ready_players[i], Network.MATCH_FOUND)
            return True
        return False

    def queue(self, client, block=True, timeout=10):
        self.match_queue.put(client, block=block, timeout=timeout)

    def get_ready_player_index(self, client):
        for i in range(len(self.ready_players)):
            if client is self.ready_players[i]:
                return i
        return None
