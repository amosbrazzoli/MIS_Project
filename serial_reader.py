import serial, json
from random import randint

SERIAL_PATH = "COM3"
BAUD = 115200

def random_message():
    value = randint(2, 6)
    state = randint(0,1)
    return {"fan" : [value, state]}

connection = serial.Serial(SERIAL_PATH, BAUD)
i = 0

#print(json.loads(message)["fan"])

while True:
    try:
        incoming = connection.readline()
        incoming = json.loads(incoming)
    except:
        print(incoming)
    

    i += 1
    if i % 20 == 0:
        message = random_message()
        message = json.dumps(message)
        print(message)
        connection.write(bytes(message, "utf-8"))
    