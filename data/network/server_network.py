from data.network.network import Network
from queue import Queue
import socket

class ServerNetwork(Network):
    def __init__(self, inputs, outputs):
        super().__init__()
        self.inputs = inputs
        self.outputs = outputs

    def is_client_connected(self, client):
        if client in self.inputs:
            return True
        return False

    def add_client(self, client):
        self.inputs.append(client)

    def remove_client(self, client):
        if client in self.outputs:
            self.outputs.remove(client)
        if client in self.inputs:
            self.inputs.remove(client)
        client.shutdown(socket.SHUT_RDWR)
        client.close()
