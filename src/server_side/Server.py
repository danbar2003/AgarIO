import socket
import threading

from server_side.engine.game import Map

RECEIVE_SIZE = 1024
SERVER_IP = socket.gethostbyname(socket.gethostname())
world = Map.Map()


def receive_data(client_socket):
    # TODO mouse_loc_data should be Point Object
    """
    :param client_socket:
    :return: (Boolean, mouse_loc) boolean - dup or not
    """
    mouse_loc_data = client_socket.recv(RECEIVE_SIZE * 32).decode()

    # print("???", mouse_loc_data)
    # -
    return False, mouse_loc_data


class Server:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(1)
        self.clients = {}
        threading.Thread(target=self.accept, args=()).start()

    def accept(self):
        print(f"server is listening \n server_ip:{SERVER_IP} \n port:{self.port}")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print("someone joined")
            self.clients[client_socket] = world.create_new_player()

    def get_clients(self):
        lst = []
        for client in self.clients:
            lst.append(client)
        return lst

    def game_loop(self):
        while True:
            # execute all clients instructions
            for client in self.get_clients():
                player = self.clients[client]
                Map.exec_instructions(player=player, player_instructions=receive_data(client))
            world.player_interactions()
            # share to clients world status
            for client in self.get_clients():
                pass


def main():
    server = Server(ip=SERVER_IP, port=9872)
    server.game_loop()


if __name__ == '__main__':
    main()
