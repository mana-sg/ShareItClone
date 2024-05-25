import socket
import time
import tkinter as tk
from tkinter import filedialog
import curses


class Sender:
    def __init__(self):
        self.receivers = []
        self.my_ip = self.get_local_ip()
        self.port = 12345
        self.selected_receiver = ""
        self.filepath = []
        self.peer_port = [12333, 6666]
        self.peer_names = []

    def create_file_threads(self):
        while len(self.filepath):
            if len(self.filepath) >= 10:
                filenames = self.filepath[:10]
                self.filepath = self.filepath[10:]
                self.connect_to_peer(filenames)

            else:
                self.connect_to_peer(self.filepath)
                self.filepath = []

    def print_table(self, stdscr):
        while True:
            stdscr.clear()
            stdscr.nodelay(True)
            stdscr.addstr(
                0, 0, "Enter the index of the person you want to send the")
            stdscr.addstr(1, 0, f"Peers: {self.peer_names}")
            client_index = stdscr.getch()
            time.sleep(0.1)
            if (len(self.peer_names) == 0):
                print("No peers found, please wait while we are scanning!")

            elif client_index-49 >= len(self.peer_names):
                stdscr.addstr(2, 0, "Invalid index")

            elif (int(client_index) in range(49, 49+len(self.peer_names))):
                self.selected_receiver = self.receivers[int(
                    client_index)-49][0]
                break

            # break
            stdscr.refresh()
        curses.endwin()

    def start_curses(self):
        curses.wrapper(self.print_table)

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

            while self.selected_receiver == "":
                try:
                    data, addr = s.recvfrom(1024)
                except socket.timeout:
                    break
                if (addr not in self.receivers):
                    self.receivers.append(addr)
                    self.peer_names.append(data.decode())

    def connect_to_peer(self, filenames):
        print(filenames)
        for file in filenames:
            while True:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect(
                            (self.selected_receiver, self.peer_port[1]))
                        with open(file, 'rb') as f:
                            while True:
                                data = f.read(1024)
                                if not data:
                                    break
                                sock.send(data)
                        print(f"{file} sent successfully")
                    break
                except:
                    continue

    def send_file_names(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.selected_receiver, self.peer_port[0]))
            for file in self.filepath:
                s.sendall(file.split("/")[-1].encode())
        time.sleep(3)

    def select_file(self):
        root = tk.Tk()
        root.withdraw()
        self.filepath = filedialog.askopenfilenames()
        root.destroy()
