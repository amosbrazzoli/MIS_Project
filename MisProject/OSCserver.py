from pythonosc.udp_client import SimpleUDPClient


from time import sleep
from random import randint


'''
Actions
0: silent
1: landing
2: rising
'''

def osc_loop(arduino, lockduino):
    IP = "127.0.0.1"
    PORT = 9001

    # Representation of the last received data
    status = {
                1 : False,
                2 : False,
                "txt" : None 
            }

    to_client = SimpleUDPClient(IP, PORT)

    while True:
        # Acquire lock on the Arduino Object
        with lockduino:
            # fetch data from the Arduino Object
            status1 = arduino.is_pressed[1]
            status2 = arduino.is_pressed[2]
            texture = arduino.texture

        # if texture is different
        if texture != status["text"]:
            to_client.send_message("/ino/texture", texture)
        
        # if 1 steps in
        if status1 == True and status[1] == False:
            to_client.send_message("/ino/step", [1, 1])
        # if 1 steps out
        elif status1 == False and status[1] == True:
            to_client.send_message("/ino/step", [2, 1])

        # if 2 steps in
        if status2 == True and status[2] == False:
            to_client.send_message("/ino/step", [1, 2])
        # if 2 steps out
        elif status2 == False and status[2] == True:
            to_client.send_message("/ino/step", [2, 2])

        # update last received data
        status[1] = status1
        status[2] = status2
        status["txt"] = texture




        
        