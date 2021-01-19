Messages:

INCOMING TO THE VR HEADSET FROM THE RASPBERRY

UTF-8

5 byte header - message length
1 byte ":"
506 byte of serialised JSON Object

b'   33:{ "time": ulongT, "HR": floatHR }



                                                                                               '
JSON SAMPLE

{
    "HR": floatHR,
    "lSteps": ulongLeftStepsCount,
    "rSteps": ulongRightStepsCount,
    "IMU": [floatX, floatY, floatZ, ...]
}

================================================================

OUTGOING MESSAGE FROM THE VR HEADSET TO THE RASPBERRY

5 byte header - message length
1 byte ":"
250 byte of serialised JSON Object

b'   30:{ "fan": [intID, boolActive] }

                                              '

JSON SAMPLE

{
    "fan": [intID, boolActive],
    "texture": intTextureID
}