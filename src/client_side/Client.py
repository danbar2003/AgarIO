import socket
import pyautogui

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
                self.client_socket.send('(dup, {})'.format(pyautogui.position()).encode())
            else:  # normal movement
                self.client_socket.send(str(pyautogui.position()).encode())


def main():
    client = Client(host_ip="192.168.0.133", port=9872)
    client.send_data()


if __name__ == '__main__':
    main()
