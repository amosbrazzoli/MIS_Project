from pythonosc.udp_client import SimpleUDPClient


from time import sleep
from random import randint


'''
Actions
0: silent
1: landing
2: rising
'''


IP = "127.0.0.1"
PORT = 9001

to_client = SimpleUDPClient(IP, PORT)



while True:
    TEXTURE_ID = randint(0, 6) #between several textures
    STEP_ACTION = randint(0, 2)

    to_client.send_message("/ino/step", STEP_ACTION)
    to_client.send_message("/ino/texture", TEXTURE_ID)