import random, hashlib, secrets, string, uuid, os
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

# randomly generate a spawnpoint
spawnpoint = locations[random.choice(list(locations.keys()))][random.randint(0,4)]

# store user sessions (cookies)
sessions = {}

# store socket sessions (request.sid and cookie)
socket_sessions = []

# class to manage user stats temporary
class Stats:
    def __init__(self, session, health, stamina):
        self.session = session
        self.health = health
        self.stamina = stamina

    def update_stats(self, health_change, stamina_change):
        self.health += health_change
        self.stamina += stamina_change

# Dictionary to store user stats with session as the key
user_stats = {}

# Function to check cookie session for authentication
def check_session(session):
    if not session:
        return False
    if session not in sessions:
        return False
    
    return True

# API Endpoint for Game Interface if authentification
@app.route("/")
def hello_world():
    if check_session(request.cookies.get('session_token')) == False:
        return redirect(url_for('login'))

    image_path = '/static/img_01.png'
    return render_template('index.html', image_path=image_path)

# APIEndpoint for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username and password:
            db = DBSession()

            check = db.query(models.User).filter(models.User.username == username, models.User.password_hash == sha256_hash(password)).all()
            db.close()

            print(check)
            if not check:
                return render_template('login.html', error_msg='Wrong Username or Password')
            
            session_token = str(uuid.uuid4())

            sessions[session_token] = {
                'username': username
            }

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

# Socket Endpoint for auth
@socketio.on('auth')
def handle_message(data):
    session_id = data.get('data')
    if session_id and session_id in sessions:
        socket_sessions.append((session_id, request.sid))
        if session_id not in user_stats.keys():
            user_stats[session_id] = {'health': 100, 'stamina': 100}

        response_data = {
            'message': 'Successfully authorized!',
            'status_code': 200,
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
    return str(data)

# SocketEndpoint for attacking
@socketio.on('hunt')
def handle_message(data):
    if request.sid and any(request.sid == t[1] for t in socket_sessions):
        session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)
        if user_stats[session]['health'] > 0 and user_stats[session]['stamina'] > 0:

            user_stats[session]['health'] -= 10
            user_stats[session]['stamina'] -= 10

            response_data = {
                'health': user_stats[session]['health'],
                'stamina': user_stats[session]['stamina']
            }
        else:
            response_data = {
                'health': 0,
                'stamina': 0
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
    return str(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    socketio.run(app)