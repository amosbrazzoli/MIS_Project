from MisProject.serial_reader import serial_loop
from MisProject.OSCserver import osc_loop
from MisProject.arduino import MIS_Arduino
from threading import Thread, Lock

import eventlet
import socketio
import json

# create the arduino object and lock
arduino = MIS_Arduino("/dev/ttyACM0", 11520)
lockduino = Lock()

# creates the socket.IO and relative server
sio = socketio.Server(async_mode='eventlet')                 
app = socketio.WSGIApp(sio)

def send_reading():
    ' helper function to keep sending data over the socket.io '
    while True:
        if arduino.sent == False:
            with lockduino:
                msg = arduino.state_dict()
            sio.emit("status", msg, to=sid)
            #print("SENT: ", msg)
        eventlet.sleep(0)

# connection event
@sio.event
def connect(sid, environ):
    print('CONNECTED: ', sid)
    return True

# disconnection event
@sio.event
def diconnect(sid):
    print('DISCONNECTED: ', sid)

# command event
@sio.event
def command(sid, data):
    with lockduino:
        arduino.command(data)
    print("COMMANDED: ", data)

# upon connection tigger the send_reading helper function
@sio.on('connect')
def sensor_start(sid, environ):
    sio.start_background_task(send_reading, sid)
    

t_serial = Thread(target=serial_loop, args=(arduino, lockduino))
t_osc = Thread(target=osc_loop, args=(arduino, lockduino))

# start serial read thread
t_serial.start()
print("SERIAL STARTED")

# start the OSC thread
t_osc.start()
print("OPEN SOUND CONTROL STARTED")

# start the socket.io server
print("WSGI STARTED")
eventlet.wsgi.server(eventlet.listen(('', 5000)), app, log_output=False)

t_serial. join()
t_osc.join()







