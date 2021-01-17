import serial, json
from arduino import MIS_Arduino
from time import time
from random import randint
from threading import Thread, Lock

SERIAL_PATH = "COM5"
BAUD = 115200


arduino = MIS_Arduino("/dev/ttyACM0", 11520)
lockduino = Lock()

def random_message():
    value = randint(2, 6)
    state = randint(0,1)
    return {"fan" : [value, state]}

def serial_loop(arduino):
    connection = serial.Serial(arduino.serial,
                                arduino.baud)
                            
    i = 0
    t0 = time()

    #print(json.loads(message)["fan"])

    while True:
        #try:
        i +=1
        incoming = connection.readline()

        # Almos allways the first json is incomplete
        try:
            incoming = json.loads(incoming)
        except:
            print(incoming)
            continue
        
        with lockduino:
            arduino.read_update(incoming)
            state = arduino.state_dict()
        #print(state)
        #except:
            #print(i/(time()-t0), ":", incoming)

if __name__ == "__main__":
    arduino = MIS_Arduino("/dev/ttyACM0", 11520)
    lockduino = Lock()

    t_serial = Thread(target=serial_loop, args=(arduino, ))

    t_serial.start()

    t_serial. join()