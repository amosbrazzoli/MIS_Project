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

// emitts {"fan": [intPIN, 0/1]}
socket.emit("command", {"fan": [
    Math.floor(Math.random() * 6),
    Math.floor(Math.random() * 2)]
});

// emitts {"wind": [intPIN, floatDir]}
socket.emit("command", {"fan": 
    Math.random() * 360
});


// emitts {"texture": [intID, 0/1]}
socket.emit("command", {"texture": [
    Math.floor(Math.random() * 6),
    Math.floor(Math.random() * 2)]
});
