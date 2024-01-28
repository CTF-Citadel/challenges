// load html components
const healthFill = document.getElementById("healthFill");
const staminaFill = document.getElementById("staminaFill");
const img_display = document.getElementById('img_display');
const error_msg = document.getElementById('error_msg');
const leaderboardPopup = document.getElementById('leaderboard');
const menuPopup = document.getElementById('menu');
const inventoryPopup = document.getElementById('inventory');
const healthStat = document.getElementById('healthStat');
const staminaStat = document.getElementById('staminaStat');

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

// Start interval to update player stats every second
setInterval(update_stats, 1000);

// function for stat updates
function update_stats() {
  socket.emit("stats", {}, function (response) {
    update_health(response.health);
    update_stamina(response.stamina);
  });
}

// function to collect items
function collect() {
  socket.emit("collect", {}, function (response) {
    if (response.error) {
      show_error(response.error)
    } else {
      update_stamina(response.stamina);
    }
  });
}

// function to hunt enemies
function hunt() {
  socket.emit("hunt", {}, function (response) {
    if (response.error) {
      show_error(response.error)
    } else {
      update_health(response.health)
      update_stamina(response.stamina);
    }
  });
}

// function to train character
function train() {
  socket.emit("train", {}, function (response) {
    if (response.error) {
      show_error(response.error)
    } else {
      update_stamina(response.stamina);
    }
  });
}

// function to travel to another place
function travel(direction) {
  socket.emit("travel", { data: direction }, function (response) {
    if (response.error) {
      show_error(response.error);
    } else {
      // update_place(response.next_place);
      update_img(response.img_url);
    }
  });
}

// function to update health bar
function update_health(value) {
  healthFill.style.width = `${value}%`;
  healthStat.innerText = `${value}/100`;
}

// function to update stamina bar
function update_stamina(value) {
  staminaFill.style.width = `${value}%`;
  staminaStat.innerText = `${value}/100`;
}

// function to update image
function update_img(url) {
  img_display.setAttribute('src', url);
}

// function to display error_msg
function show_error(error) {
  error_msg.innerText = error;
  error_msg.style.opacity = 1;

  // Interval to make an effect with opacity fading out
  setTimeout(() => {
    error_msg.style.opacity = 0;
  }, 2000);
}

// Function for Leaderboard-Popup
function leaderboard() {
  console.log(leaderboardPopup.style.display)
  if (leaderboardPopup.style.visibility == 'hidden') {
    leaderboardPopup.style.visibility = 'visible';
  } else {
    leaderboardPopup.style.visibility = 'hidden';
  }
}

// Function for Menu-Popup
function menu() {
  console.log(leaderboardPopup.style.display)
  if (leaderboardPopup.style.visibility == 'hidden') {
    leaderboardPopup.style.visibility = 'visible';
  } else {
    leaderboardPopup.style.visibility = 'hidden';
  }
}

// Function for Inventory-Popup
function inventory() {
  console.log(leaderboardPopup.style.display)
  if (leaderboardPopup.style.visibility == 'hidden') {
    leaderboardPopup.style.visibility = 'visible';
  } else {
    leaderboardPopup.style.visibility = 'hidden';
  }
}

// function for check on 1 popup appearance
function popup(popup) {
  if (popup === 'leaderboard') {
    leaderboardPopup.style.visibility = leaderboardPopup.style.visibility === 'visible' ? 'hidden' : 'visible';
    menuPopup.style.visibility = 'hidden';
    inventoryPopup.style.visibility = 'hidden';
  } else if (popup === 'menu') {
    leaderboardPopup.style.visibility = 'hidden';
    menuPopup.style.visibility = menuPopup.style.visibility === 'visible' ? 'hidden' : 'visible';
    inventoryPopup.style.visibility = 'hidden';
  } else {
    leaderboardPopup.style.visibility = 'hidden';
    menuPopup.style.visibility = 'hidden';
    inventoryPopup.style.visibility = inventoryPopup.style.visibility === 'visible' ? 'hidden' : 'visible';
  }
}
