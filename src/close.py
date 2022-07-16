from config import *
import socket
from data.network.network import *
from data.network.client_network import *

network = ClientNetwork(SERVER_IP, SERVER_PORT)
network.connect()
network.send(5, data='close')