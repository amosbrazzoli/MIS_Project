from socket_server import socket_loop
from serial_reader import serial_loop
from arduino import MIS_Arduino

from threading import Thread, Lock

arduino = MIS_Arduino("/dev/ttyACM0", 11520)
lockduino = Lock()

t_serial = Thread(target=serial_loop, args=(arduino, lockduino))
t_socket = Thread(target=socket_loop, args=(arduino, lockduino))

t_serial.start()
t_socket.start()

t_serial. join()
t_socket.join()






