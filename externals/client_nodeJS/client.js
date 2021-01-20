const io = require('socket.io-client');

const socket = io('http://localhost:5000');


// Service Handles
socket.on("connect", () => {
    console.log("CONNECTED: ")
    console.log(socket.id)
    console.log(socket.connected);
});

    

socket.on("disconnect", () => {
    console.log("DISCONNECTED")
    console.log(socket.id);
    console.log(socket.connected);
});

// gets the status of the Arduino,
// which is provided constantly by the server
socket.on("status", (data) => {
    console.log(data)
});

// emitts {"fan": intPIN, "state": 0/1]}
socket.emit("command", 
    {
        "fan": Math.floor(Math.random() * 6),
        "state": Math.floor(Math.random() * 2)
    }
);

// emitts { "yaw": floatDir }
socket.emit("command", 
    {
        "yaw": Math.random() * 360
    }
);


// emitts { "id": intID, "value" 0/1] }
socket.emit("command", 
    {
        "id": Math.floor(Math.random() * 6),
        "value": Math.floor(Math.random() * 2)
    }
);
