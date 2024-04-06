# Elysium Realms

> [!NOTE]
>
> This Web-Challenge is about finding a curcial vulnerabiltiy inside a Web-Game-Application. <br/>
> Big thanks to [Aisle-Designs](https://aisledesigns.com/) to design the gaming web-interface.

## Challenge Development

To automate the challenge I first setup a `docker-compose.yml` file which exports the necessary ports and imports the flag via an ARG var. <br/>
```yml
version: '3.9'

services:
  flask:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - FLAG=$FLAG
    ports:
      - "80:5000"
```

The `Dockerfile` sets up a python environment to host the application and import the flag as environment variable. <br/>
```docker
FROM python:latest

ARG FLAG
ENV FLAG=${FLAG}

WORKDIR .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "service.py"]
```

The application should be a simple web-based text MMO-RPG game. <br/>
For this purpose I used simple session authentication using `UUIDs` in cookies. <br/>
```py
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            db = DBSession()

            check = db.query(models.User).filter(models.User.username == username, models.User.password_hash == sha256_hash(password)).first()
            
            if not check:
                return render_template('login.html', error_msg='Wrong Username or Password')
            
            session_token = str(uuid.uuid4())

            current_place = db.query(models.User.current_place).filter(models.User.username == username).first()
            user_level = db.query(models.User.level).filter(models.User.username == username).first()

            if session_token not in user_stats.keys():
                user_stats[session_token] = {'health': 100, 'stamina': 100, 'current_place': current_place[0], 'regenerate': False, 'username': username, 'level': user_level, 'last_action': time.time() - throttle_interval}

            db.close()

            response = make_response(redirect('/'))
            response.set_cookie('session_token', session_token, expires=datetime.now() + timedelta(minutes=10), samesite='Strict')
            return response

    return render_template('login.html')
```
The `/login` endpoint allows any user to login and create a new session to play the game. <br/>
If the user exists and ca nauthenticate normally, base stats are set for the player to play the game. <br/> <br/>

```py
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            db = DBSession()

            check = db.query(models.User).filter(models.User.username == username).all()

            if check:
                return render_template('signup.html', error_msg='This User does already exist!')
            
            spawnpoint = locations[random.choice(list(locations.keys()))][random.randint(0,4)]

            new_user = models.User(
                username=username, password_hash=sha256_hash(password), level=1, spawnpoint=spawnpoint, current_place=spawnpoint, affiliation=None, credits=0
            )

            db.add(new_user) 
            db.commit()
            db.refresh(new_user)
            db.close()

        return redirect(url_for('login'))
    
    return render_template('signup.html')
```
The `/signup` endpoint allows the creation of a new account if the username isn't already taken. <br/>
When the user is created in the database default stats are set like `level=1`, `credits=0` or `affiliation=None`. <br/>
Because this is a MMO-RPG I added random spawn-locations. <br/>
```py
locations = {
    'Mountain': ['Dragonspire Peaks', 'Mystic Summit', 'Thunderpeak Range', "Eagle's Eyrie", 'Celestial Crest'],
    'Forest': ['Enchanted Arbor', 'Moonshade Grove', 'Elderwood Realm', 'Feywild Thicket', 'Sylvan Whisperwoods'],
    'Swamp': ['Shadowfen Marsh', 'Mistwood Bog', "Serpent's Lair", 'Foghaven Wetlands', 'Fiery Swamp'],
    'Plains': ['Gilded Grasslands', 'Azure Savannah', 'Golden Horizon Fields', 'Elysian Meadowlands', 'Windswept Plains'],
    'Desert': ['Dunes of Mirage', 'Sands of Serenity', 'Eternal Sun Wastes', 'Oasis of Dreams', 'Quicksand Mirage']
}
```
You can observe 25 distinct biomes displayed above. <br/>
When an account gets created a random biome is being chosen and assigned to the user which will be the spawnlocation and can be used to track how far the player its original place.
This can help to get different drops in different regions as the level of difficulty can be raised by the distance in biomes the user has from its spawn-biome. <br/> <br/>
When logged in the user has a main interface on which several actions can be performed. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/6a37963e-96f8-42b5-9f40-29ccdadd6e90)

The game itself works via websockets. <br/>
All actions which a user can perform are executed via socket endpoints. <br/>
To use socket sessions which directly store valuable user data in the database I need to authenticate a socket session. <br/>
```py
@socketio.on('auth')
def handle_message(data):
    session_id = data.get('data')
    if session_id and session_id in user_stats:
        socket_sessions.append((session_id, request.sid))

        if user_stats[session_id]['regenerate'] == False:
            user_stats[session_id]['regenerate'] = True
            regenerate_stats(session_id)

        return {'message': 'Successfully authorized!', 'status_code': 200, 'health': user_stats[session_id]['health'], 'stamina': user_stats[session_id]['stamina']}
    else:
        return {'message': 'Authentication failed!', 'status_code': 401}
```
Every Socket-Session has its own `sid`. I use this `sid` and the cookie-session to identify a user. <br/>
If the cookie-session is verified a new session is being added and will be verified for every socket endpoint. <br/>
To get a users current stats like `health` and `stamina` I setup a simple endpoint. <br/> <br/>

```py
@socketio.on('stats')
def handle_message(data):
    if request.sid and any(request.sid == t[1] for t in socket_sessions):
        session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)
        response_data = {
            'health': user_stats[session]['health'],
            'stamina': user_stats[session]['stamina']
        }
    else:
        response_data = {
            'message': 'Authentication failed!',
            'status_code': 401
        }

    return response_data
```
This will return the current stats and can be used in the main-interface. <br/> <br/>

```py
@socketio.on('collect')
def handle_collect():
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}
        
    session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

    health, stamina = user_stats[session]['health'], user_stats[session]['stamina']

    if throttle(session):
        return {'error': 'Wait a bit before collecting again!', 'error_code': 2}

    if health == 0:
        user_stats[session]['regenerate'] = False
        return {'error': 'You are dead!', 'error_code': 1, 'health': 0, 'stamina': 0}

    if stamina <= 0:
        return {'error': 'No stamina left for collecting!', 'error_code': 1}

    user_stats[session]['stamina'] -= 10
    user_stats[session]['last_action'] = time.time()

    collected_item = random.choice(collecting_materials)

    try:
        db = DBSession()

        user = db.query(models.User).filter(models.User.username == user_stats[session]['username']).first()

        found_material = models.Item(
            itemname=collected_item, quantity=1, type='materials', price=random.randint(10, 1000), affiliation=user.username, description='An item aquired while collecting.'
        )
        db.add(found_material)
        db.commit()
        db.refresh(found_material)

        return {'stamina': user_stats[session]['stamina'], 'collected_material': collected_item }

    finally:
        db.close()
```
The `/collect` socket endpoint will try to perform the action `collect` which will return a random item if the user has enough `stamina` and `health`. <br/>
```py
collecting_materials = [
    "Wood", "Stone", "Iron Ore", "Gold Ore", "Copper Ore",
    "Silver Ore", "Diamond", "Coal", "Clay", "Flint", "Obsidian",
    "Sulfur", "Quartz"
]
```
The `collecting_materials` array holds different items a user can aquire. <br/>
If all requirements are met a user will get a new item and lose some of its stamina in exchange. <br/>
It's also important to keep in mind that I use `throttle(session)` to check if a user is not performign actions too fast (Only every 2 seconds). <br/> <br/>

```py
@socketio.on('hunt')
def handle_message():
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}
    
    session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

    if throttle(session):
        return {'error': 'Wait a bit before hunting again!', 'error_code': 2}

    health, stamina = user_stats[session]['health'], user_stats[session]['stamina']

    if health == 0:
        return {'error': 'You are dead!', 'error_code': 0, 'health': 0, 'stamina': 0}

    if stamina == 0:
        return {'error': 'No stamina left for hunting!', 'error_code': 1, 'health': health, 'stamina': stamina}

    user_stats[session].update({'health': health - 10, 'stamina': stamina - 10})

    if health == 10: # Check if User will die in this hunt (health too low)
        user_stats[session]['regenerate'] = False
        return {'error': 'You died!', 'error_code': 1, 'health': health, 'stamina': stamina}
    
    user_stats[session]['last_action'] = time.time()

    hunted_item = random.choice(hunting_materials)

    try:
        db = DBSession()

        user = db.query(models.User).filter(models.User.username == user_stats[session]['username']).first()

        found_material = models.Item(
            itemname=hunted_item, quantity=1, type='materials', price=random.randint(10, 1000), affiliation=user.username, description='An item aquired while hunting.'
        )
        db.add(found_material)
        db.commit()
        db.refresh(found_material)

        return { 'health': health - 10, 'stamina': stamina - 10, 'hunted_material': hunted_item }

    finally:
        db.close()
```
The `/hunt` socket endpoint works almost the same as the `/collect` socket endpoint except the items it can aquire through hunting are different. <br/>
```py
hunting_materials = [
    "Leather", "Wool", "Feathers", "Bone",
    "Hide", "Fur", "Shell", "Wolf-Fangs", 
]
```
The items above can be aquired through hunting. <br/> <br/>

```py
@socketio.on('train')
def handle_train():
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}
        
    session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

    health, stamina = user_stats[session]['health'], user_stats[session]['stamina']

    if throttle(session):
        return {'error': 'Wait a bit before training again!', 'error_code': 2}

    if health == 0:
        user_stats[session]['regenerate'] = False
        return {'error': 'You are dead!', 'error_code': 1, 'health': 0, 'stamina': 0}

    if stamina <= 0:
        return {'error': 'No stamina left for training!', 'error_code': 1}

    user_stats[session]['stamina'] -= 10
    user_stats[session]['last_action'] = time.time()

    return {'stamina': user_stats[session]['stamina']}
```
The `/train` socket endpoint itself works the same as the others except that it is actually useles and does nothing. <br/>
It is there just for game aesthetic design. <br/> <br/>

```py
@socketio.on('travel')
def handle_message(direction):
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}

    session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

    db = DBSession()

    # Load spawnpoint to check level requirement for travelling to another place (never implemented)
    spawnpoint = db.query(models.User.spawnpoint).filter(models.User.username == user_stats[session]['username']).first()

    if user_stats[session]['current_place'][0] is not None and len(user_stats[session]['current_place'][0]) > 1:
        cur_place = user_stats[session]['current_place'][0]
    else:
        cur_place = user_stats[session]['current_place']

    # Determine next place to travel to from direction from request
    next_place = travel(direction.get('data'), cur_place)

    if next_place in error_msg:
        db.close()
        return {'error': next_place, 'dir': direction.get('data')}
        
    user_stats[session]['current_place'] = next_place

    # Update new location in db
    current_place = db.query(models.User).filter(models.User.username == user_stats[session]['username']).first()
    current_place.current_place = next_place

    db.commit()
    db.close()

    return {'next_place': next_place, 'img_url': get_img(next_place), 'dir': direction.get('data')}
```
The `/travel` endpoint allows a user to travel to a new biome/region. <br/>
To check if there is a biome in the direction a user wants to travel to I created another function. <br/>
```py
def travel(dir, cur_location):
    check_before, check_after = False, False

    # Loop to determine next place to travel to
    for index, biome in enumerate(locations):
        if check_after == True and index < 5: # Check if new location was found and set biome after
            biome_after = biome
            check_after = False
        if cur_location in locations[biome]: # Check if new location was found
            check_before = True
            check_after = True
            current_biome = biome
            current_index = index
        if check_before == False: # Check if new location was found and set biome before
            biome_before = biome

    # Get new place for direction
    match dir:
        case 'N': # Direction North
            if current_index > 0:
                new_location_index = locations[current_biome].index(cur_location)
                new_location = locations[biome_before][new_location_index]
            else:
                return error_msg[0]
            
        case 'NW': # Direction North-West
            if current_index > 0 and locations[current_biome].index(cur_location) > 0:
                new_location_index = locations[current_biome].index(cur_location) - 1
                new_location = locations[biome_before][new_location_index]
            else:
                return error_msg[0]

        case 'NE': # Direction North-East
            if current_index > 0 and locations[current_biome].index(cur_location) < 4:
                new_location_index = locations[current_biome].index(cur_location) + 1
                new_location = locations[biome_before][new_location_index]
            else:
                return error_msg[0]

        case 'E': # Direction East
            if locations[current_biome].index(cur_location) < 4:
                new_location_index = locations[current_biome].index(cur_location) + 1
                new_location = locations[current_biome][new_location_index]
            else:
                return error_msg[0]

        case 'S': # Direction South
            if current_index < 4:
                new_location_index = locations[current_biome].index(cur_location)
                new_location = locations[biome_after][new_location_index]
            else:
                return error_msg[0]

        case 'SW': # Direction South-West
            if current_index < 4 and locations[current_biome].index(cur_location) > 0:
                new_location_index = locations[current_biome].index(cur_location) - 1
                new_location = locations[biome_after][new_location_index]
            else:
                return error_msg[0]

        case 'SE': # Direction South-East
            if current_index < 4 and locations[current_biome].index(cur_location) < 4:
                new_location_index = locations[current_biome].index(cur_location) + 1
                new_location = locations[biome_after][new_location_index]
            else:
                return error_msg[0]

        case 'W': # Direction West
            if locations[current_biome].index(cur_location) > 0:
                new_location_index = locations[current_biome].index(cur_location) - 1
                new_location = locations[current_biome][new_location_index]
            else:
                return error_msg[0]

        case _: # else
            return error_msg[1]

    return new_location
```
In the function above I check if a valid biome is in that direction and if so the location is being updated. <br/>
Every location has its own image generated using [Stable Diffusion](https://github.com/AUTOMATIC1111/stable-diffusion-webui). <br/>
If everything works out the next place is being returned to the user together wit hthe new URL to the image (All images are stored externally). <br/> <br/>


The menu itself includes 4 differnet options. <br/>
- `Inventory` -> A user can check the current stats like `level` or `credits` and see all `items`, `weapons` and `tools` he/she/it possesses.
- `Leaderboard` -> Current leaderboard of all users and guilds.
- `Marketplace` -> All `items`, `tools` and `weapons` which are currently sold. This also includes the flag of the challenge. <br/>
- `Transfer` -> A function to transfer credits between players.

```py
@socketio.on('leaderboard')
def leaderboard(data):
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}
    
    group = data.get('data')
    db = DBSession()

    match group:
        case 'users':
            users_data = db.query(models.User.username, models.User.level, models.User.affiliation).order_by(models.User.level.desc()).all()
            result = [{'column1': username, 'column2': level, 'column3': affiliation if affiliation is not None else 'None'} for username, level, affiliation in users_data]
        case 'guilds':
            guild_member_count_query = db.query(models.Guild.title, models.Guild.level, func.count(models.User.username).label('member_count')).outerjoin(models.User).group_by(models.Guild.title, models.Guild.level).order_by(models.Guild.level.desc())
            guilds_with_member_count = guild_member_count_query.all()
            result = [{'column1': guild.title, 'column2': guild.level, 'column3': guild.member_count} for guild in guilds_with_member_count]
        case _:
            result = {'error': 'No such group in database!'}

    result_json = json.dumps(result)
    db.close()
    return result_json
```
The `/leaderboard` socket endpoint returns either all users or guilds descending by level. <br/> <br/>

```py
@socketio.on('showCredits')
def showCredits():
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}
    
    session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)
    
    db = DBSession()

    users_credits = db.query(models.User.credits).filter(models.User.username == user_stats[session]['username']).first()

    result = { 'credits': users_credits[0] }
    result_json = json.dumps(result)
    db.close()
    return result_json
```

The `/showCredits` endpoint returns a users current credits. <br/>
This is used in the transfer function to display the amount a user can transfer. <br/> <br/>

```py
@socketio.on('transfer')
def transfer(data):
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}
    
    session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

    target = data.get('target')
    amount = data.get('amount')

    db = DBSession()

    try:
        user_from = db.query(models.User).filter(models.User.username == user_stats[session]['username']).first()

        target_user = db.query(models.User).filter(models.User.username == target).first()

        if user_from.username == target:
            return {'error': "Can't transfer money to yourself!"}

        if user_from.credits < int(amount):
            return {'error': "You don't have enough social-credits to transfer!"}

        if target_user:
            target_user.credits = target_user.credits + int(amount)
            user_from.credits = user_from.credits - int(amount)
            db.commit()

            return {'success': f'amount transferred!'}
        else:
            return {'error': "Transfer-User doesn't exist!"}

    except Exception as e:
        db.rollback()
        return {'error': f"Transfer can't be processed!{e}"}

    finally:
        db.close()
```

The `/tranfer` socket endpoint allows the transfer of credits between users. <br/>

> [!NOTE]
> This endpoint contains the vulnerability in the application. <br/>
> `user_from.credits = user_from.credits - int(amount)` allows a user to gain credits by sending negative sums. <br/> 
<br/>

```py
@socketio.on('inventory')
def inventory(data):
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}

    session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

    db = DBSession()
    type = data.get('type')

    try:
        user = db.query(models.User).filter(models.User.username == user_stats[session]['username']).first()

        match type:
            case 'items':
                items_data = db.query(models.Item.itemname, models.Item.description, models.Item.quantity, models.Item.type, models.Item.price, models.Item.affiliation, models.Item.id).filter(models.Item.affiliation == user.username).order_by(models.Item.quantity.desc()).all()
                result_items = [{'column1': f'https://winklersblog.net/imgs/elysium_realms/{item.type}.png', 'column2': item.itemname, 'column3': item.quantity, 'column4': item.id, 'column5': item.description} for item in items_data]

                return json.dumps(result_items)

            case 'tools':
                tools_data = db.query(models.Tool.toolname, models.Tool.description, models.Tool.durability, models.Tool.efficiency, models.Tool.rank, models.Tool.type, models.Tool.price, models.Tool.affiliation, models.Tool.id).filter(models.Tool.affiliation == user.username).order_by(models.Tool.rank.desc()).all()
                result_items = [{'column1': f'https://winklersblog.net/imgs/elysium_realms/{tool.type}.png', 'column2': tool.toolname, 'column3': tool.durability, 'column4': tool.efficiency, 'column5': tool.rank, 'column6': tool.id, 'column7': tool.description} for tool in tools_data]

                return json.dumps(result_items)

            case 'weapons':
                weapons_data = db.query(models.Weapon.weaponname, models.Weapon.description, models.Weapon.damage, models.Weapon.attack_speed, models.Weapon.durability, models.Weapon.rank, models.Weapon.type, models.Weapon.price, models.Weapon.affiliation, models.Weapon.id).filter(models.Weapon.affiliation == user.username).order_by(models.Weapon.rank.desc()).all()
                result_items = [{'column1': f'https://winklersblog.net/imgs/elysium_realms/{weapon.type}.png', 'column2': weapon.weaponname, 'column3': weapon.damage, 'column4': weapon.attack_speed, 'column5': weapon.durability, 'column6': weapon.rank, 'column7': weapon.id, 'column8': weapon.description} for weapon in weapons_data]

                return json.dumps(result_items)
            
            case _:
                return {'error': 'No such item-type!'}

    except Exception as e:
        db.rollback()
        return {'error': str(e)}

    finally:
        db.close()
```
The `/inventory` socket endpoint returns all `items`, `tools` or `weapons` he/she/it possesses. <br/> <br/>

```py
@socketio.on('user_info')
def user_info():
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}

    session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

    db = DBSession()

    try:
        user = db.query(models.User).filter(models.User.username == user_stats[session]['username']).first()

        return {
            'username': user.username,
            'level': user.level,
            'affiliation': user.affiliation,
            'current_place': user.current_place,
            'credits': user.credits
        }

    except Exception as e:
        db.rollback()
        return {'error': str(e)}

    finally:
        db.close()
```
The `/user_info` socket endpoint returns all user stats for the inventory. <br/> <br/>

```py
@socketio.on('marketPlace')
def market_Place(data):
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}

    db = DBSession()
    group = data.get('data')

    try:
        match group:
            case 'items':
                items_data = db.query(models.Item.itemname, models.Item.quantity, models.Item.type, models.Item.price, models.Item.affiliation, models.Item.id).order_by(models.Item.quantity.desc()).all()
                result_items = [{'column1': f'https://winklersblog.net/imgs/elysium_realms/{item.type}.png', 'column2': item.itemname, 'column3': item.quantity, 'column4': item.price, 'column5': item.affiliation, 'column6': item.id} for item in items_data]

                return json.dumps(result_items)

            case 'tools':
                tools_data = db.query(models.Tool.toolname, models.Tool.durability, models.Tool.efficiency, models.Tool.rank, models.Tool.type, models.Tool.price, models.Tool.affiliation, models.Tool.id).order_by(models.Tool.rank.desc()).all()
                result_items = [{'column1': f'https://winklersblog.net/imgs/elysium_realms/{tool.type}.png', 'column2': tool.toolname, 'column3': tool.durability, 'column4': tool.efficiency, 'column5': tool.rank, 'column6': tool.price, 'column7': tool.affiliation, 'column8': tool.id} for tool in tools_data]

                return json.dumps(result_items)

            case 'weapons':
                weapons_data = db.query(models.Weapon.weaponname, models.Weapon.damage, models.Weapon.attack_speed, models.Weapon.durability, models.Weapon.rank, models.Weapon.type, models.Weapon.price, models.Weapon.affiliation, models.Weapon.id).order_by(models.Weapon.rank.desc()).all()
                result_items = [{'column1': f'https://winklersblog.net/imgs/elysium_realms/{weapon.type}.png', 'column2': weapon.weaponname, 'column3': weapon.damage, 'column4': weapon.attack_speed, 'column5': weapon.durability, 'column6': weapon.rank, 'column7': weapon.price, 'column8': weapon.affiliation, 'column9': weapon.id} for weapon in weapons_data]

                return json.dumps(result_items)

            case _:
                return json.dumps({'error': 'No such group in database!'})

    except Exception as e:
        db.rollback()
        return {'error': str(e)}

    finally:
        db.close()
```
The `/marketplace` endpoint returns all `items`, `tools` or `weapons` which are sold by other users. <br/> <br/>

```py
@socketio.on('buy')
def buy_item(data):
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}

    session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

    db = DBSession()

    type = data.get('type')
    id = data.get('id')

    try:
        user = db.query(models.User).filter(models.User.username == user_stats[session]['username']).first()

        match type:
            case 'item':
                item = db.query(models.Item).filter(models.Item.id == id).first()

                if user.credits >= item.price:
                    user.credits -= item.price
                    item.affiliation = user.username
                    db.commit()
                    return {'success': 'Item bought!'}
                else:
                    return {'error': "Can't afford item!"}

            case 'tool':
                tool = db.query(models.Tool).filter(models.Tool.id == id).first()

                if user.credits >= tool.price:
                    user.credits -= tool.price
                    tool.affiliation = user.username
                    db.commit()
                    return {'success': 'Tool bought!'}
                else:
                    return {'error': "Can't afford tool!"}
            
            case 'weapon':
                weapon = db.query(models.Weapon).filter(models.Weapon.id == id).first()

                if user.credits >= weapon.price:
                    user.credits -= weapon.price
                    weapon.affiliation = user.username
                    db.commit()
                    return {'success': 'Weapon bought!'}
                else:
                    return {'error': "Can't afford weapon!"}
                
            case _:
                return {'error': f'No such type found'}
    
    except Exception as e:
        db.rollback()
        return {'error': str(e)}

    finally:
        db.close()
```
The `/buy` socket endpoint allows users to buy other users' `items`, `tools` and `weapons`. <br/>
Once bought any item can be found in the inventory. <br/> <br/>

To make the game more realistic I added fake game data which is being generated once the container starts up. <br/>
```py
def rndm_tool():
    choices = ['shovel', 'chisel', 'pickaxe']
    tool = random.choice(choices)

    ranks = ['common', 'rare', 'epic', 'legendary', 'mythic']
    rank = random.choice(ranks)

    properties = ['Sharp','Durable','Lightweight (baby!)','Efficient','Versatile','Sturdy','Wide-blade','Heavy-duty','Precision','Multi-functional']
    my_property = random.choice(properties)

    return {
        'toolname': f'{my_property} {tool}',
        'durability':random.uniform(1, 99),
        'efficiency': random.randrange(1, 10),
        'rank': rank,
        'type': f'tool_0{random.randrange(0, 5)}'
    }

def rndm_weapon():
    ranks = ['common', 'rare', 'epic', 'legendary', 'mythic']
    rank = random.choice(ranks)

    properties = ['Sharp','Durable','Lightweight (baby!)','Deahtly','Versatile','Sturdy','Wide','Heavy-duty','Precision','Multi-functional']
    my_property = random.choice(properties)

    return {
        'weaponname': f'{my_property} blade',
        'damage': random.randrange(1, 1000),
        'attack_speed': random.uniform(1, 1000),
        'durability': random.uniform(1, 99),
        'rank': rank,
        'type': f'blade_0{random.randrange(0, 6)}'

def inject_data():
    db = DBSession()

    # insert guilds
    for guild in open('data/guilds.txt', 'r'):
        check = db.query(models.Guild).filter(models.Guild.title == guild.split('\n')[0]).all()

        if check:
            continue

        if guild.strip() != 'Ainz Ooal Gown': # check for custom details
            new_guild = models.Guild(
                title=guild.strip(), level=random.randint(1, 6)
            )
        else:
            new_guild = models.Guild(
                title=guild.strip(), level=10
            )
        
        db.add(new_guild) # commit new entry to db
        db.commit()
        db.refresh(new_guild)

    # insert users
    for user in open('data/users.txt', 'r'):
        check = db.query(models.User).filter(models.User.username == user.strip()).all()

        if check:
            continue

        if user.strip() != 'Aryt3': # check for custom details
            new_user = models.User(
                username=user.strip(), password_hash=sha256_hash(''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))), level=random.randint(1, 99), affiliation=random.choice(open('data/guilds.txt').readlines()[1:]).rstrip('\n') if open('data/guilds.txt').readlines()[1:] else None
            )
        else:
            new_user = models.User(
                username=user.strip(), password_hash=sha256_hash(''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))), level=100, affiliation='Ainz Ooal Gown'
            )
        
        db.add(new_user) # commit new entry to db
        db.commit()
        db.refresh(new_user)

    # insert random items
    for _ in range(0, 50):
        new_item = models.Item(
            itemname=random.choice(materials), description='An item which is very dear to me.', quantity=random.randrange(1, 100), type='materials', price=random.randint(1000, 100000), affiliation='Aryt3'
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    
    for _ in range(0, 50):
        tool = rndm_tool()
        
        new_tool = models.Tool(
            toolname=tool['toolname'], description='A tool which is very dear to me.', durability=tool['durability'], efficiency=tool['efficiency'], rank=tool['rank'], type=tool['type'], price=random.randint(1000, 100000), affiliation='Aryt3'
        )
        db.add(new_tool)
        db.commit()
        db.refresh(new_tool)

    for _ in range(0, 50):
        weapon = rndm_weapon()

        new_weapon = models.Weapon(
            weaponname=weapon['weaponname'], description='A weapon which is very dear to me.', damage=weapon['damage'], attack_speed=weapon['attack_speed'], durability=weapon['durability'], rank=weapon['rank'], type=weapon['type'], price=random.randint(1000, 100000), affiliation='Aryt3'
        )
        db.add(new_weapon)
        db.commit()
        db.refresh(new_weapon)

    flag = models.Item(
        itemname='super secret flag', description=f'TH{{{os.environ.get("FLAG")}}}', quantity=1, type='flag', price=1234567890, affiliation='Aryt3'
    )
    db.add(flag)
    db.commit()
    db.refresh(flag)

    db.close()
```
The files `guilds.txt` and `users.txt` contain random names which are being loaded into the game. <br/> <br/>

```py
import time

# Dictionary to store user stats and sessions with session-UUID as key
user_stats = {}

# store socket sessions (request.sid and cookie)
socket_sessions = []

# Time for a player to heal once
heal_interval = 10

# Function to regenerate user stats over time
def regenerate_stats(player):
    while user_stats[player]['regenerate'] == True:
        time.sleep(heal_interval) # Loop timer

        # regenerate stats
        if user_stats[player]['health'] < 100:
            user_stats[player]['health'] += 10
        if user_stats[player]['stamina'] < 100:
            user_stats[player]['stamina'] += 10

# Function to check cookie session for authentication
def check_session(session):
    if not session:
        return False
    if session not in user_stats:
        return False
    
    return True

# Time to throttle actions in seconds
throttle_interval = 2

# Function to throttle actions a user can execute in a certain amount of time
def throttle(session):
    if time.time() - user_stats[session]['last_action'] < throttle_interval:
        return True
    else:
        return False
```
To authenticate users I use an array and a dictioanry to store them temporary. <br/>
I also have a function to regenerate a users stats every 10 seconds for the purpose of game functionality. <br/>
The `throttle` function checks for last action taking by a user to cap the actions a user can perform per a set amount of time. <br/>

I used a local `game.db` file together with `sqlite` to store all different kinds of things. <br/>
```py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL = f'sqlite:///game.db'

engine = create_engine(SQLALCHEMY_DB_URL, echo=True)
DBSession = sessionmaker(engine, autoflush=False)
```

Different tables are setup to achieve game functionality. <br/>
```py
from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    username = Column(String(length=255), primary_key=True)
    password_hash = Column(String(length=255))
    level = Column(Integer())
    affiliation = Column(String(length=255), ForeignKey("guilds.title"))
    spawnpoint = Column(String(length=255))
    current_place = Column(String(length=255))
    credits = Column(BigInteger())

    def __repr__(self):
        return f'User(username={self.username}, password_hash={self.password_hash}, level={self.level}, affiliation={self.affiliation}, spawnpoint={self.spawnpoint}, current_place={self.current_place}, credits={self.credits})'

class Guild(Base):

    __tablename__ = "guilds"

    title = Column(String(length=255), primary_key=True)
    level = Column(Integer())

    def __repr__(self):
        return f'Guild(title={self.title}, level={self.level})'

class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    itemname = Column(String(length=255))
    description = Column(String(length=255))
    quantity = Column(Integer())
    type = Column(String(length=20))
    price = Column(BigInteger())
    affiliation = Column(String(length=255), ForeignKey("users.username"))

    def __repr__(self):
        return f'Item(id={self.id}, itemname={self.itemname}, description={self.description}, quantity={self.quantity}, price={self.price}, affiliation={self.affiliation})'

class Tool(Base):

    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, autoincrement=True)
    toolname = Column(String(length=255))
    description = Column(String(length=255))
    durability = Column(Float())
    efficiency = Column(Float())
    rank = Column(String(length=255)) 
    type = Column(String(length=20))
    price = Column(BigInteger())
    affiliation = Column(String(length=255), ForeignKey("users.username"))

    def __repr__(self):
        return f'Tool(id={self.id}, toolname={self.toolname}, description={self.description}, durability={self.durability}, efficiency={self.efficiency}, rank={self.rank}, type={self.type}, price={self.price}, affiliation={self.affiliation})'

class Weapon(Base):

    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    weaponname = Column(String(length=255))
    description = Column(String(length=255))
    damage = Column(Float())
    attack_speed = Column(Float())
    durability = Column(Float())
    rank = Column(String(length=255)) 
    type = Column(String(length=20))
    price = Column(BigInteger())
    affiliation = Column(String(length=255), ForeignKey("users.username"))

    def __repr__(self):
        return f'Weapon(id={self.id}, weaponname={self.weaponname}, description={self.description}, damage={self.damage}, attack_speed={self.attack_speed}, durability={self.durability}, rank={self.rank}, type={self.type}, price={self.price}, affiliation={self.affiliation})'
```

All of this together creates a simple text-based MMO-RPG in the web. <br/>

