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
        threading.Thread(target=self.send_instructions, args=()).start()
        threading.Thread(target=self.receive_world_info, args=()).start()

    def send_instructions(self):
        # TODO if user not in window
        while True:  # user in window
            # if user pressed on something -> duplicate
            if is_pressing():
                self.client_socket.send(' dup {}'.format(pyautogui.position()).encode())
            else:  # normal movement
                self.client_socket.send(str(pyautogui.position()).encode())
            time.sleep(0.01)

    def receive_world_info(self):
        while True:
            start_time = time.time()
            data = self.client_socket.recv(1024 ** 2).decode()
            print('FPS:', 1 / (time.time() - start_time))


def main():
    client = Client(host_ip="127.0.0.1", port=9871)


if __name__ == '__main__':
    main()
