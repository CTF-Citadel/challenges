import random, uuid, os, time
from flask import *
from model.database import DBSession
from model import models
from datetime import datetime, timedelta
from flask_socketio import SocketIO
from game import *
from manage_sessions import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

# Inject fake users and guilds
inject_data()

# API Endpoint for Game Interface if authentification
@app.route("/")
def hello_world():
    if check_session(request.cookies.get('session_token')) == False:
        return redirect(url_for('login'))

    return render_template('index.html', image_path=get_img(user_stats[request.cookies.get('session_token')]['current_place']), current_place=user_stats[request.cookies.get('session_token')]['current_place'])

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

            current_place = db.query(models.User.current_place).filter(models.User.username == username).first()
            user_level = db.query(models.User.level).filter(models.User.username == username).first()

            if session_token not in user_stats.keys():
                user_stats[session_token] = {'health': 100, 'stamina': 100, 'current_place': current_place[0], 'regenerate': False, 'username': username, 'level': user_level, 'last_action': time.time() - throttle_interval}

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
            
            spawnpoint = locations[random.choice(list(locations.keys()))][random.randint(0,4)]

            new_user = models.User(
                username=username, password_hash=sha256_hash(password), level=1, spawnpoint=spawnpoint, current_place=spawnpoint
            )

            db.add(new_user) 
            db.commit()
            db.refresh(new_user)
            db.close()

        return redirect(url_for('login'))
    
    return render_template('signup.html')


#     /$$$$$$                      /$$                   /$$            /$$$$$$                        /$$     /$$                    
#    /$$__  $$                    | $$                  | $$           /$$__  $$                      | $$    |__/                    
#   | $$  \__/  /$$$$$$   /$$$$$$$| $$   /$$  /$$$$$$  /$$$$$$        | $$  \__/  /$$$$$$   /$$$$$$$ /$$$$$$   /$$  /$$$$$$  /$$$$$$$ 
#   |  $$$$$$  /$$__  $$ /$$_____/| $$  /$$/ /$$__  $$|_  $$_/        |  $$$$$$  /$$__  $$ /$$_____/|_  $$_/  | $$ /$$__  $$| $$__  $$
#    \____  $$| $$  \ $$| $$      | $$$$$$/ | $$$$$$$$  | $$           \____  $$| $$$$$$$$| $$        | $$    | $$| $$  \ $$| $$  \ $$
#    /$$  \ $$| $$  | $$| $$      | $$_  $$ | $$_____/  | $$ /$$       /$$  \ $$| $$_____/| $$        | $$ /$$| $$| $$  | $$| $$  | $$
#   |  $$$$$$/|  $$$$$$/|  $$$$$$$| $$ \  $$|  $$$$$$$  |  $$$$/      |  $$$$$$/|  $$$$$$$|  $$$$$$$  |  $$$$/| $$|  $$$$$$/| $$  | $$
#    \______/  \______/  \_______/|__/  \__/ \_______/   \___/         \______/  \_______/ \_______/   \___/  |__/ \______/ |__/  |__/

# Socket Endpoint for auth
@socketio.on('auth')
def handle_message(data):
    session_id = data.get('data')
    if session_id and session_id in user_stats:
        socket_sessions.append((session_id, request.sid))

        if user_stats[session_id]['regenerate'] == False:
            user_stats[session_id]['regenerate'] = True
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
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}
        
    session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

    if throttle(session):
        return {'error': 'Wait a bit before collecting again!', 'error_code': 2}

    if user_stats[session]['stamina'] <= 0:
        return {'error': 'No stamina left for collecting!', 'error_code': 1}

    user_stats[session]['stamina'] -= 10
    user_stats[session]['last_action'] = time.time()

    return {'stamina': user_stats[session]['stamina']}

# SocketEndpoint for attacking
@socketio.on('hunt')
def handle_message(data):
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

    return {'health': health - 10, 'stamina': stamina - 10}

# Socket Endpoint for training
@socketio.on('train')
def handle_message(data):
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}

    session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

    if throttle(session):
        return {'error': 'Wait a bit before training again!', 'error_code': 2}

    if user_stats[session]['stamina'] > 0:

        user_stats[session]['stamina'] -= 10
        user_stats[session]['last_action'] = time.time()
        return {'stamina': user_stats[session]['stamina']}

    else:
        return {'error': 'No stamina left for training!', 'error_code': 1, 'health': user_stats[session]['health'], 'stamina': user_stats[session]['stamina']}

# Socket Endpoint for travelling
@socketio.on('travel')
def handle_message(direction):
    if request.sid and any(request.sid == t[1] for t in socket_sessions):
        session = next((value[0] for value in socket_sessions if value[1] == request.sid), None)

        db = DBSession()

        # Load spawnpoint to check level requirement for travelling to another place 
        spawnpoint = db.query(models.User.spawnpoint).filter(models.User.username == user_stats[session]['username']).first()

        if user_stats[session]['current_place'][0] is not None and len(user_stats[session]['current_place'][0]) > 1:
            cur_place = user_stats[session]['current_place'][0]
        else:
            cur_place = user_stats[session]['current_place']

        # Determine next place to travel to from direction from request
        next_place = travel(direction.get('data'), cur_place)

        if next_place in error_msg:
            response_data = {
                'error': next_place,
                'dir': direction.get('data')
            }
        
        else:
            user_stats[session]['current_place'] = next_place
            response_data = {
                'next_place': next_place,
                'img_url': get_img(next_place),
                'dir': direction.get('data')
            }

            current_place = db.query(models.User).filter(models.User.username == user_stats[session]['username']).first()

            current_place.current_place = next_place
            db.commit()

    else:
        response_data = {
            'message': 'Authentication failed!',
            'status_code': 401
        }

    db.close()

    return response_data  

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    socketio.run(app)