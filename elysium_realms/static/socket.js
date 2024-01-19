const socket = io.connect(`http://${location.hostname}:${location.port}/`); // initiate socket

socket.on("response", function (data) {
  console.log("Server response:", data);
});

function mine() {
  console.log('Mine')
  socket.emit("mine", { data: document.cookie }, function (response) {
    console.log("Acknowledgement from server:", response);
  });
}

function attack() {
  console.log('Attack')
  socket.emit("attack", { data: document.cookie }, function (response) {
    console.log("Acknowledgement from server:", response);
  });
}

function train() {
  console.log('Train')
  socket.emit("train", { data: document.cookie }, function (response) {
    console.log("Acknowledgement from server:", response);
  });
}