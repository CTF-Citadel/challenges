# Shadow Gateway

> [!NOTE]
>
> I got the idea of this challenge when taking part in huntress-CTF earlier in october 2023. <br/>
> The main focus in this challenge is to find out that you are able to manipulate the cookie to access a certain webpage. 

## Challenge Development

> [!NOTE]
> 
> I wanted this challenge to be the entrypoint to web challenges meaning this should be the easiest one. 

Starting off I needed a simple webservice to host this challenge. <br/>
After brainstorming I decided on using `Flask` because it easy a pretty lightweight webframework and was even created by an austrian coder. <br/>
```yml
version: '3.9'

services:
  web:
    build: .
    ports:
      - "80:5000"
    environment:
      FLAG: ${FLAG}
```

I only needed 1 container to host this website and to not change too much I used the default port `5000` from flask and exposed it to default http `80`. <br/>
The flag is of course loaded via environment variable. <br/>

The most important piece of this webservice is of course the Flask service. <br/>
```py
from flask import Flask, render_template, request, redirect, url_for
import base64, json, os

app = Flask(__name__)

users = []

flag = "TH{" + os.environ.get("FLAG") + "}" # build flag

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
```

I used 4 different endpoints in this script (Every endpoint does also have a html template). 
- `/` -> Index-Page of the website
- `/login` -> Webpage for login purpose
- `/signup` -> Webpage for signup purpose
- `/developer` -> Webpage for flag retrieval

Another thing to keep in mind is that I stored users locally because it would be unnecessary to store them elsewhere. <br/>
The main goal is to find out that the cookie when logged in gets `base64` encoded which is the standard encoding for web stuff. <br/>
If decoded a user should see something like the json stuff below. <br/>
```json
{
'username': "user123",
'password': "password123",
'role': "user"
}
```

Of course just changing hte cookie would be pretty bland that's why the participants must also do a directory scan on the website first- <br/>
There they should find `/developer` which is a webpage which can't be accessed without a cookie containing the role `developer`. <br/>
Because this should be the easiest web challenge I included a `clue` which can be found on the index page in form of a comment in the html. <br/>
```html
<!DOCTYPE html>
<html>
<head>
    <title>Role-Forge</title>
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='./style.css') }}">
</head>
<body>
    <div id="mainSection">
        <h2>Deluxe Forge</h2>
        <br/>
        <p><a href="{{ url_for('login_route') }}">Login</a></p>
        <p><a href="{{ url_for('signup') }}">Signup</a></p>
    </div>
    <!-- Note from developer: We need to fix access to dashboard, apparently admin role doesn't have access to it! -->
</body>
</html>
```

The other important functions of the flask service are as follows. <br/>
The different endpoints apply the usage of the flask inbuild function `render_template` to render the templates being found in `/templates`. <br/>
For authentication we simply use the base64 encoded cookies and user credentials stored in plaintext inside the cookie. <br/>


