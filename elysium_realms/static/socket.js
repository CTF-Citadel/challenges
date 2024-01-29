// load html components
const healthFill = document.getElementById("healthFill");
const staminaFill = document.getElementById("staminaFill");
const img_display = document.getElementById('img_display');
const error_msg = document.getElementById('error_msg');
const menuPopup = document.getElementById('menu');
const healthStat = document.getElementById('healthStat');
const staminaStat = document.getElementById('staminaStat');
const display = document.getElementById('display');

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

function loadLeaderboard() {
  clearDisplay();

  // Function to handle guild button click
  function handleGuildButtonClick() {
    clearDisplay();
    loadLeaderboard();
    socket.emit("leaderboard", { data: 'guilds'}, function (response) {
      console.log(response)
      if (typeof response === 'string') {
        response = JSON.parse(response); 
        createUserElements(response, 'Guild', 'Level', 'Member-Count');
        updateFlexStyles(1.5, 0.5, 1);
      } else {
        console.log(response)
      }
    });
  }
  
  // Function to handle users button click
  function handleUsersButtonClick() {
    clearDisplay();
    loadLeaderboard();
    socket.emit("leaderboard", { data: 'users'}, function (response) {
      if (typeof response === 'string') {
        response = JSON.parse(response); 
        createUserElements(response, 'User', 'Level', 'Guild');
        updateFlexStyles(1, 0.5, 1.5);
      } else {
        console.log(response)
      }
    });
  }
  
  // Create buttons and attach event listeners
  let guildButton = document.createElement('button');
  guildButton.textContent = 'Guild';
  guildButton.classList.add('fetchButton');
  guildButton.addEventListener('click', handleGuildButtonClick);
  
  let usersButton = document.createElement('button');
  usersButton.textContent = 'Users';
  usersButton.classList.add('fetchButton');
  usersButton.addEventListener('click', handleUsersButtonClick);    

  // Append buttons to the display element
  let buttonContainer = document.createElement('div');
  buttonContainer.appendChild(guildButton);
  buttonContainer.appendChild(usersButton);
  display.insertBefore(buttonContainer, display.firstChild);
}

// Function to load marketplace
function loadMarketplace() {
  clearDisplay();
}

// Function to 
function loadTransfer() {
  clearDisplay();
}

// Function to 
function loadGuide() {
  clearDisplay();
}

// Function to 
function loadInventory() {
  clearDisplay();
}

// function to clear display board
function clearDisplay() {
  let display = document.getElementById('display');
  display.innerHTML = ''; 
}

// function to render fetched content
function createUserElements(users, header1, header2, header3) {
  let titleDiv = document.createElement('div');
  titleDiv.className = 'user-container';
  titleDiv.innerHTML = `<p>${header1}</p><p>${header2}</p><p>${header3}</p>`;
  titleDiv.style.fontWeight = '900';
  display.appendChild(titleDiv);

  users.forEach(function(user) {
    let userDiv = document.createElement('div');
    userDiv.className = 'user-container';
    userDiv.innerHTML = `<p>${user.column1}</p><p>${user.column2}</p><p>${user.column3}</p>`;
    display.appendChild(userDiv);
  });
}

// Function to dynamically update table structure
function updateFlexStyles(flex1, flex2, flex3) {
  let userContainers = document.querySelectorAll('.user-container');

  userContainers.forEach(userContainer => {
      let paragraphs = userContainer.querySelectorAll('p');

      paragraphs.forEach((paragraph, index) => {
          switch (index) {
              case 0:
                  paragraph.style.flex = flex1;
                  break;
              case 1:
                  paragraph.style.flex = flex2;
                  break;
              case 2:
                  paragraph.style.flex = flex3;
                  break;
              default:
                  break;
          }
      });
  });
}