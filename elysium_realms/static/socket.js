// load html components
const healthBar = document.getElementById("healthBar");
const healthFill = document.getElementById("healthFill");

// initiate socket connection
const socket = io.connect(`http://${location.hostname}:${location.port}/`); 

// get UUID from session cookie
const sessionToken = document.cookie.match(/session_token=([^;]+)/);
const uuid = sessionToken ? sessionToken[1] : null;

// Authenticate User when socket is established
socket.emit("auth", { data: uuid }, function (response) {
  if (response.status_code === 200) {
    console.log('Connection successfully established!');
  } else {
    console.log('Connection denied!');
  }
});

// Get default stats
socket.emit("stats", { data: document.cookie }, function (response) {
  update_health(response.health);
  console.log(response);
});

// function to collect items
function collect() {
  socket.emit("collect", { data: document.cookie }, function (response) {
    console.log(response);
  });
}

// function to hunt enemies
function hunt() {
  socket.emit("hunt", { data: document.cookie }, function (response) {
    update_health(response.health)
    console.log(response);
  });
}

// function to train character
function train() {
  socket.emit("train", { data: document.cookie }, function (response) {
    console.log(response);
  });
}

// function to update health bar
function update_health(value) {
  healthFill.style.width = `${value}%`;
}
