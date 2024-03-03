from sender import Sender
from receiver import Receiver
import threading
import os


if __name__ == "__main__":
    os.system('clear')
    tag = '''
     _______. __    __       ___      .______       _______     __  .___________.
    /       ||  |  |  |     /   \     |   _  \     |   ____|   |  | |           |
   |   (----`|  |__|  |    /  ^  \    |  |_)  |    |  |__      |  | `---|  |----`
    \   \    |   __   |   /  /_\  \   |      /     |   __|     |  |     |  |     
.----)   |   |  |  |  |  /  _____  \  |  |\  \----.|  |____    |  |     |  |     
|_______/    |__|  |__| /__/     \__\ | _| `._____||_______|   |__|     |__|     
    '''

    print(tag)
    name = input("Enter your name: ")

    choice = int(input("Select 1 to send or 2 to receive file: "))
    if choice == 1:
        sender = Sender()
        listen_peers_thread = threading.Thread(target=sender.receive_broadcast)
        listen_peers_thread.start()

        sender.start_curses()
        print("Sending file to: ", sender.selected_receiver)

        listen_peers_thread.join()

        sender.select_file()
        sender.send_file_names()
        sender.create_file_threads()

    elif choice == 2:
        receiver = Receiver(name)
        connection_thread = threading.Thread(target=receiver.connect_to_peer)
        connection_thread.start()
        broadcast_thread = threading.Thread(target=receiver.broadcast_message)
        broadcast_thread.start()

        connection_thread.join()

        receiver.stop()
        broadcast_thread.join()
    else:
        print("Invalid choice")
