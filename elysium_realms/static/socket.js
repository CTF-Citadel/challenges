// load html components
const healthFill = document.getElementById("healthFill");
const staminaFill = document.getElementById("staminaFill");
const img_display = document.getElementById('img_display');
const error_msg = document.getElementById('error_msg');
const menuPopup = document.getElementById('menu');
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

// function for check on 1 popup appearance
function popup() {
  menuPopup.style.visibility = menuPopup.style.visibility === 'visible' ? 'hidden' : 'visible';
}

// Function to load leaderboard from backend
function loadLeaderboard() {
  socket.emit("leaderboard", function (response) {
    if (typeof response === 'string') {
      response = JSON.parse(response); 
    }
    createUserElements(response);
  })
}

function createUserElements(users) {
  let userListDiv = document.getElementById('display');

  let titleDiv = document.createElement('div');
  titleDiv.className = 'user-container';
  titleDiv.innerHTML = '<p>User:</p><p>Level:</p><p>Guild:</p>';
  userListDiv.appendChild(titleDiv);

  users.forEach(function(user) {
    let userDiv = document.createElement('div');
    userDiv.className = 'user-container';
    userDiv.innerHTML = `<p>${user.username}</p><p>${user.level}</p><p>${user.affiliation}</p>`;
    userListDiv.appendChild(userDiv);
  });
}

let styleElement = document.createElement('style');
styleElement.textContent = `
  .user-container {
    display: flex;
    flex-direction: row;
  }

  .user-container p {
    margin: 0;
    padding: 5px;
    border: 1px solid #ccc;
    flex: 1;
    text-align: center;
    letter-spacing: 1px;
  }`;
document.head.appendChild(styleElement);