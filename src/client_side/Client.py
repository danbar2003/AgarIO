import socket
import pyautogui
import time
import threading


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
        threading.Thread(target=self.send_instructions, args=()).start()
        threading.Thread(target=self.receive_world_info, args=()).start()

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
        while True:
            msg = ''
            next_msg = ''
            data = self.client_socket.recv(1024 ** 2).decode()
            if '$$' in data:
                lst = data.split('$$')
                msg += lst[0]
                next_msg = lst[0]
                display_data(msg)
                msg = next_msg
            else:
                msg += data


def display_data(frame):
    print(frame)


def main():
    client = Client(host_ip="127.0.0.1", port=765)


if __name__ == '__main__':
    main()
