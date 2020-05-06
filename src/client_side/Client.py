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
        time.sleep(1)
        self.gui_window = WindowGui(width, height)
        threading.Thread(target=self.send_instructions, args=()).start()

    def send_instructions(self):
        # TODO if user not in window
        while True:  # user in window
            # if user pressed on something -> duplicate
            if is_pressing():
                self.client_socket.send('dup{}'.format(pyautogui.position()).encode())
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
                self.gui_window.print_data(msg)
                msg = next_msg
            else:
                msg += data


def main():
    client = Client(host_ip="192.168.0.138", port=777)
    client.receive_world_info()


if __name__ == '__main__':
    main()
