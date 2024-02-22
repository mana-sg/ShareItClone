import socket
import time
import tkinter as tk
from tkinter import filedialog

receivers = list()


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    return local_ip


def receive_broadcast(port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', port))

        print("Listening for broadcast messages...")

        start_time = time.time()
        while True and (time.time() - start_time <= 5):
            data, addr = s.recvfrom(1024)
            if (addr not in receivers):
                receivers.append(addr)
                print("Receivers list: ", receivers)

    client_index = int(input(
        "Enter index of whih person you want to send the file to: "))
    print("Sending file to: ", receivers[client_index])
    return receivers[client_index]


def broadcast_message(message, port):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        start_time = time.time()
        while time.time() - start_time <= 5:
            s.sendto(message.encode(), ('<broadcast>', port))
            print("Broadcast message sent:", message)
            time.sleep(1)


def connect_to_peer(filenames, peer_ip, peer_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((peer_ip, peer_port))
        with open(filenames, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.send(data)

        print(f"{filename} sent successfully")


def send_file_names(filenames, peer_ip, peer_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((peer_ip, peer_port))
        s.sendall(filename.encode())


def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


if __name__ == "__main__":
    my_ip = get_local_ip()
    port = 12345
    receiver_ip = receive_broadcast(port)
    # broadcast_message(receiver_ip[0], port)
    filepath = select_file()
    filename = filepath.split("/")[-1]
    print(filepath)
    send_file_names(filename, receiver_ip[0], 12333)
    time.sleep(3)
    connect_to_peer(filepath, receiver_ip[0], 6666)
