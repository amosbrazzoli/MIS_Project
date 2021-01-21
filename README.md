# MIS and Virtual Reality to Treat Acrophobia
Exam Requirement for the Multisensory Interactive Systems Course at the University of Trento by Prof. Luca Turchet

#### Contributors:
Amos Brazzoli
Omid Jadidi
Phiona Nambukenya
Federico Zuanni


### Repository Structure


```bash
MIS_Project
├── MisProject
│   ├── OSCserver.py			OSC server loop
│   ├── arduino.py				Arduino Shared Class
│   ├── serial_reader.py		Serial I/O loop
│   ├── socketIO				socket.io server and client
│   │   ├── clientIO.py
│   │   └── socketIO_server.py
│   ├── socketTCP				same as socket.io, just TCP
│   │   ├── client.py
│   │   └── socket_server.py
│   └── utils.py				utility functions and classes
├── Pipfile
├── Pipfile.lock
├── README.md
├── externals
│   ├── Pure_Data_Haptic		Pure data patch for haptic speakers
│   │   └── haptic_foot.pd
│   ├── Sensors
│   │   ├── SRTeensy
│   │   │   └── SRTeensy.ino	Arduino compatible code for sensors
│   │   └── libs				Various libs for expansions
│   │       ├── Queue.cpp
│   │       ├── Queue.h
│   │       ├── Time_Queue.cpp
│   │       ├── Time_Queue.h
│   │       └── test.cpp
│   └── client_nodeJS			A sample client in node.js for control
│       ├── client.js
│       └── package-lock.json
├── extras						Other documentation on the project
├── main.py						Main file using TCP socket
└── mainIO.py					Main file using socket.io
```

### Software Dependencies:
PureData:
    Help >> Find Externals >> mrpeach
Arduino:
    https://github.com/tttapa/Arduino-Filters
    Must be renamed as ´Filters´
Node.js:
	socket.io
Python:
	python-osc
	pyserial
	eventlet
	python-socketio

## Serial I/O

Output from the Arduino

```json
{
	"time"		: arduinoTime, 			// unsigned long
    "ECG"		: ECGread, 				// float 
    "lom"		: ECGlowerOutScope, 	// bool
    "lom"		: ECGupperOutScope, 	// bool
    "delta"		: dECG_over_dt, 		// float
    "pressure1" : analogReadPressure1, 	// int
    "pressure2" : analogReadPressure2, 	// int
    "x"			: IMUx, 				// float
    "y"			: IMUy, 				// float
    "z"			: IMUz, 				// float
}
```

Input to the Arduino

```json
{	"fan": [
            	fanPin,		// int
            	fanValue 	// bool
			]
}
```



## socket.io communication

Various possible commands given in the **socket.io** event `"command" : { }`. Be aware that `"id"` and `"valie"`, and `"fan"` and `"state"` must be issued present in the same json object to cause effects. 

```json
{
    "id" 	: textureID, 				// int
    "value" : textureValue, 			// bool
    "fan" 	: fanPin, 					// int
    "state"	: fanState, 				// bool
    "yaw"	: windDirection, 			// float [-360, 360]
}
```

The socket uses the python `Object.__dict__` dictionary as a source of information for the clients. Here is an example right after initialisation. The field keeping in mind the sensor readings should be mostly self explanatory

```json
{
    'HIGH_PRESSURE_THRESHOLD': 800, 
    'LOW_PRESSURE_THRESHOLD': 300, 
    'R_THRESHOLD': 620, 
    'serial': '/dev/ttyACM0', 
    'baud': 11520, 
    'last_read': 0, 
    'ECG': 0, 
    'lop': 0, 
    'lom': 0, 
    'delta': 0, 
    'last_beat': 0, 
    'BPM': 0, 
    'in_beat': False, 
    'ECG_Queue': <utils.ECG_Queue object at 0x7f3b0f4931f0>, 
    'pressure': {}, 
	'steps': {}, 
	'is_pressed': {},
	'x': 0,
	'y': 0,
	'z': 0,
	'texture': None,
	'relays': {},
	'sent': False,
	'windspan': functools.partial(<function area at 0x7f3b0f47f670>, 5),
	'shift': 1
}
```



## TCP socket

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