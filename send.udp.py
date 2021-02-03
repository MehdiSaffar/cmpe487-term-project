
import socket
import time

data = "Hello UDP Server".encode()
addr = ("<broadcast>", 5000)
bufsize = 1024

# Create a UDP socket at client side
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        sock.sendto(data, addr)
        print(data)
        time.sleep(0.5)
