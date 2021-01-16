import select, socket, sys, queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.bind(('localhost', 50000))
server.listen(5)
inputs = [server]
outputs = []
message_queues = {}

while inputs:
    # get all the connections
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # process readable sockets
    for s in readable:
        #  if the readable socket is this server
        # means that a new connection has arrived
        if s is server:
            # accept the connection
            connection, client_address = s.accept()
            connection.setblocking(False)
            # set the connection in the inputs
            inputs.append(connection)
            # generate a connection queue fot the new connection
            message_queues[connection] = queue.Queue()

        # if the socket is not this server
        else:
            # read 1024 bytes of data
            data = s.recv(1024)
            if data:
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
        try:
            next_message = message_queues[s].get_nowait()
        except queue.Empty:
            outputs.remove(s)
        else:
            s.send(next_message)
    
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