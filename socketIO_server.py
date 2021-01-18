import eventlet
import socketio

from arduino import MIS_Arduino
from threading import Lock

sio = socketio.Server(logger=True, engineio_logger=True)
app = socketio.WSGIApp(sio)

arduino = MIS_Arduino("/dev/ttyACM0", 11520)
lockduino = Lock()

def send_reading():
    while True:
        if arduino.sent == False:
            #with lockduino:
            msg = arduino.state_dict()
            sio.emit("status", msg)
            print("SENT: ", msg)


@sio.event
def connect(sid, environ):
    sio.start_background_task(send_reading)
    print('CONNECTED: ', sid)

@sio.event
def diconnect(sid):
    print('DISCONNECTED: ', sid)

@sio.event
def command(sid, data):
    #with lockduino:
    arduino.command(data)
    #print("COMMANDED: ", data)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)