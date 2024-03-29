import socket
import time
import ssl
import threading


class Receiver(threading.Thread):
    def __init__(self, username):
        super().__init__()
        self.my_ip = self.get_local_ip()
        self.broadcast_port = 12345
        self.peer_port = [12333, 6666]
        self.filename = []
        self.username = username
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def receive_file(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(
            'certificates/shareit.crt', 'certificates/shareit.key')
        for file in self.filename:
            print(file)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((self.my_ip, self.peer_port[1]))
                server_socket.listen(1)
                print("Server is listening on port",
                      self.peer_port[1])
                with context.wrap_socket(server_socket, server_side=True) as ssock:
                    conn, addr = ssock.accept()
                    print("Connection established.")
                    with open(file, 'wb') as f:
                        while True:
                            data = conn.recv(1048576)
                            if not data:
                                break
                            f.write(data)
                    print("File received successfully")

    def receive_filenames(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(
            'certificates//shareit.crt', 'certificates/shareit.key')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.my_ip, self.peer_port[0]))
            s.listen()
            print('Waiting for a connection...')
            with context.wrap_socket(s, server_side=True) as ssock:
                conn, addr = ssock.accept()
                with conn:
                    print('Connected established.')
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        self.filename.append(data.decode())

                    print('Received filename:', self.filename)

    def connect_to_peer(self):
        self.receive_filenames()
        self.receive_file()

    def broadcast_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while not self._stop_event.is_set():
                s.sendto(self.username.encode(),
                         ('<broadcast>', self.broadcast_port))
                time.sleep(1)

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
        finally:
            s.close()
        return local_ip
