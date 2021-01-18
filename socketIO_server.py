import eventlet
import socketio

from arduino import MIS_Arduino
from threading import Lock
from time import sleep
import json

arduino = MIS_Arduino("/dev/ttyACM0", 11520)
lockduino = Lock()

sio = socketio.Server(async_mode='eventlet')
                        
app = socketio.WSGIApp(sio)

def send_reading(sid):
    while True:
        if arduino.sent == False:
            with lockduino:
                msg = arduino.state_dict()
            sio.emit("status", msg, to=sid)
            #print("SENT: ", msg)
        eventlet.sleep(0)


@sio.event
def connect(sid, environ):
    print('CONNECTED: ', sid)
    return True

@sio.event
def diconnect(sid):
    print('DISCONNECTED: ', sid)

@sio.event
def command(sid, data):
    with lockduino:
        arduino.command(data)
    print("COMMANDED: ", data)

@sio.on('connect')
def sensor_start(sid, environ):
    sio.start_background_task(send_reading, sid)


if __name__ == "__main__":
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
    print("STARTED")