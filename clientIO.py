import socketio

from time import sleep
from random import randint
import json

sio = socketio.Client()



def command_loop():
    def random_message():
        value = randint(2, 5)
        state = randint(0, 1)
        return json.dumps({"fan" : [value, state]})
    data = random_message()
    sio.emit("command", data)
    print("COMMANDED: ", data)


@sio.event
def connect():
    sio.start_background_task(command_loop)
    print('CONNECTED')
    

@sio.event
def connect_error():
    print("CONNECT ERROR")

@sio.event
def status(data):
    print('GOT: ', data)
    
@sio.event
def disconnect():
    print('DISCONNECTED')

sio.connect('http://localhost:5000')

sio.wait()