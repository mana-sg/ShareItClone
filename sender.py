import socket
import time
import tkinter as tk
from tkinter import filedialog


class Sender:
    def __init__(self):
        self.receivers = []
        self.my_ip = self.get_local_ip()
        self.port = 12345
        self.selected_receiver = ""
        self.filepath = ""
        self.peer_port = 12333

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
        finally:
            s.close()
        return local_ip

    def receive_broadcast(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.bind(('', self.port))

            print("Listening for broadcast messages...")

            start_time = time.time()
            while True and (time.time() - start_time <= 5):
                data, addr = s.recvfrom(1024)
                if (addr not in self.receivers):
                    self.receivers.append(addr)
                    print("Receivers list: ", self.receivers)

        client_index = int(input(
            "Enter index of whih person you want to send the file to: "))
        print("Sending file to: ", self.receivers[client_index])
        self.selected_receiver = self.receivers[client_index][0]

    def connect_to_peer(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((self.selected_receiver, self.peer_port))
            with open(self.filepath, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    client_socket.send(data)

            print(f"{self.filepath} sent successfully")

    def send_file_names(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.selected_receiver, self.peer_port))
            s.sendall(self.filepath.split("/")[-1].encode())
        time.sleep(5)

    def select_file(self):
        root = tk.Tk()
        root.withdraw()
        self.filepath = filedialog.askopenfilename()
        root.destroy()
