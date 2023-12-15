# AI-Banking

> [!NOTE]
>
> When brainstorming I got the idea of a relatively simple challenge focusing on `SQL-injection`. <br/>
> Instead of using simple MySQL I wanted to use a DB which has a slightly different SQL syntax.

## Challenge Development

> [!NOTE]
> 
> For a better user experience every CTF challenge needs some kind of storyline. <br/>
> In this challenge I tried to build the storyline around some kind of Banking Web Application which has a security flaw. 

I used three different containers for this challenge. <br/>

The three containers are the following:
- Backend: Flask-API for authentication and access to database
- Frontend: React-App for WebGUIand accessing API
- Database: Storing user data and flag

```yml
version: "3"

services:
  db:
    image: mariadb:latest
    hostname: db
    restart: always
    environment:
      MARIADB_ROOT_PASSWORD: 2U3Qps4cDZHJJT8LgnJR
      MARIADB_DATABASE: users
      MARIADB_USER: dbadmin
      MARIADB_PASSWORD: eEGnsF5JrDFfNB88LMxR

  flask_app:
    image: python:3.9-slim
    build:
      context: .
      dockerfile: Dockerfile_PY
    hostname: flask-app
    command: ["python3", "service.py"]
    depends_on:
      - db
    environment:
      DB_USER: dbadmin
      DB_PW: eEGnsF5JrDFfNB88LMxR
      DB_NAME: users
      FLAG: ${FLAG}
    restart: always

  react_app:
    build:
      context: ./react_app
      dockerfile: Dockerfile_REACT
    ports:
      - "80:80"
    command: sh -c "sleep 5 && nginx -g 'daemon off;'"
```

In this `docker-compose.yml` file I hardcode a lot of things. <br/>
The reason for this is that it doesn't matter. All the services are not exposed to the outside. <br/>
The names of the environment variables are simple and state what their usage is. <br/>

## Frontend

In the frontend I used the REACT framework. <br/>
The purpose of the frontend is to make a nice looking UI for users to neatly access the backend endpoints. <br/>
For this web challenge I wanted people to use a directory scanner to find `/robots.txt` which is a keyfile in web-hacking. <br/>
Other important paths are `/login`, `/signup` and others. <br/>
I again created a lot of unimportant information to get a good storyline together. <br/>
Other less important key features are responsive designs, a footer and navbar which old information like fake copyright and fake contact information.

A thing to keep in mind is that the same container where the REACT-App is running hosting a Nginx Proxy. <br/>
```conf
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://flask-app:5000;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
``` 

The `Nginx` webserver is basically redirecting every normal request to the REACT-App and every request going to `/api/` to the backend container. <br/>
This does act as a normal security measure and is common practice for hosting container stacks. <br/>

REACT-App Dockerfile:
```Dockerfile
# Use the official Node.js image 
FROM node:14 as build-stage

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json and package-lock.json (This is to get dependencies like requirements.txt)
COPY package*.json ./

# Install the app dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Build React app
RUN npm run build

# Use the official Nginx image 
FROM nginx:latest

# Copy the custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy the build output from the previous stage to the Nginx public directory
COPY --from=build-stage /app/build /usr/share/nginx/html

# Expose port 80 (the default port used by Nginx)
EXPOSE 80

# Start Nginx when the container runs
CMD ["nginx", "-g", "daemon off;"]
```

The comments should give information about each command. <br/>
To get more authenticity I used `https://github.com/Aryt3/AIGen` to generate some images for the website. <br/>

The `/robots.txt` holds key information to solve the challenge. <br/>
```
User-agent: *
Disallow: /

Email: admin@tophack.at
```

This email should be used to login and read the flag. <br/>
I won't go into detail about the frontend code because most of it is just about styling features or simple axios requests. 

## Backend

In the backend I used Flask as API which is just the interface for interacting with the frontend but also with the database. <br/>
I used three main API endpoints and one function to initialize the flag. <br/>

```py
@app.route('/api/login', methods=['POST'])
def login():
    db = DBSession() # open session with database
    try:
        data = request.get_json()
        email = data.get('email', '') # get email from json request
        password = data.get('password', '') # get password from json request

        emails = db.query(models.User).filter(models.User.email == email).all() # search if the email even exists

        if not emails:
            return jsonify({'message': 'No Such Email Found!'}), 404 # if email wasn't found don't even send the request

        query = text(f"SELECT email FROM accounts WHERE email='{email}' AND password='{password}'") # if email exists send this select query

        with engine.connect() as con: # to directly execute queries we need to open a database session this way
            rs = con.execute(query) # execute query kinda like requests.get()

            rows = rs.fetchall() # format fetched data

            email_exists = any(row[0] == email for row in rows) # check if we got an email back

            if email_exists: 
                session_token = generate_session_token() # generate session cookie

                sessions[session_token] = { # store session cookie
                    'email': email
                }

                expiration_date = datetime.now() + timedelta(minutes=10) # let cookie expire in 10min
                response = jsonify({'message': 'Login successful!'}) # return json response
                response.set_cookie('session_token', session_token, expires=expiration_date, samesite='Strict') # pass cookie in response
                return response
            else:
                return jsonify({'message': 'Login failed!'}), 401 # return auth error if email doesn't exist

    except Exception as e:
        return jsonify({'error': 'An error occured'}), 500
```

Now this API endpoint should handle login requests and includes the critical vulnerability of the challenge. <br/>
The `SQL-Injection` vulnerability is being implemenited via the `query`. <br/>
The reason this vulnerability occurs is that the user input doesn't get sanitized and the query is getting passed to db as is which is a crucial issue in any application. <br/>

```py
@app.route('/api/signup', methods=['POST'])
def signup():
    db = DBSession() # open session with database

    data = request.get_json()
    email = data.get('email', '') # get email from json request
    password = data.get('password', '') # get password from json request

    emails = db.query(models.User).filter(models.User.email == email).all() # Check if email already exists

    if emails:
        return jsonify({'error': 'A user with this email does already exist!'}), 401 # response if user already exists

    try: # create new user
        new_user = models.User( 
        email=email, password=password, balance=0, notes="V3IwbmdVczNy" # Addign small hint to default user creation
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.close()
        return jsonify({'error': 'User successfully created!'}), 200 # return successful response

    except Exception as e:
        return jsonify({'error': 'An error occured'}), 500
```

Now this API endpoint should handle signup requests which is not really needed for the challenge but adds some authenticity. <br/>

```py
@app.route('/api/data', methods=['GET'])
def data():
    session_token = request.cookies.get('session_token') # Check if user has a session cookie

    if not session_token:
        return jsonify({'error': 'No Open-Session Found!'}), 500 # If no cookie found return error

    db = DBSession() # open session with db

    try:
        email = sessions[session_token].get('email') # from session cookie get email
        user = db.query(models.User).filter(models.User.email == email).first() # query user information

        if user: # format user information from query
            user_data = {
                'email': user.email,
                'balance': user.balance,
                'notes': user.notes
            }

            return jsonify(user_data) # return formated data as json
        else:
            return jsonify({'error': 'You dare fiddling with my API?!?!?!'}), 404 # custom error code if they directly try to attack API

    except Exception as e:
        db.close()
        return jsonify({'error': str(e)}), 500
```

Now this API endpoint returns user information which returns the flag if the correct user is logged in. <br/>
Another important function is the flag implementation. <br/>
```py
def init_flag():
    db = DBSession() # open session with database

    flag = os.environ.get("FLAG") # get flag from environment variable

    random_password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10)) # create "random" password for account

    new_user = models.User( # create the new user locally
        email='admin@tophack.at', password=random_password, balance=876582, notes="TH{" + flag + "}"
    )
    db.add(new_user) # commit new entry to db
    db.commit()
    db.refresh(new_user)
    db.close()
```

This function is called once when the script is run during deployment which creates the flag and pushes it into the database. <br/>
For the communication with the database I decided to use `sqlalchemy` because I was already familiar with it. <br/>
