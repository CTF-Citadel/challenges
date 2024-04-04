import random, uuid, os, time
from flask import *
from model.database import DBSession
from model import models
from datetime import datetime, timedelta
from flask_socketio import SocketIO
from game import *
from manage_sessions import *
from sqlalchemy import func

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

    return render_template('index.html', image_path=get_img(user_stats[request.cookies.get('session_token')]['current_place']))

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
                username=username, password_hash=sha256_hash(password), level=1, spawnpoint=spawnpoint, current_place=spawnpoint, affiliation=None, credits=0
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

        return {'message': 'Successfully authorized!', 'status_code': 200, 'health': user_stats[session_id]['health'], 'stamina': user_stats[session_id]['stamina']}
    else:
        return {'message': 'Authentication failed!', 'status_code': 401}

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


# SocketEndpoint for attacking
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

# Socket Endpoint for training
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

# Socket Endpoint for travelling
@socketio.on('travel')
def handle_message(direction):
    if request.sid not in (t[1] for t in socket_sessions):
        return {'auth': 'Authentication failed!', 'status_code': 401}

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
        db.close()
        return {'error': next_place, 'dir': direction.get('data')}
        
    user_stats[session]['current_place'] = next_place

    # Update new location in db
    current_place = db.query(models.User).filter(models.User.username == user_stats[session]['username']).first()
    current_place.current_place = next_place

    db.commit()
    db.close()

    return {'next_place': next_place, 'img_url': get_img(next_place), 'dir': direction.get('data')}

# Socket Endpoint for leaderboard updates
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

# Socket Endpoint to fetch user credits
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

# Socket Endpoint for Transferrng Credits
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

# Socket Endpoint for displaying current inventory
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

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    socketio.run(app)