from data.network.client_network import ClientNetwork
from data.network.network import Network
from config import FPS, SERVER_IP, SERVER_PORT
import pygame

class Control():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.scene_dict = {}
        self.active_scene = None

        self.network = ClientNetwork(SERVER_IP, SERVER_PORT)
        self.connected = False

    def add_scene(self, scene):
        self.scene_dict[scene.name] = scene
        scene.set_control(self)

    def set_active_scene(self, scene_name):
        self.active_scene = scene_name

    #==============================================#
    #=============== COMMUNICATION ================#
    #==============================================#

    def connect(self):
        if self.network.connect():
            self.connected = True
            return True
        else:
            return False

    def send(self, data_type, data=None, timeout=None):
        return self.network.send(data_type, data=data, timeout=timeout)

    def recv(self, timeout=None):
        return self.network.recv(timeout=timeout)

    def disconnect(self):
        self.network.disconnect()
        self.connected = False

    #==============================================#
    #================= MAIN LOOP ==================#
    #==============================================#

    def main_loop(self):
        if not self.active_scene:
            print('Error. Can\'t start the main loop since the active scene is None.')
            return
        # Starting the main loop
        while True:
            self.clock.tick(FPS)

            # Listening for server messages
            if self.connected:
                data_type, data = self.network.recv(timeout=0.01, log=False)
                if not data_type is None:
                    print(f'New server message: {Network.data_type_to_str(data_type)}')
                current_scene.handle_server_data(data_type, data=data)

            # Client side update
            current_scene = self.scene_dict[self.active_scene]
            current_scene.update()
            current_scene.render(self.screen)
            for event in pygame.event.get():
                current_scene.on_event(event)