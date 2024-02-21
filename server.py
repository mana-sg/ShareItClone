import socket
import time
# import threading


def receive_file(filename, peer_ip, peer_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((peer_ip, peer_port))
        server_socket.listen(1)
        print("Server is listening on port", peer_port)
        conn, addr = server_socket.accept()
        print("Connection established with", addr)
        with open(filename, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
        print("File received successfully")


def connect_to_peer(peer_ip):
    print("I WANT YOUR FILE!!!")
    receive_file("JESUS.JPG", peer_ip, 12333)


def receive_broadcast(local_ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', port))
        print("Listening for broadcast messages...")

        while True:
            data, addr = s.recvfrom(1024)
            print("Received broadcast message from {}: {}".format(
                addr, data.decode()))
            if (data.decode() == local_ip):
                # threading.Thread(target=connect_to_peer, args=(local_ip)).start()
                connect_to_peer(local_ip)
                break


def broadcast_message(message, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        start_time = time.time()
        while time.time() - start_time <= 5:
            s.sendto(message.encode(), ('<broadcast>', port))
            print("Broadcast message sent:", message)
            time.sleep(1)


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip


if __name__ == "__main__":
    message = get_local_ip()
    port = 12345
    broadcast_message(message, port)
    receive_broadcast(message, port)
