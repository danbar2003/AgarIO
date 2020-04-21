import socket
import threading

from server_side.engine.game.Player import Player

RECEIVE_SIZE = 1024


def receive_data(client_socket):

    """
    :param client_socket:
    :return: (Boolean, mouse_loc) boolean - dup or not
    """
    mouse_loc_data = client_socket.recv(RECEIVE_SIZE * 16).decode()

    #print("???", mouse_loc_data)
    # -
    return False, mouse_loc_data
    # TODO - more work to do here!!!


class Server:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.ip, self.port))
        print("?")
        self.server_socket.listen(1)
        self.clients = {}
        threading.Thread(target=self.accept, args=()).start()

    def accept(self):
        while True:
            print("listening")
            client_socket, client_address = self.server_socket.accept()
            self.clients[client_socket] = Player(len(self.clients), color=0)  # TODO color

    def data_process(self, client, data):
        is_dup, mouse_loc = data
        if is_dup:
            pass
        else:
            player = self.clients[client]
            player.move(mouse_loc)
            pass

    def share_data(self, client):
        pass

    def game_loop(self):
        while True:
            lst = []
            for client in self.clients:
                lst = [client]

            for client in lst:
                self.data_process(client=client, data=receive_data(client))
                self.share_data(client)


def main():
    server = Server(ip=socket.gethostbyname(socket.gethostname()), port=9872)
    server.game_loop()


if __name__ == '__main__':
    main()
