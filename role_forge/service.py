from flask import Flask, render_template, request, redirect, url_for
import base64, json, os

app = Flask(__name__)

users = []

flag = "TH{" + str(os.environ.get("FLAG")) + "}" # build flag

# Function to add users to array
def add_user(username, password):
    user_data = {
        'username': username,
        'password': password
    }
    users.append(user_data)
    print(users)

# Simulate user authentication
def login(username, password):
    print(users)
    # Checking credentials stored in array "users"
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True

    return False

# Function to encode user information into a cookie
def generate_cookie(username, password):
    user_data = {
        'username': username,
        'password': password,
        'role': "user"
    }
    encoded_cookie = base64.b64encode(json.dumps(user_data).encode()).decode()
    return encoded_cookie

# Index page with login and signup links
@app.route('/')
def index():
    return render_template('index.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if login(username, password):
            response = redirect(url_for('index'))
            response.set_cookie('session', value=generate_cookie(username, password))
            return response
        else:
            return "Authentication failed."

    return render_template('login.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user["username"] == username:
                return f"Error: User '{username}' already exists."

        add_user(username, password)

        print(users)

        return redirect(url_for('login_route'))

    return render_template('signup.html')

# Endpoint for flag retrieval
@app.route('/developer')
def challenge():
    encoded_cookie = request.cookies.get('session')

    print(encoded_cookie)
    if encoded_cookie:
        decoded_cookie = base64.b64decode(encoded_cookie).decode()
        decoded_cookie = json.loads(decoded_cookie)
        print(decoded_cookie)
        if decoded_cookie["role"] == "developer":
            return render_template('developer.html', decoded_cookie=decoded_cookie, flag=flag)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
