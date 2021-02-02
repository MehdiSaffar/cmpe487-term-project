import socket
import time
import sys

HOST = sys.argv[1]  # The server's hostname or IP address
PORT = 5000        # The port used by the server

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'Hello, world')
    time.sleep(1)