## Description:
A simple CLI to share files over the local network.<br />
This project uses Socket Programming concepts to implement a peer to peer connection to transfer files.<br />
There is no server involved.<br />
The Project invlolves usage of broadcasting for peer discovery and usage of TCP to send file as a binary stream. <br />
Two TCP handshakes are performed, one to send all the filenames involved, the other to send the binary data.

## Languages and Frameworks
  - **Language Used**: Python
  - **Libraries Used**:
    - **_Socket_**: A library in Python to create web sockets.
    - **_SSL_**: A library in Python to implement SSL encryption and certification.
    - **_Threading_**: Library in Python which helps in creation of threads.
    - **_Time_**: Python library to access time.

## Usage:
- Clone the project into your system:
  ```
  
    $git clone https://github.com/mana-sg/ShareItClone
  
  ```
  
- Jump into the git repository.
  ```

    $cd ShareItClone

  ```
  
- Run the ```main.py``` file:
  ```

    $python3 main.py
  
  ```

- Now that the code is running, you can select whether you want to receive or send files.
- If you select receive, you have to wait untill the sender connects to your connection.
- If you selected send, you will see a window with all the peer names, select the peer which you want to send the file to.
- Once you select the peer, a file dialog will open up, select the file which you want to send.
- The file will be sent succesfully.
