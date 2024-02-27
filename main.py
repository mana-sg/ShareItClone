from sender import Sender
from receiver import Receiver
import threading
# import os


if __name__ == "__main__":
    # if not os.path.exists('shareit.crt') and not os.path.exists('shareit.key'):
    #     os.system("openssl genrsa -out shareit.key 2048")
    #     os.system(
    #         "openssl req -new -key shareit.key -out shareit.csr -config openssl.cnf")
    #     os.system(
    #         "openssl x509 -in shareit.csr -out shareit.crt -req -signkey shareit.key -days 365")
    #
    name = input("Enter your name: ")

    choice = int(input("Select 1 to send or 2 to receive file: "))
    if choice == 1:
        sender = Sender()
        # while True:
        #     sender.receive_broadcast()
        #     if len(sender.receivers) == 0:
        #         choice = int(
        #             input("No receivers found. Press 1 to scan again or 2 to exit: "))
        #         if choice == 2:
        #             exit()
        #     else:
        #         indices = [i+1 for i in range(len(sender.peer_names))]
        #         print(tabulate(list(zip(indices, sender.peer_names)), headers=[
        #               "Index", "Peer Name"], tablefmt="pretty"))
        #         choice = input(
        #             "Press R to scan again or C to continue: ")
        #         if choice == "C" or choice == "c":
        #             break

        listen_peers_thread = threading.Thread(target=sender.receive_broadcast)
        listen_peers_thread.start()

        sender.start_curses()

        # print_thread = threading.Thread(target=sender.start_curses)
        #
        # while sender.selected_receiver == "":
        #     client_index = int(input(
        #         "Enter index of whih person you want to send the file to: "))-1
        #     if (len(sender.peer_names) == 0):
        #         print("No peers found, please wait while we are scanning!")
        #     elif client_index >= len(sender.peer_names) or client_index < 0:
        #         print("Invalid index")
        #     else:
        #         break
        #

        print("Sending file to: ", sender.selected_receiver)
        listen_peers_thread.join()

        sender.select_file()
        sender.send_file_names()
        sender.connect_to_peer()

    elif choice == 2:
        receiver = Receiver(name)
        # while True:
        #     receiver.broadcast_message()
        #     choice = input("Enter Y to broadcast again or C to continue: ")
        #     if choice == "C" or choice == "c":
        #         break
        # receiver.connect_to_peer()
        #
        connection_thread = threading.Thread(target=receiver.connect_to_peer)
        connection_thread.start()
        broadcast_thread = threading.Thread(target=receiver.broadcast_message)
        broadcast_thread.start()

        connection_thread.join()

        receiver.stop()
        broadcast_thread.join()
    else:
        print("Invalid choice")
