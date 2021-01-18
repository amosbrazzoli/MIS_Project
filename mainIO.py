from serial_reader import serial_loop
from arduino import MIS_Arduino
from threading import Thread, Lock

import eventlet
import socketio
import json

sio = socketio.Server(async_mode='eventlet')
                            
app = socketio.WSGIApp(sio)

def send_reading():
    sleep(1)

    if arduino.sent == False:
        with lockduino:
            msg = arduino.state_dict()
        sio.emit("status", msg, broadcast=True)
        print("SENT: ", msg)


@sio.event
def connect(sid, environ):
    print('CONNECTED: ', sid)
    sio.start_background_task(send_reading)

@sio.event
def diconnect(sid):
    print('DISCONNECTED: ', sid)

@sio.event
def command(sid, data):
    data = json.loads(data)
    with lockduino:
        arduino.command(data)
    print("COMMANDED: ", data)

if __name__ == "__main__":
    arduino = MIS_Arduino("/dev/ttyACM0", 11520)
    lockduino = Lock()

    

    t_serial = Thread(target=serial_loop, args=(arduino, lockduino))

    t_serial.start()
    print("STARTED")
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app, log_output=False)

    t_serial. join()







