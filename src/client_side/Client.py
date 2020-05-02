import socket
import time
import pyautogui
import threading
from client_side.gui.WindowGui import WindowGui


def is_pressing():
    pass


class Client:
    def __init__(self, host_ip, port):
        self.ip = host_ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))
        width, height = pyautogui.size()
        self.client_socket.send(f'{width}x{height}'.encode())  # res
        self.gui_window = WindowGui(width, height)
        time.sleep(1)
        threading.Thread(target=self.send_instructions, args=()).start()

    def send_instructions(self):
        # TODO if user not in window
        while True:  # user in window
            # if user pressed on something -> duplicate
            if is_pressing():
                self.client_socket.send('dup {}'.format(pyautogui.position()).encode())
            else:  # normal movement
                self.client_socket.send(str(pyautogui.position()).encode())
            time.sleep(0.01)

    def receive_world_info(self):
        msg = ''
        while True:
            data = self.client_socket.recv(1024 ** 2).decode()
            if '$$' in data:
                lst = data.split('$$')
                if len(lst) > 2:
                    msg += lst[0]
                    next_msg = lst[len(lst) - 1]
                else:
                    msg += lst[0]
                    next_msg = lst[1]
                main_player, enemy_players_info, points_info = convert_str_to_data(msg)
                self.gui_window.calculate_fov(main_player, enemy_players_info, points_info)
                msg = next_msg
            else:
                msg += data


def convert_str_to_data(frame):
    main_player, enemy_players, points = frame.split('|')
    color, circles = main_player.split('#')
    print(color)
    color = float(color[1:])
    circles = remove_chars(circles, ["[", "]", "'", "(", ")", " "])
    main_player = []
    for circle in circles.split(','):
        coordinate, radios = circle.split('!')
        x, y = coordinate.split(':')
        main_player.append(((float(x), float(y)), float(radios)))
    main_player = (color, main_player)

    enemy_players_info = []
    for enemy_player in enemy_players.split('"'):
        if ':' in enemy_player:
            color, circles = enemy_player.split('#')
            circles = remove_chars(circles, ["[", "]", "'", "(", ")", " "])
            enemy_player = []
            for circle in circles.split(','):
                coordinate, radios = circle.split('!')
                x, y = coordinate.split(':')
                enemy_player.append(((float(x), float(y)), float(radios)))
            enemy_players_info.append((color, enemy_player))
    points_info = []
    for point in points.split(','):
        point = remove_chars(point, ["'", "(", ")", "[", "]"])
        x, y = point.split('X')
        points_info.append((float(x), float(y)))
    return main_player, enemy_players_info, points_info


def remove_chars(str_data, str_lst):
    for str_part in str_lst:
        str_data = str_data.replace(str_part, "")
    return str_data


def main():
    client = Client(host_ip="192.168.0.133", port=777)
    client.receive_world_info()


if __name__ == '__main__':
    main()
