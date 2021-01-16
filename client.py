import socket
from time import time, sleep

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('localhost', 50000))
    t0 = time()

    while True:
        s.sendall(b'''{"fan": [intID, boolActive], "txt": intTxId}''')
        t0 = time()
        print("Sent")
        
        data = s.recv(1024)
        print(f"GOT: {data}")
