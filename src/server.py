from config import SERVER_IP, SERVER_PORT, MAX_CONNECTIONS
from data.network.server_network import ServerNetwork
from data.network.match_manager import MatchManager
from data.network.network import Network
from queue import Queue
import select
import socket
import pickle

#=======================================================================#
#=========================== SERVER SETUP ==============================#
#=======================================================================#


# AF_INET corresponds to IPV4 and SOCK_STREAM corresponds to TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Set the server to non-blocking mode (see documentation)
server.setblocking(0)
# Binding the socket to a pair (ip, port)
try:
    server.bind((SERVER_IP, SERVER_PORT))
except socket.error as e:
    print(f'Error in trying to bind the socket to the server/port.\n{e}')
# Maximum of MAX_CONNECTIONS connections at the same time
server.listen(MAX_CONNECTIONS)
print(f'Server started. Waiting for connections on port {SERVER_PORT}.')

# Network to handle sends and recvs
network = ServerNetwork([server], [])
# Object to handle the matches
match_manager = MatchManager(network)

#=======================================================================#
#========================= CONNECTION LOOP =============================#
#=======================================================================#


while network.inputs:

    #==========================#
    #====== MATCH LOGIC =======#
    #==========================#

    match_manager.update()

    #==========================#
    #=== COMMUNICATION LOOP ===#
    #==========================#

    readable, writable, exceptional = select.select(network.inputs, network.outputs, network.inputs, 10)

    # Handling the readable sockets
    for s in readable:
        if s is server:
            # If the server is 'readable', that means we got a new connection
            try:
                client_socket, client_address = s.accept()
                client_socket.setblocking(False)
                network.add_client(client_socket)
                print(f'New connection from {client_socket.getsockname()}.')
                continue
            except Exception as e:
                print(f'Failed to accept new connection.\n{e}')

        # In this case, there is a message to be received
        data_type, data = network.recv(s)
        print(f'New message from {s.getsockname()}: {Network.data_type_to_str(data_type)}.')

        if data_type is None:
            # If there is no data, that means the connection is over
            print(f'Socket disconnected: {s.getsockname()}.')
            network.remove_client(s)
            continue

        #========================#
        #=== GENERAL MESSAGES ===#
        #========================#

        # If message is 'close', we'll shut down the server
        if data == 'close':
            server.close()
            exit()

        # Client requesting to check if it's still connected to the server
        if data_type == Network.CHECK_CONNECTION:
            network.send(s, Network.SUCCESS)
            continue

        if data_type == Network.ENTER_MATCH_QUEUE:
            try:
                match_manager.queue(s) # 10 seconds timeout
                print(f'{s.getsockname()} enters the match queue. Match queue size: {match_manager.match_queue.qsize()}')
                network.send(s, Network.SUCCESS)
            except Exception as e:
                print(f'Error when trying to add {s.getsockname()} to the match queue.\n{e}')
                network.send(s, Network.FAILED)

        #========================#
        #=== IN-GAME MESSAGES ===#
        #========================#

        if s in match_manager.match_dict and data_type in Network.get_in_game_data_types():
            game_controller = match_manager.match_dict[s]
            game_controller.handle_in_game_message(s, data_type, data)