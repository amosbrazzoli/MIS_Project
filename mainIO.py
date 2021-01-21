from MisProject.serial_reader import serial_loop
from MisProject.OSCserver import osc_loop
from MisProject.arduino import MIS_Arduino
from threading import Thread, Lock

import eventlet
import socketio

# create the arduino object and lock
arduino = MIS_Arduino("/dev/ttyACM0", 11520)
lockduino = Lock()

static_files = {
    '/': './public/index.html',
    '/jquery.js': './public/jquery.js',
    '/socket.io.js': './public/socket.io.js',
}

# creates the socket.IO and relative server
sio = socketio.Server(async_mode='eventlet')                 
app = socketio.WSGIApp(sio, static_files=static_files)

def send_reading(sid):
    ' helper function to keep sending data over the socket.io '
    while True:
        if arduino.sent == False:
            with lockduino:
                msg = arduino.state_dict()
            sio.emit("sensorWalk", msg, to=sid)
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

# fan command event
@sio.event
def fan(sid, data):
    with lockduino:
        arduino.fan_command(data)
    print("COMMANDED: ", data)

# wind command event
@sio.event
def wind(sid, data):
    with lockduino:
        arduino.wind_command(data)
    print("WIND COMMANDED: ", data)

# texture command event
@sio.event
def walkingMat(sid, data):
    with lockduino:
        arduino.texture_command(data)
    print("WIND COMMANDED: ", data)

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
eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app, log_output=False)

t_serial. join()
t_osc.join()







