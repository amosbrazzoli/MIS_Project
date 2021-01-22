const app = require('express')();
const http = require('http').Server(app);
const io = require('socket.io')(http);
const util = require('util');
// const Audic = require("audic");
// var player = require("play-sound")(opts = {});
// const sound = require("sound-play");

const port = 5000;
const clients = [];	//track connected clients
// const snow = new Audic("snowtrim.mp3")

//Server Web Client
app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

app.get('/socket.io.js', function(req, res){
	res.sendFile(__dirname + '/socket.io.js');
});

app.get('/jquery.js', function(req, res){
	res.sendFile(__dirname + '/jquery.js');
});

//make one reference to event name so it can be easily renamed 
const chatEvent = "chatMessage";
const sensorCOM3 = "sensorWalk";
const windRecMSG = 'wind';

//start reading serial
// const serial = new SerialPort('COM3', {
//     baudRate: 115200
// })
// //parsing line of serial input
// const parser = serial.pipe(new Readline({ delimiter: '\r\n' }))


//When a client connects, bind each desired event to the client socket
io.on('connection', socket =>{
	//track connected clients via log
	clients.push(socket.id);
	//const clientConnectedMsg = 'User connected ' + util.inspect(socket.id) + ', total: ' + clients.length;
	//io.emit(chatEvent, true);
	console.log(clientConnectedMsg);
	io.emit("start", {})

	//track disconnected clients via log
	socket.on('disconnect', ()=>{
		clients.pop(socket.id);
		const clientDisconnectedMsg = 'User disconnected ' + util.inspect(socket.id) + ', total: ' + clients.length;
		io.emit(chatEvent, clientDisconnectedMsg);
		console.log(clientDisconnectedMsg);
	})

	//multicast received message from client
	socket.on(chatEvent, msg =>{
		const combinedMsg = socket.id.substring(0,4) + ': ' + msg;
		io.emit(chatEvent, combinedMsg);
		console.log('multicast: ' + combinedMsg);
	});

	//Receving wind message 
	socket.on(windRecMSG, msg => {
		console.log('Wind location is: --- '+msg)
	})

	socket.on('walkingMat', msg => {
		console.log('walking mat is: --- '+msg.toString())
	})

	socket.on(sensorCOM3, msg => {
		console.log('walking mat is: --- '+msg.toString())
	})
});


http.listen(port, () => {
    console.log('listening on *:' + port);
    
  });
// const snow = new Audic("snowtrim2.mp3");
// snow.load();
// var mySound = new Audio('snowtrim2.mp3');
// mySound.load();
// parser.on('data', (a) =>{
//     let mySTring = JSON.parse(a);
//             // player.kill();
//             console.log(a.toString());
// 			// console.log(mySTring.X,mySTring.Y,mySTring.Z)
//             io.emit(sensorCOM3,mySTring);
//           })
