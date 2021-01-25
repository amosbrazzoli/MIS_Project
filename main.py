from MisProject.socketTCP.socket_server import socket_loop
from MisProject.serial_reader import serial_loop
from MisProject.arduino import MIS_Arduino
from MisProject.OSCserver import osc_loop

from threading import Thread, Lock

arduino = MIS_Arduino("/dev/ttyACM1", 11520)
teensy = MIS_Arduino("/dev/ttyACM0", 11520)
teensylock = Lock()
lockduino = Lock()


t_serial_teensy = Thread(target=serial_loop, args=(teensy, teensylock, True, False))
t_serial_arduino = Thread(target=serial_loop, args=(arduino, lockduino, False, True))
t_socket = Thread(target=socket_loop, args=(arduino, teensy, lockduino, teensylock))
t_osc = Thread(target=osc_loop, args=(arduino, teensy, lockduino, teensylock))

t_serial_teensy.start()
t_serial_arduino.start()
t_socket.start()
t_osc.start()

t_serial_teensy.join()
t_serial_arduino.join()
t_socket.join()
t_osc.join()






