import socket
import time


class Receiver:
    def __init__(self, username):
        self.my_ip = self.get_local_ip()
        self.broadcast_port = 12345
        self.peer_port = 12333
        self.filename = ""
        self.username = username

    def receive_file(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.my_ip, self.peer_port))
            server_socket.listen(1)
            print("Server is listening on port", self.peer_port)
            conn, addr = server_socket.accept()
            print("Connection established with", addr)
            with open(self.filename, 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
            print("File received successfully")

    def receive_filenames(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.my_ip, self.peer_port))
            s.listen()

            print('Waiting for a connection...')
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)

                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    self.filename = data.decode()

                print('Received filenames:', self.filename)

    def connect_to_peer(self):
        self.receive_filenames()
        self.receive_file()

    def broadcast_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            start_time = time.time()
            while time.time() - start_time <= 5:
                s.sendto(self.my_ip.encode(),
                         ('<broadcast>', self.broadcast_port))
                print(f"Broadcast message sent: {self.username}({self.my_ip})")
                time.sleep(1)

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
        finally:
            s.close()
        return local_ip
