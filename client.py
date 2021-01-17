import socket, queue, select, sys
from time import time, sleep

"""
999:MESSAGE
"""



to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
to_server.connect(('localhost', 50000))

inputs = [to_server]
outputs = [to_server]
command_queue = queue.Queue()

HEADER_LEN = 5
SENSOR_LEN = 506
COMMAND_LEN = 250
MESSAGE = '{ "time": ulongT, "HR": floatHR }'

while True:
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    for s in readable:
        if s == to_server:
            data = s. recv(COMMAND_LEN + HEADER_LEN + 1)
            if not data: break
            print(data)
    
    for s in writable:
        if s == to_server:
            msg =  f"{len(MESSAGE):>{HEADER_LEN}}:" + f"{MESSAGE:<{SENSOR_LEN}}"
            s.send(bytes(msg, 'utf8'))

    
    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        print(f"REMOVED: {s}")
        s.close()

