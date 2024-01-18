const socket = io.connect(`http://${location.hostname}:${location.port}/`); // initiate socket

socket.on("response", function (data) {
  console.log("Server response:", data);
});

socket.emit("message", { data: "Hello, server!" }, function (response) {
  console.log("Acknowledgement from server:", response);
});
