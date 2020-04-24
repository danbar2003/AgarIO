import socket
import threading

from server_side.engine.game.Map import Map
from server_side.engine.game.Point import Point

RECEIVE_SIZE = 1024
SERVER_IP = '127.0.0.1'  # socket.gethostbyname(socket.gethostname())
world = Map()


def to_string(main_player, players_lst, points_lst):
    enemy_players_info = []
    for player in players_lst:
        if player == main_player:
            continue
        enemy_players_info.append(player.info_str())
    points_info = []
    for point in points_lst:
        points_info.append(f"({point.x, point.y})")
    return f"main_player={main_player.info_str()}, enemy_players={enemy_players_info}, points={points_info}"


class Server:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(1)
        self.clients = {}
        threading.Thread(target=self.share_data_to_clients, args=()).start()
        print(f"server is listening \n server_ip:{SERVER_IP} \n port:{self.port}")

    def accept(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print("someone joined")
            self.clients[client_socket] = world.create_new_player()
            threading.Thread(target=self.execute_client_instructions, args=(client_socket,)).start()

    def get_clients(self):
        lst = []
        for client in self.clients:
            lst.append(client)
        return lst

    def execute_client_instructions(self, client_socket):  # conversation with client
        while True:
            """
            :param client_socket:
            :return: (Boolean, mouse_loc) boolean - dup or not 
            """
            try:
                data = client_socket.recv(RECEIVE_SIZE * 32).decode()

                dup = False
                if 'dup' in data:
                    dup = True
                lst = data.split('Point')
                point_str = lst[len(lst) - 1]
                x_str, y_str = point_str.split(',')
                x = int(x_str.split('=')[1])
                y = int((y_str.split('=')[1])[:y_str.split('=')[1].find(')')])
                player = self.clients[client_socket]
                world.exec_instructions(player=player, player_instructions=(dup, Point(x, y)))
            except Exception:
                pass

    def share_data_to_clients(self):
        while True:
            for client in self.clients:
                client.send(to_string(main_player=self.clients[client], players_lst=world.players,
                                                    points_lst=world.points).encode())


def main():
    server = Server(ip=SERVER_IP, port=9871)
    threading.Thread(target=server.accept, args=()).start()
    # while True:
    # world.to_string()


if __name__ == '__main__':
    main()
