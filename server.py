import select, socket, sys, queue

HEADER_LEN = 5
SENSOR_LEN = 506
COMMAND_LEN = 250

MESSAGE = '{ "fan": [intID, boolActive] }'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setblocking(False)
client.bind(('localhost', 50000))
client.listen(5)
inputs = [client]
outputs = []
message_queues = {}

while inputs:
    # get all the connections
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # process readable sockets
    for s in readable:
        #  if the readable socket is this client
        # means that a new connection has arrived
        if s is client:
            # accept the connection
            connection, client_address = s.accept()
            connection.setblocking(False)
            # set the connection in the inputs
            inputs.append(connection)
            # generate a connection queue fot the new connection
            message_queues[connection] = queue.Queue()

        # if the socket is not this client
        else:
            # read 1024 bytes of data
            data = s.recv(SENSOR_LEN + HEADER_LEN + 1)
            if data:
                print(f"GOT: {data}")
                # push the data connection queue
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
                
            else:
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]

    for s in writable:
        msg =  f"{len(MESSAGE):>{HEADER_LEN}}:" + f"{MESSAGE:<{COMMAND_LEN}}"
        s.send(bytes(msg, 'utf8'))
    
    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]
                


conn, addr = s.accept()
while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.sendall(data)
conn.close()