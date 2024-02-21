import socket


def send_file(filename, server_ip, server_port):
    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Connect the socket to the server
        client_socket.connect((server_ip, server_port))

        # Open the file to be sent
        with open(filename, 'rb') as f:
            # Read data from the file and send it
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)

        print("File sent successfully")


# Example usage:
send_file("/Users/manas/Desktop/JESUS.jpg", "192.168.144.157", 12333)
