import socketio
from time import sleep
from random import randint
import json

sio = socketio.Client(logger=True, engineio_logger=True)

def random_message():
    value = randint(2, 5)
    state = randint(0, 1)
    return json.dumps({"fan" : [value, state]})

def command_loop():
    while True:
        data = random_message()
        sio.emit("command", data)
        #print("COMMANDED: ", data)
        sleep(0.3)


@sio.event
def connect():
    sio.start_background_task(command_loop)
    print('CONNECTED')

@sio.event
def connect_error():
    print("CONNECT ERROR")

@sio.event
def status(sid, data):
    #print('GOT: ', data)
    
@sio.event
def disconnect():
    print('DISCONNECTED')

sio.connect('http://localhost:5000')
sio.wait()