from MisProject.TCPsocket.socket_server import socket_loop
from MisProject.serial_reader import serial_loop
from MisProject.arduino import MIS_Arduino
from MisProject.OSCserver import osc_loop

from threading import Thread, Lock

arduino = MIS_Arduino("/dev/ttyACM0", 11520)
lockduino = Lock()

t_serial = Thread(target=serial_loop, args=(arduino, lockduino))
t_socket = Thread(target=socket_loop, args=(arduino, lockduino))
t_osc = Thread(target=osc_loop, args=(arduino, lockduino))

t_serial.start()
t_socket.start()
t_osc.start()

t_serial. join()
t_socket.join()
t_osc.join()






