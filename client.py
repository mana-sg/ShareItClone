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
    # Create a UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', port))

        print("Listening for broadcast messages...")

        start_time = time.time()
        while True and (time.time() - start_time <= 5):
            data, addr = s.recvfrom(1024)
            # print("Received broadcast message from {}: {}".format(
            #     addr, data.decode()))
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


def connect_to_peer(filename, peer_ip, peer_port):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect the socket to the server
        client_socket.connect((peer_ip, peer_port))

        # Open the file to be sent
        with open(filename, 'rb') as f:
            # Read data from the file and send it
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)

        print("File sent successfully")


def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


if __name__ == "__main__":
    my_ip = get_local_ip()
    port = 12345
    receiver_ip = receive_broadcast(port)
    broadcast_message(receiver_ip[0], port)
    filepath = select_file()
    connect_to_peer(filepath, receiver_ip[0], 12333)
