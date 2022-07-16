from data.network.network import Network
import socket

class ClientNetwork(Network):

    def __init__(self, server_ip, server_port):
        self.client  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server  = server_ip
        self.port    = server_port
        self.address = (self.server, self.port)

    def send(self, data_type, data=None, timeout=None):
        super().send(self.client, data_type, data=data)
        # Waiting for a response
        return self.recv(timeout=timeout)

    def recv(self, timeout=None, log=True):
        return super().recv(self.client, timeout=timeout, log=log)

    def connect(self):
        try:
            self.client.connect(self.address)
            print('Connected to server!')
            return True
        except:
            print(f'Error when trying to connect to the server {self.address} by the Network.')
            print('Checking if a connection was already established.')
            # Check if is already connected
            return self.is_connected()