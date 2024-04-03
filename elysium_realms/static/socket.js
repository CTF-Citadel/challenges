// load html components
const healthFill = document.getElementById("healthFill");
const staminaFill = document.getElementById("staminaFill");
const img_display = document.getElementById('img_display');
const error_msg = document.getElementById('error_msg');
const result_msg = document.getElementById('result_msg');
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
  socket.emit("collect", function (response) {
    if (response.error) {
      show_error(response.error)
    } else {
      update_stamina(response.stamina);
      show_result('Collecting-Harvest: ',response.collected_material)
    }
  });
}

// function to hunt enemies
function hunt() {
  socket.emit("hunt", function (response) {
    if (response.error) {
      show_error(response.error)
    } else {
      update_health(response.health)
      update_stamina(response.stamina);
      show_result('Hunting-Harvest: ', response.hunted_material)
    }
  });
}

// function to train character
function train() {
  socket.emit("train", function (response) {
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

// function to fetch user credits
function getCredits() {
  return new Promise((resolve, reject) => {
    socket.emit("showCredits", function (response) {
      if (response.error) {
        console.log(response.error);
        reject("error");
      } else {
        try {
          const creditsObject = JSON.parse(response);
          const credits = creditsObject.credits;
          resolve(credits); // Resolve the Promise with the credits value
        } catch (error) {
          console.error("Error parsing response:", error);
          reject("error");
        }
      }
    });
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

function show_result(msg, result) {
  result_msg.innerText = `${msg} 1x ${result}`;
  result_msg.style.opacity = 1;

  // Interval to make an effect with opacity fading out
  setTimeout(() => {
    result_msg.style.opacity = 0;
  }, 2000); 
}

// function for check on 1 popup appearance
function popup() {
  menuPopup.style.visibility = menuPopup.style.visibility === 'visible' ? 'hidden' : 'visible';
}

// Function to load UI and fetch leaderboards
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
  buttonContainer.classList.add('subBtns')
  buttonContainer.style.height = '30px';
  display.insertBefore(buttonContainer, display.firstChild);
}

// Function to load transfer-page
function loadTransfer() {
  clearDisplay();

  // Declare currentCredits variable
  let currentCredits;

  // Call getCredits() and wait for the Promise to resolve
  getCredits()
    .then((credits) => {
      currentCredits = credits; // Assign credits to currentCredits

      // Use currentCredits here or call functions that depend on it
      if (currentCredits == 'error') {
        console.log("An error occured while fetching users' credits!");
      } else {
        function transfer() {
          if (confirmationText.value === 'CONFIRM') {
            error_msg.innerHTML = '';
            socket.emit("transfer", { target: transferTarget.value, amount: transferAmount.value }, function (response) {
              if (response.error) {
                error_msg.innerHTML = response.error;
              } else {
                // If transfer is successful, fetch updated credits
                getCredits()
                  .then((credits) => {
                    if (credits === 'error') {
                      console.log("An error occurred while fetching users' credits!");
                    } else {
                      currentCredits = credits;
                      creditCount.textContent = `Current Credits: ${currentCredits}`;
                      error_msg.innerHTML = response.success;
                    }
                  })
                  .catch((error) => {
                    console.error("Error:", error);
                  });
              }
            });
          } else {
            error_msg.innerHTML = "Please type 'CONFIRM' before transferring!";
          }
        }

        // Create credit count element
        let creditCount = document.createElement('h2');
        creditCount.textContent = `Current Credits: ${currentCredits}`;
        creditCount.classList.add('creditCount');

        let transferTargetLabel = document.createElement('h2');
        transferTargetLabel.textContent = 'User to transfer to';
        transferTargetLabel.classList.add('transferLabel');

        // input for user to transfer to 
        let transferTarget = document.createElement('input');
        transferTarget.classList.add('transferUser');

        let transferAmountLabel = document.createElement('h2');
        transferAmountLabel.textContent = 'Amount to transfer';
        transferAmountLabel.classList.add('transferLabel');

        // input for amount to transfer to another user
        let transferAmount = document.createElement('input');
        transferAmount.classList.add('transferAmount');

        let confirmationTextLabel = document.createElement('h2');
        confirmationTextLabel.textContent = 'Type CONFIRM to proceed with transfer!';
        confirmationTextLabel.classList.add('transferInput');

        // input for user to confirm transfer
        let confirmationText = document.createElement('input');
        confirmationText.classList.add('transferConfirm');

        // Create transfer button
        let transferBtn = document.createElement('button');
        transferBtn.textContent = 'Transfer Credits';
        transferBtn.classList.add('fetchButton');
        transferBtn.addEventListener('click', transfer);

        let error_msg = document.createElement('h2')
        error_msg.classList.add('errorMsgCreds');

        // Create container for credit count and transfer button
        let buttonContainer = document.createElement('div');
        buttonContainer.classList.add('transferWindow');
        buttonContainer.appendChild(creditCount);
        buttonContainer.appendChild(transferTargetLabel);
        buttonContainer.appendChild(transferTarget);
        buttonContainer.appendChild(transferAmountLabel);
        buttonContainer.appendChild(transferAmount);
        buttonContainer.appendChild(confirmationTextLabel);
        buttonContainer.appendChild(confirmationText);
        buttonContainer.appendChild(transferBtn);
        buttonContainer.appendChild(error_msg);

        // Insert button container into display
        display.insertBefore(buttonContainer, display.firstChild);
      }
    })
    .catch((error) => {
      // Handle error if getCredits() Promise rejects
      console.error("Error:", error);
    });
}

function createMarketItems(items, header1, header2, header3, header4) {
  items.forEach(function(user) {
    let userDiv = document.createElement('div');
    userDiv.className = 'item-container';

    // Create img element for the user's item
    let display_img = document.createElement('img');
    display_img.src = user.column1; // Assuming column1 contains the image URL
    display_img.alt = 'Item Image';
    display_img.style.width = 'calc(100% / 6)'; // Set width to 1/6 of the container width
    userDiv.appendChild(display_img);

    // Create div for column2 and column3
    let column23Div = document.createElement('div');
    column23Div.className = 'item-info';
    let column2 = document.createElement('p');
    column2.textContent = `${header1}: ${user.column2}`;
    column23Div.appendChild(column2);
    let column3 = document.createElement('p');
    column3.textContent = `${header2}: ${user.column3}`;
    column23Div.appendChild(column3);
    userDiv.appendChild(column23Div);

    // Create div for column4 and column5
    let column45Div = document.createElement('div');
    column45Div.className = 'item-info';
    let column4 = document.createElement('p');
    column4.textContent = `${header3}: ${user.column4}$`;
    column45Div.appendChild(column4);
    let column5 = document.createElement('p');
    column5.textContent = `${header4}: ${user.column5}`;
    column45Div.appendChild(column5);
    userDiv.appendChild(column45Div);

    // Create buy button
    let buyButton = document.createElement('button');
    buyButton.textContent = 'BUY';
    buyButton.addEventListener('click', function() {
      socket.emit('buy', { id: user.column6, type: 'item' }, function(response) {
        if (response.error) {
          alert(response.error);
        } else {
          alert(response.success);
        }
      });
    });
    userDiv.appendChild(buyButton);

    display.appendChild(userDiv);
  });
}

function createMarketTools(items, header1, header2, header3, header4, header5, header6) {
  items.forEach(function(user) {
    let userDiv = document.createElement('div');
    userDiv.className = 'item-container';

    // Create img element for the user's item
    let display_img = document.createElement('img');
    display_img.src = user.column1; // Assuming column1 contains the image URL
    display_img.alt = 'Item Image';
    display_img.style.width = 'calc(100% / 6)'; // Set width to 1/6 of the container width
    userDiv.appendChild(display_img);

    // Create div for the first set of headers (Tool-Name, Durability, Efficiency)
    let column123Div = document.createElement('div');
    column123Div.className = 'item-info';
    let column1 = document.createElement('p');
    column1.textContent = `${header1}: ${user.column2}`;
    column123Div.appendChild(column1);
    let column2 = document.createElement('p');
    column2.textContent = `${header2}: ${user.column3}/100`;
    column123Div.appendChild(column2);
    let column3 = document.createElement('p');
    column3.textContent = `${header3}: ${user.column4}`;
    column123Div.appendChild(column3);
    userDiv.appendChild(column123Div);

    // Create div for the second set of headers (Rank, Price, Seller)
    let column456Div = document.createElement('div');
    column456Div.className = 'item-info';
    let column4 = document.createElement('p');
    column4.textContent = `${header4}: ${user.column5}`;
    column456Div.appendChild(column4);
    let column5 = document.createElement('p');
    column5.textContent = `${header5}: ${user.column6}$`;
    column456Div.appendChild(column5);
    let column6 = document.createElement('p');
    column6.textContent = `${header6}: ${user.column7}`;
    column456Div.appendChild(column6);
    userDiv.appendChild(column456Div);

    // Create buy button
    let buyButton = document.createElement('button');
    buyButton.textContent = 'BUY';
    buyButton.addEventListener('click', function() {
      socket.emit('buy', { id: user.column8, type: 'tool' }, function(response) {
        if (response.error) {
          alert(response.error);
        } else {
          alert(response.success);
        }
      });
    });
    userDiv.appendChild(buyButton);

    display.appendChild(userDiv);
  });
}

function createMarketWeapons(items, header1, header2, header3, header4, header5, header6) {
  items.forEach(function(user, index) {
    if (index % 2 === 0) {
      // Create a new row for every even-indexed item
      var rowDiv = document.createElement('div');
      rowDiv.className = 'item-row';
      display.appendChild(rowDiv);
    }

    // Create a new item container for each weapon
    let userDiv = document.createElement('div');
    userDiv.className = 'item-container';

    // Create img element for the user's weapon
    let display_img = document.createElement('img');
    display_img.src = user.column1; // Assuming column1 contains the image URL
    display_img.alt = 'Weapon Image';
    display_img.style.width = 'calc(100% / 6)'; // Set width to 1/6 of the container width
    userDiv.appendChild(display_img);

    // Create div for the first set of headers (Weapon-Name, Damage, Attack-Speed)
    let column123Div = document.createElement('div');
    column123Div.className = 'item-info';
    let column1 = document.createElement('p');
    column1.textContent = `${header1}: ${user.column2}`;
    column123Div.appendChild(column1);
    let column2 = document.createElement('p');
    column2.textContent = `${header2}: ${user.column3}`;
    column123Div.appendChild(column2);
    let column3 = document.createElement('p');
    column3.textContent = `${header3}: ${user.column4}`;
    column123Div.appendChild(column3);
    userDiv.appendChild(column123Div);

    // Create div for the second set of headers (Durability, Rank, Price)
    let column456Div = document.createElement('div');
    column456Div.className = 'item-info';
    let column4 = document.createElement('p');
    column4.textContent = `${header4}: ${user.column5}`;
    column456Div.appendChild(column4);
    let column5 = document.createElement('p');
    column5.textContent = `${header5}: ${user.column6}`;
    column456Div.appendChild(column5);
    let column6 = document.createElement('p');
    column6.textContent = `${header6}: ${user.column7}$`;
    column456Div.appendChild(column6);
    userDiv.appendChild(column456Div);

    // Create buy button
    let buyButton = document.createElement('button');
    buyButton.textContent = 'BUY';
    buyButton.addEventListener('click', function() {
      socket.emit('buy', { id: user.column9, type: 'weapon' }, function(response) {
        if (response.error) {
          alert(response.error);
        } else {
          alert(response.success);
        }
      });
    });
    userDiv.appendChild(buyButton);

    // Append the item container to the appropriate row
    if (index % 2 === 0) {
      rowDiv.appendChild(userDiv);
    } else {
      let previousRow = display.lastElementChild;
      previousRow.appendChild(userDiv);
    }
  });
}

// Function to load marketplace
function loadMarketplace() {
  clearDisplay();

  // Function to handle guild button click
  function handleItemsButtonClick() {
    clearDisplay();
    loadMarketplace();
    socket.emit("marketPlace", { data: 'items' }, function (response) {
      console.log(response)
      if (typeof response === 'string') {
        response = JSON.parse(response); 
        createMarketItems(response, 'Item-Name', 'Quantity', 'Price', 'Seller');
      } else {
        console.log(response)
      }
    });
  }

  function handleToolsButtonClick() {
    clearDisplay();
    loadMarketplace();
    socket.emit("marketPlace", { data: 'tools' }, function (response) {
      console.log(response)
      if (typeof response === 'string') {
        response = JSON.parse(response); 
        createMarketTools(response, 'Tool-Name', 'Durability', 'Efficiency', 'Rank', 'Price', 'Seller');
      } else {
        console.log(response)
      }
    });
  }

  function handleWeaponsButtonClick() {
    clearDisplay();
    loadMarketplace();
    socket.emit("marketPlace", { data: 'weapons' }, function (response) {
      console.log(response)
      if (typeof response === 'string') {
        response = JSON.parse(response); 
        createMarketWeapons(response, 'Weapon-Name', 'Damage', 'Attack-Speed', 'Durability', 'Rank', 'Price', 'Seller');
      } else {
        console.log(response)
      }
    });
  }
  
  // Create buttons and attach event listeners
  let itemsButton = document.createElement('button');
  itemsButton.textContent = 'Items';
  itemsButton.classList.add('fetchButton');
  itemsButton.addEventListener('click', handleItemsButtonClick);
  
  let toolsButton = document.createElement('button');
  toolsButton.textContent = 'Tools';
  toolsButton.classList.add('fetchButton');
  toolsButton.addEventListener('click', handleToolsButtonClick);
  
  let weaponsButton = document.createElement('button');
  weaponsButton.textContent = 'Weapons';
  weaponsButton.classList.add('fetchButton');
  weaponsButton.addEventListener('click', handleWeaponsButtonClick);   

  // Append buttons to the display element
  let buttonContainer = document.createElement('div');
  buttonContainer.appendChild(itemsButton);
  buttonContainer.appendChild(toolsButton);
  buttonContainer.appendChild(weaponsButton);
  buttonContainer.classList.add('subBtns')
  buttonContainer.style.height = '30px';
  display.insertBefore(buttonContainer, display.firstChild);
}

// Function to 
function loadGuide() {
  clearDisplay();

  let infoMsg = document.createElement('h1');
  infoMsg.innerHTML = 'Coming Soon!';
  infoMsg.style.margin = '10px';

  let buttonContainer = document.createElement('div');
  buttonContainer.appendChild(infoMsg);
    
  display.insertBefore(buttonContainer, display.firstChild);
}

function createInventoryItems(items, header1, header2, header3) {
  items.forEach(function(user) {
    let userDiv = document.createElement('div');
    userDiv.className = 'item-container';
    userDiv.style.position = 'relative';

    // Create img element for the user's item
    let display_img = document.createElement('img');
    display_img.src = user.column1; // Assuming column1 contains the image URL
    display_img.alt = 'Item Image';
    display_img.style.width = 'calc(100% / 6)'; // Set width to 1/6 of the container width
    userDiv.appendChild(display_img);

    let columnDiv = document.createElement('div');
    columnDiv.className = 'item-info';
    
    let column2 = document.createElement('p');
    column2.textContent = `${header1}: ${user.column2}`; 
    columnDiv.appendChild(column2);

    let column3 = document.createElement('p');
    column3.textContent = `${header2}: ${user.column3}`; 
    columnDiv.appendChild(column3);
    
    let column5 = document.createElement('p');
    column5.textContent = `${header3}: ${user.column5}`; 
    columnDiv.appendChild(column5);

    userDiv.appendChild(columnDiv);

    display.appendChild(userDiv);
  });
}

function createInventoryTools(items, header1, header2, header3, header4, header5) {
  items.forEach(function(user) {
    let userDiv = document.createElement('div');
    userDiv.className = 'item-container';
    userDiv.style.position = 'relative';

    // Create img element for the user's item
    let display_img = document.createElement('img');
    display_img.src = user.column1; // Assuming column1 contains the image URL
    display_img.alt = 'Item Image';
    display_img.style.width = 'calc(100% / 6)'; // Set width to 1/6 of the container width
    userDiv.appendChild(display_img);

    let columnDiv1 = document.createElement('div');
    columnDiv1.className = 'item-info';
    
    let column2 = document.createElement('p');
    column2.textContent = `${header1}: ${user.column2}`; 
    columnDiv1.appendChild(column2);

    let column3 = document.createElement('p');
    column3.textContent = `${header2}: ${user.column3}`; 
    columnDiv1.appendChild(column3);
    
    let column4 = document.createElement('p');
    column4.textContent = `${header3}: ${user.column4}`; 
    columnDiv1.appendChild(column4);


    let columnDiv2 = document.createElement('div');
    columnDiv2.className = 'item-info';

    let column5 = document.createElement('p');
    column5.textContent = `${header4}: ${user.column5}`; 
    columnDiv2.appendChild(column5);

    let column6 = document.createElement('p');
    column6.textContent = `${header5}: ${user.column7}`; 
    columnDiv2.appendChild(column6);

    userDiv.appendChild(columnDiv1);
    userDiv.appendChild(columnDiv2);

    display.appendChild(userDiv);
  });
}

function createInventoryWeapons(items, header1, header2, header3, header4, header5, header6) {
  items.forEach(function(user) {
    let userDiv = document.createElement('div');
    userDiv.className = 'item-container';
    userDiv.style.position = 'relative';

    // Create img element for the user's item
    let display_img = document.createElement('img');
    display_img.src = user.column1; // Assuming column1 contains the image URL
    display_img.alt = 'Item Image';
    display_img.style.width = 'calc(100% / 6)'; // Set width to 1/6 of the container width
    userDiv.appendChild(display_img);


    let columnDiv1 = document.createElement('div');
    columnDiv1.className = 'item-info';

    let column2 = document.createElement('p');
    column2.textContent = `${header1}: ${user.column2}`; 
    columnDiv1.appendChild(column2);

    let column3 = document.createElement('p');
    column3.textContent = `${header2}: ${user.column3}`; 
    columnDiv1.appendChild(column3);
    
    let column5 = document.createElement('p');
    column5.textContent = `${header3}: ${user.column4}`; 
    columnDiv1.appendChild(column5);

    let columnDiv2 = document.createElement('div');
    columnDiv2.className = 'item-info';
    
    let column6 = document.createElement('p');
    column6.textContent = `${header4}: ${user.column5}`; 
    columnDiv2.appendChild(column6);

    let column7 = document.createElement('p');
    column7.textContent = `${header5}: ${user.column6}`; 
    columnDiv2.appendChild(column7);

    let column8 = document.createElement('p');
    column8.textContent = `${header6}: ${user.column8}`; 
    columnDiv2.appendChild(column8);

    userDiv.appendChild(columnDiv1);
    userDiv.appendChild(columnDiv2);

    display.appendChild(userDiv);
  });
}

// Function to 
function loadInventory() {
  clearDisplay();
  socket.emit('user_info', function(response) {
    if (response.error) {
      alert(response.error);
    } else {
      let userDiv = document.createElement('div');
      userDiv.className = 'user-info';
      userDiv.style.position = 'relative';
      userDiv.style.top = '-30px';

      let username = document.createElement('p');
      username.textContent = `Username: ${response.username}`;
      username.style.margin = '10px';
      username.style.marginTop = '30px';
      userDiv.appendChild(username);

      let level = document.createElement('p');
      level.textContent = `Level: ${response.level}`;
      level.style.margin = '10px';
      userDiv.appendChild(level);

      let affiliation = document.createElement('p');
      affiliation.textContent = `Affiliation: ${response.affiliation || 'None'}`;
      affiliation.style.margin = '10px';
      userDiv.appendChild(affiliation);

      let currentPlace = document.createElement('p');
      currentPlace.textContent = `Current Place: ${response.current_place || 'Unknown'}`;
      currentPlace.style.margin = '10px';
      userDiv.appendChild(currentPlace);

      let credits = document.createElement('p');
      credits.textContent = `Credits: ${response.credits}$`;
      credits.style.margin = '10px';
      userDiv.appendChild(credits);

      display.appendChild(userDiv);
    }
  });

  function handleItemsButtonClick() {
    clearDisplay();
    loadInventory();
    socket.emit("inventory", { type: 'items' }, function (response) {
      console.log(response)
      if (typeof response === 'string') {
        response = JSON.parse(response); 
        createInventoryItems(response, 'Item-Name', 'Quantity', 'Description');
      } else {
        console.log(response)
      }
    });
  }

  function handleToolsButtonClick() {
    clearDisplay();
    loadInventory();
    socket.emit("inventory", { type: 'tools' }, function (response) {
      console.log(response)
      if (typeof response === 'string') {
        response = JSON.parse(response); 
        createInventoryTools(response, 'Tool-Name', 'Durability', 'Efficiency', 'Rank', 'Description');
      } else {
        console.log(response)
      }
    });
  }

  function handleWeaponsButtonClick() {
    clearDisplay();
    loadInventory();
    socket.emit("inventory", { type: 'weapons' }, function (response) {
      console.log(response)
      if (typeof response === 'string') {
        response = JSON.parse(response); 
        createInventoryWeapons(response, 'Weapon-Name', 'Damage', 'Attack-Speed', 'Durability', 'Rank', 'Description');
      } else {
        console.log(response)
      }
    });
  }

  let itemsButton = document.createElement('button');
  itemsButton.textContent = 'Items';
  itemsButton.classList.add('fetchButton');
  itemsButton.addEventListener('click', handleItemsButtonClick);
  
  let toolsButton = document.createElement('button');
  toolsButton.textContent = 'Tools';
  toolsButton.classList.add('fetchButton');
  toolsButton.addEventListener('click', handleToolsButtonClick);
  
  let weaponsButton = document.createElement('button');
  weaponsButton.textContent = 'Weapons';
  weaponsButton.classList.add('fetchButton');
  weaponsButton.addEventListener('click', handleWeaponsButtonClick);   

  // Append buttons to the display element
  let buttonContainer = document.createElement('div');
  buttonContainer.appendChild(itemsButton);
  buttonContainer.appendChild(toolsButton);
  buttonContainer.appendChild(weaponsButton);
  buttonContainer.classList.add('subBtns')
  buttonContainer.style.top = '160px';
  buttonContainer.style.height = '18px';
  buttonContainer.style.position = 'relative';
  display.insertBefore(buttonContainer, display.firstChild);
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