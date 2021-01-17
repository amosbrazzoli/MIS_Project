import serial, json

SERIAL_PATH = "COM3"
BAUD = 115200

message = '"fan": [1, true]'

connection = serial.Serial(SERIAL_PATH, BAUD)
i = 0

print(json.loads(message)["fan"])
"""
while True:
    incoming = connection.readline()
    incoming = json.loads(incoming)
    print(incoming)

    i += 1
    if i % 20 == 0:
        connection.write(bytes(message, "utf-8"))

"""





