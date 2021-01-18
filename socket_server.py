import select, socket, queue, json
from arduino import MIS_Arduino
from threading import Thread, Lock



def socket_loop(arduino):
    HEADER_LEN = 5
    SENSOR_LEN = 506
    COMMAND_LEN = 250

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setblocking(False)
    client.bind(('192.168.1.79', 50001))
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
                print(f"ACCEPTED: {client_address}")
                connection.setblocking(False)
                # set the connection in the inputs
                inputs.append(connection)
                # generate a connection queue fot the new connection
                message_queues[connection] = queue.Queue()

            # if the socket is not this client
            else:
                # read 1024 bytes of data
                data = s.recv(COMMAND_LEN + HEADER_LEN + 1)
                if data:
                    # commands a variation in the arduino
                    print(f"GOT: {data}")
                    data = json.loads(data)
                    with lockduino:
                        arduino.command(data)
                    # push the data connection queue
                    ## message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)
                    
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writable:
            with lockduino:
                MESSAGE = arduino.state_dict()
            MESSAGE = json.dumps(MESSAGE)
            print("SENT")
            msg =  f"{len(MESSAGE):>{HEADER_LEN}}:" + f"{MESSAGE:<{SENSOR_LEN}}"
            s.send(bytes(msg, 'utf8'))
        
        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]
                    
if __name__ == "__main__":
    arduino = MIS_Arduino("/dev/ttyACM0", 11520)
    lockduino = Lock()

    t_socket = Thread(target=socket_loop, args=(arduino,))

    t_socket.start()


    t_socket.join()