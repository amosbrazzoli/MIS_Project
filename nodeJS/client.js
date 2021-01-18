const io = require('socket.io-client');
const sleep = (milliseconds) => {
    return new Promise(resolve => setTimeout(resolve, milliseconds))
  }
const socket = io('http://localhost:5000');

// client-side
socket.on("connect", () => {
    console.log(socket.id); // x8WIv7-mJelg7on_ALbx
});

socket.on("connect", () => {
    console.log(socket.connected); // true
});

socket.on("disconnect", () => {
    console.log(socket.id); // undefined
});

socket.on("disconnect", () => {
    console.log(socket.connected); // false
});

socket.on("status", (data) => {
    //console.log(data)
});


socket.emit("command", {"fan": [
    Math.floor(Math.random() * 6),
    Math.floor(Math.random() * 2)]
});
