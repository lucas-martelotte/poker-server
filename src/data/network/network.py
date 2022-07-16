import socket
import pickle

class Network():

    HEADER_SIZE = 10

    #=====================#
    #= Client Data Types =#
    #=====================#
    ENTER_MATCH_QUEUE = 0
    CHECK_CONNECTION  = 1
    PLAY_CARD         = 2
    PLACE_BET         = 3
    FOLD              = 4
    SURRENDER         = 5

    #=====================#
    #= Server Data Types =#
    #=====================#
    MATCH_FOUND   = 500
    MATCH_ABORTED = 501
    SEND_GAME     = 502
    VICTORY       = 503
    DEFEAT        = 504
    NEW_TURN      = 505

    #=====================#
    #= Status Data Types =#
    #=====================#
    FAILED = -1
    SUCCESS = -2


    data_type_to_str_dict = {
        ENTER_MATCH_QUEUE : 'ENTER_MATCH_QUEUE',
        CHECK_CONNECTION  : 'CHECK_CONNECTION',
        PLAY_CARD         : 'PLAY_CARD',
        PLACE_BET         : 'PLACE_BET',
        FOLD              : 'FOLD',
        SURRENDER         : 'SURRENDER',
        MATCH_FOUND       : 'MATCH_FOUND',
        MATCH_ABORTED     : 'MATCH_ABORTED',
        SEND_GAME         : 'SEND_GAME',
        VICTORY           : 'VICTORY',
        DEFEAT            : 'DEFEAT',
        NEW_TURN          : 'NEW_TURN',
        FAILED            : 'FAILED',
        SUCCESS           : 'SUCCESS'
                        }

    def get_in_game_data_types():
        return [
                Network.PLAY_CARD,
                Network.PLACE_BET,
                Network.FOLD,
                Network.SURRENDER
               ]

    def data_type_to_str(msg):
        if msg in Network.data_type_to_str_dict:
            return Network.data_type_to_str_dict[msg]
        return str(msg)

    def __init__(self):
        pass

    #===================================================#
    #================== COMMUNICATION ==================#
    #===================================================#

    def send(self, client, data_type, data=None):

        if data is None:
            data_lenght = 0
            data_pickle = bytes('','utf-8')
        else:
            data_pickle = pickle.dumps(data)
            data_lenght = len(data_pickle)

        string = f'{data_type:<{self.HEADER_SIZE}}'
        string += f'{data_lenght:<{self.HEADER_SIZE}}'
        data_with_header = bytes(string,'utf-8') + data_pickle

        try:
            # Sending the message
            client.send((data_with_header))
        except socket.error as e:
            print(f'Error when trying to send data to {client.getsockname()}.')
            print(e)


    def recv(self, client, timeout=None, log=True):
        if not timeout is None:
            client.settimeout(timeout)

        try:
            data_type = int(client.recv(Network.HEADER_SIZE))
            data_size = int(client.recv(Network.HEADER_SIZE))

            if log:
                print(f'Data type: {Network.data_type_to_str(data_type)}. Data size: {data_size}.')

            if data_type is None:
                if log:
                    print('Data type is None.')
                return None, None

            if data_size > 0:
                bytes_data = client.recv(data_size)
                data = pickle.loads(bytes_data)
            else:
                data = None

            client.setblocking(False)
            return data_type, data
        except Exception as e:
            if log:
                print(f'Failed to receive from {client.getsockname()}.\n{e}')
            client.setblocking(False)
            return None, None

    def disconnect(self):
        if self.is_connected():
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
            print('Disconnected.')
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def is_connected(self):
        try:
            data_type, data = self.send(self.CHECK_CONNECTION, timeout=1)
            if data_type is None:
                print(f'Client is not connected to server.')
                return False
            print(f'Client was already connected to server.')
            return True
        except:
            print('Error. Client was not connected and was unable to establish a new connection.')
            return False
