import socket
import threading
import time

from engine.game.Map import Map
from engine.game.Point import Point

RECEIVE_SIZE = 1024
SERVER_IP = socket.gethostbyname(socket.gethostname())
world = Map()
msg_num = 0


def to_string(main_player, players_lst, points_info):
    enemy_players_info = []
    for player in players_lst:
        if player == main_player:
            continue
        enemy_players_info.append(player.info_str())
    return f"({main_player.info_str()}|{enemy_players_info}|{points_info})$$"


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
            time.sleep(2)
            client_socket, client_address = self.server_socket.accept()
            print("someone joined")
            threading.Thread(target=self.execute_client_instructions, args=(client_socket,)).start()

    def execute_client_instructions(self, client_socket):  # conversation with client
        width, height = (client_socket.recv(RECEIVE_SIZE).decode()).split('x')
        width, height = int(width), int(height)
        self.clients[client_socket] = world.create_new_player((width, height))
        while True:
            try:
                data = client_socket.recv(RECEIVE_SIZE ** 2).decode()
                dup = False
                if 'dup' in data:
                    dup = True
                data = data.replace("dup", "")
                lst = data.split('Point')
                coordinate = lst[len(lst) - 1]
                coordinate = coordinate.replace("'", "")
                coordinate = coordinate.replace("(", "")
                coordinate = coordinate.replace(")", "")
                coordinate = coordinate.replace(" ", "")
                x, y = coordinate.split(',')
                x, y = int(x[2:]), int(y[2:])
                player = self.clients[client_socket]
                world.exec_instructions(player=player, player_instructions=(dup, Point(x, y)))
            except Exception:
                print('error')
                break

    def share_data_to_clients(self):
        global msg_num
        while True:
            start_time = time.time()
            if len(self.clients) > 0:
                points_info = []
                for point in world.points:
                    points_info.append(f"({point.x}X{point.y})")
                for client in self.clients.copy():
                    try:
                        client.send(to_string(main_player=self.clients[client], players_lst=world.players,
                                              points_info=points_info).encode())
                    except ConnectionResetError:
                        world.players.remove(self.clients[client])
                        del self.clients[client]
            print(time.time() - start_time)


def main():
    server = Server(ip=SERVER_IP, port=777)
    server.accept()


if __name__ == '__main__':
    main()
