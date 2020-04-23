import socket
import pyautogui
import time

BUFFER = []


def is_pressing():
    pass


class Client:
    def __init__(self, host_ip, port):
        self.ip = host_ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))

    def send_data(self):
        # TODO if user not in window
        while True:  # user in window
            # if user pressed on something -> duplicate
            if is_pressing():
                self.client_socket.send(' dup {}'.format(pyautogui.position()).encode())
            else:  # normal movement
                self.client_socket.send(str(pyautogui.position()).encode())
        time.sleep(0.0001)


def main():
    client = Client(host_ip="127.0.0.1", port=9871)
    client.send_data()


if __name__ == '__main__':
    main()
