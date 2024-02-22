from .sender import Sender
from .receiver import Receiver


if __name__ == "__main__":
    print("Select 1 to send or 2 to receive file")
    choice = int(input())
    if choice == 1:
        sender = Sender("user1") 
        sender.receive_broadcast()
        sender.select_file()
        sender.send_file_names()
        sender.connect_to_peer()

    elif choice == 2:
        receiver = Receiver("user2")
        receiver.broadcast_message()
        receiver.connect_to_peer()
