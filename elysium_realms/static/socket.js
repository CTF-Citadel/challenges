// load html components
const healthFill = document.getElementById("healthFill");
const staminaFill = document.getElementById("staminaFill");
const current_place = document.getElementById('current_place');

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

// Get stat updates every second
setInterval(update_stats, 1000);

function update_stats() {
  socket.emit("stats", {}, function (response) {
    update_health(response.health);
    update_stamina(response.stamina);
  });
}

// function to collect items
function collect() {
  socket.emit("collect", {}, function (response) {
    update_stamina(response.stamina);
  });
}

// function to hunt enemies
function hunt() {
  socket.emit("hunt", {}, function (response) {
    update_health(response.health)
    update_stamina(response.stamina);
  });
}

// function to train character
function train() {
  socket.emit("train", {}, function (response) {
    update_stamina(response.stamina);
  });
}

// function to travel to another place
function travel() {
  socket.emit("travel", {}, function (response) {
    update_place(response.next_place);
  });
}

// function to update health bar
function update_health(value) {
  healthFill.style.width = `${value}%`;
}

// function to update stamina bar
function update_stamina(value) {
  staminaFill.style.width = `${value}%`;
}

// function to update UI after travelling
function update_place(place) {
  current_place.textContent = place;
}