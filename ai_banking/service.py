from flask import Flask, request, jsonify
from model.database import DBSession, engine
from model import models
import os, uuid, secrets, string
from flask_cors import CORS 
from datetime import datetime, timedelta
from sqlalchemy import text

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "supports_credentials": True}})  # Allow any origin

sessions = {}

def generate_session_token():
    return str(uuid.uuid4())  # Generate a random session token using UUID

def init_flag():
    db = DBSession()

    emails = db.query(models.User).filter(models.User.email == "admin@tophack.at").all()

    if emails:
        return

    flag = os.environ.get("FLAG")

    random_password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))

    new_user = models.User(
        email='admin@tophack.at', password=random_password, balance=876582, notes="TH{" + flag + "}"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

init_flag()

@app.route('/api/login', methods=['POST'])
def login():
    db = DBSession()
    try:
        data = request.get_json()
        email = data.get('email', '')
        password = data.get('password', '')

        emails = db.query(models.User).filter(models.User.email == email).all()

        if not emails:
            return jsonify({'message': 'No Such Email Found!'}), 404

        query = text(f"SELECT email FROM accounts WHERE email='{email}' AND password='{password}'")

        with engine.connect() as con:
            rs = con.execute(query)

            rows = rs.fetchall()

            email_exists = any(row[0] == email for row in rows)

            if email_exists:
                session_token = generate_session_token()

                sessions[session_token] = {
                    'email': email
                }

                expiration_date = datetime.now() + timedelta(minutes=10)
                response = jsonify({'message': 'Login successful!'})
                response.set_cookie('session_token', session_token, expires=expiration_date, samesite='Strict')
                return response
            else:
                return jsonify({'message': 'Login failed!'}), 401

    except Exception as e:
        return jsonify({'error': 'An error occured'}), 500


@app.route('/api/signup', methods=['POST'])
def signup():
    db = DBSession()

    data = request.get_json()
    email = data.get('email', '')
    password = data.get('password', '')

    emails = db.query(models.User).filter(models.User.email == email).all()

    if emails:
        return jsonify({'error': 'A user with this email does already exist!'}), 401

    try:
        new_user = models.User(
        email=email, password=password, balance=0, notes="V3IwbmdVczNy"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
        return jsonify({'error': 'User successfully created!'}), 200

    except Exception as e:
        return jsonify({'error': 'An error occured'}), 500


@app.route('/api/data', methods=['GET'])
def data():
    session_token = request.cookies.get('session_token')

    if not session_token:
        return jsonify({'error': 'No Open-Session Found!'}), 500

    db = DBSession()

    try:
        email = sessions[session_token].get('email')
        user = db.query(models.User).filter(models.User.email == email).first()

        if user:
            user_data = {
                'email': user.email,
                'balance': user.balance,
                'notes': user.notes
            }

            return jsonify(user_data)
        else:
            return jsonify({'error': 'You dare fiddling with my API?!?!?!'}), 404

    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)