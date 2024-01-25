import random, hashlib, secrets, string, uuid, os, time
from flask import *
from model.database import DBSession
from model import models
from datetime import datetime, timedelta
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

# hash function for passwords
def sha256_hash(text):
    sha256 = hashlib.sha256()
    sha256.update(text.encode('utf-8'))
    return sha256.hexdigest()

# List of fantasy places for the text rpg
locations = {
    'Mountain': ['Dragonspire Peaks', 'Mystic Summit', 'Thunderpeak Range', "Eagle's Eyrie", 'Celestial Crest'],
    'Swamp': ['Shadowfen Marsh', 'Mistwood Bog', "Serpent's Lair", 'Foghaven Wetlands', 'Fiery Swamp'],
    'Desert': ['Dunes of Mirage', 'Sands of Serenity', 'Eternal Sun Wastes', 'Oasis of Dreams', 'Quicksand Mirage'],
    'Forest': ['Enchanted Arbor', 'Moonshade Grove', 'Elderwood Realm', 'Feywild Thicket', 'Sylvan Whisperwoods'],
    'Plains': ['Gilded Grasslands', 'Azure Savannah', 'Golden Horizon Fields', 'Elysian Meadowlands', 'Windswept Plains']
}

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

    db.close()
    
inject_data()

# Function to regenerate user stats over time
def regenerate_stats(player):
    while True:
        # Loop timer
        time.sleep(10)

        # regenerate stats
        if user_stats[player]['health'] < 100:
            user_stats[player]['health'] += 10
        if user_stats[player]['stamina'] < 100:
            user_stats[player]['stamina'] += 10

# store socket sessions (request.sid and cookie)
socket_sessions = []

# Dictionary to store user stats and sessions with session-UUID as key
user_stats = {}

# Function to check cookie session for authentication
def check_session(session):
    if not session:
        return False
    if session not in user_stats:
        return False
    
    return True

# API Endpoint for Game Interface if authentification
@app.route("/")
def hello_world():
    if check_session(request.cookies.get('session_token')) == False:
        return redirect(url_for('login'))

    image_path = '/static/img_01.png'
    return render_template('index.html', image_path=image_path, current_place=user_stats[request.cookies.get('session_token')]['current_place'][0])


# APIEndpoint for user login
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

            user_spawnpoint = db.query(models.User.spawnpoint).filter(models.User.username == username).first()
            user_level = db.query(models.User.level).filter(models.User.username == username).first()

            if session_token not in user_stats.keys():
                user_stats[session_token] = {'health': 100, 'stamina': 100, 'current_place': user_spawnpoint, 'regenerate': False, 'username': username, 'level': user_level}

            db.close()

            response = make_response(redirect('/'))
            response.set_cookie('session_token', session_token, expires=datetime.now() + timedelta(minutes=10), samesite='Strict')
            return response

    return render_template('login.html')

# API Endpoint for User signup
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
            
            new_user = models.User(
                username=username, password_hash=sha256_hash(password), level=1, spawnpoint=locations[random.choice(list(locations.keys()))][random.randint(0,4)]
            )

            db.add(new_user) 
            db.commit()
            db.refresh(new_user)
            db.close()

        return redirect(url_for('login'))
    
    return render_template('signup.html')


# Socket Section


# Socket Endpoint for auth
@socketio.on('auth')
def handle_message(data):
    session_id = data.get('data')
    if session_id and session_id in user_stats:
        socket_sessions.append((session_id, request.sid))

        if user_stats[session_id]['regenerate'] == False:
            regenerate_stats(session_id)

        response_data = {
            'message': 'Successfully authorized!',
            'status_code': 200,
            'health': user_stats[session_id]['health'],
            'stamina': user_stats[session_id]['stamina']
        }
    else:
        response_data = {
            'message': 'Authentication failed!',
            'status_code': 401
        }
    
    return response_data


# SocketEndpoint for attacking
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


# Socket Endpoint for mining
@socketio.on('collect')
def handle_message(data):
    if request.sid and any(request.sid == t[1] for t in socket_sessions):
        session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)
        if user_stats[session]['stamina'] > 0:

            user_stats[session]['stamina'] -= 10

            response_data = {
                'stamina': user_stats[session]['stamina']
            }
        else:
            response_data = {
                'error': 'No stamina left for collecting!',
                'error_code': 1,
                'health': user_stats[session]['health'],
                'stamina': user_stats[session]['stamina']
            }
    else:
        response_data = {
            'message': 'Authentication failed!',
            'status_code': 401
        }

    return response_data


# SocketEndpoint for attacking
@socketio.on('hunt')
def handle_message(data):
    if request.sid and any(request.sid == t[1] for t in socket_sessions):
        session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)
        if user_stats[session]['health'] == 10 and user_stats[session]['stamina'] > 0: # Check if User will die in this hunt (health too low)
            
            user_stats[session]['health'] -= 10
            user_stats[session]['stamina'] -= 10

            response_data = {
                'error': 'You died!',
                'error_code': 0,
                'health': user_stats[session]['health'],
                'stamina': user_stats[session]['health']
            }
        elif user_stats[session]['stamina'] == 0: # Check if there is stamina available to hunt
            response_data = {
                'error': 'No stamina left for hunting!',
                'error_code': 1,
                'health': user_stats[session]['health'],
                'stamina': user_stats[session]['stamina']
            }
        elif user_stats[session]['health'] > 0 and user_stats[session]['stamina'] > 0: # Check if there is stamina and health available to hunt

            user_stats[session]['health'] -= 10
            user_stats[session]['stamina'] -= 10

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


# Socket Endpoint for training
@socketio.on('train')
def handle_message(data):
    if request.sid and any(request.sid == t[1] for t in socket_sessions):
        session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)
        if user_stats[session]['stamina'] > 0:

            user_stats[session]['stamina'] -= 10

            response_data = {
                'stamina': user_stats[session]['stamina']
            }
        else:
            response_data = {
                'error': 'No stamina left for training!',
                'error_code': 1,
                'health': user_stats[session]['health'],
                'stamina': user_stats[session]['stamina']
            }
    else:
        response_data = {
            'message': 'Authentication failed!',
            'status_code': 401
        }

    return response_data


# Socket Endpoint for travelling
@socketio.on('travel')
def handle_message(direction):
    if request.sid and any(request.sid == t[1] for t in socket_sessions):
        session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

        db = DBSession()

        # Load spawnpoint to check level requirement for travelling to another place 
        spawnpoint = db.query(models.User.spawnpoint).filter(models.User.username == user_stats[session]['username']).first()
        
        db.close()

        if user_stats[session]['current_place'] and user_stats[session]['current_place'][0] is not None:
            cur_place = user_stats[session]['current_place'][0]
        else:
            cur_place = user_stats[session]['current_place']

        # Determine next place to travel to from direction from request
        next_place = travel(direction.get('data'), cur_place)
        if next_place == 'Invalid direction!' or next_place == 'No place to travel to in this direction!':
            response_data = {
                'error': next_place,
                'dir': direction.get('data')
            }
        
        else:
            user_stats[session]['current_place'] = next_place
            response_data = {
                'next_place': next_place,
                'dir': direction.get('data')
            }

    else:
        response_data = {
            'message': 'Authentication failed!',
            'status_code': 401
        }

    return response_data


# Function to determine next place to travel to
def travel(dir, cur_location):
    check_before = False
    check_after = False

    cur_location
    # Get biome of current place
    for index, biome in enumerate(locations):
        with open('yeet.txt', 'a') as file:
            file.write(f"{cur_location}\n{locations[biome]}\n")
        if check_after == True and index != 4: # Check if new location was found and set biome after
            biome_after = biome
            index_after = index
            check_after = False
        if cur_location in locations[biome]: # Check if new location was found
            check_before = True
            check_after = True
            current_biome = biome
            current_index = index
        if check_before == False: # Check if new location was found and set biome before
            biome_before = biome
            index_before = index

    # Get new place for direction
    if dir == 'N':
        if current_index != 0:
            new_location_index = locations[current_biome].index(cur_location)
            new_location = locations[biome_before][new_location_index]
        else:
            return 'No place to travel to in this direction!'
    elif dir == 'NW':
        if current_index != 0:
            new_location_index = locations[current_biome].index(cur_location) - 1
            new_location = locations[biome_before][new_location_index]
        else:
            return 'No place to travel to in this direction!'
    elif dir == 'NE':
        if current_index != 0:
            new_location_index = locations[current_biome].index(cur_location) + 1
            new_location = locations[biome_before][new_location_index]
        else:
            return 'No place to travel to in this direction!'
    elif dir == 'E':
        if locations[current_biome].index(cur_location) != 0:
            new_location_index = locations[current_biome].index(cur_location) + 1
            new_location = locations[current_biome][new_location_index]
        else:
            return 'No place to travel to in this direction!'
    elif dir == 'S':
        if current_index != 4:
            new_location_index = locations[current_biome].index(cur_location)
            new_location = locations[biome_after][new_location_index]
        else:
            return 'No place to travel to in this direction!'
    elif dir == 'SW':
        if current_index != 4:
            new_location_index = locations[current_biome].index(cur_location) - 1
            new_location = locations[biome_after][new_location_index]
        else:
            return 'No place to travel to in this direction!'
    elif dir == 'SE':
        if current_index != 4:
            new_location_index = locations[current_biome].index(cur_location) + 1
            new_location = locations[biome_after][new_location_index]
        else:
            return 'No place to travel to in this direction!'
    elif dir == 'W':
        if locations[current_biome].index(cur_location) != 4:
            new_location_index = locations[current_biome].index(cur_location) - 1
            new_location = locations[current_biome][new_location_index]
        else:
            return 'No place to travel to in this direction!'
    else:
        return 'Invalid direction!'

    with open('yeet.txt', 'a') as file:
        file.write(f'{new_location}\n')

    return new_location    


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    socketio.run(app)