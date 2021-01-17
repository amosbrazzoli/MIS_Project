import serial, json
from time import time
from random import randint

SERIAL_PATH = "COM5"
BAUD = 115200

def random_message():
    value = randint(2, 6)
    state = randint(0,1)
    return {"fan" : [value, state]}

connection = serial.Serial(SERIAL_PATH, BAUD)
i = 0
t0 = time()

#print(json.loads(message)["fan"])

while True:
    try:
        i +=1
        incoming = connection.readline()
        incoming = json.loads(incoming)
        print(incoming)
    except:
        print(i/(time()-t0), ":", incoming)
    

    if i % 100 == 0:
        message = random_message()
        message = json.dumps(message)
        print(i/(time()-t0), message)
        connection.write(bytes(message, "utf-8"))
    