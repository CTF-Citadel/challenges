# The Blogger

> [!NOTE]
>
> This Web-Challenge consists of 2 stages. 
> The first stage is simple OSINT on social media account which is hidden on the website.
> The second stage is about executing SSRF on the admin-dashboard.

## Challenge Development

To automate the challenge I first setup a `docker-compose.yml` file. <br/>
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

In the compose file I export the port `5000` which is the internal `Flask` service to the external port `80`. <br/>
The flag is being passed as `ARG` in the compose file. <br/>
The `Dockerfile` sets up a python container to host a `Flask service`. <br/>
```docker
FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG FLAG

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN echo "Here, grab your flag: TH{${FLAG}}" > /root/flag.txt

EXPOSE 5000

CMD ["python", "service.py"]
```

In the `Dockerfile` the `flag` is being written to a file in a common directory with common syntax. <br/>
The `Flask` application contains several endpoints, two of which serve no functional purpose beyond aesthetic design. <br/>
```py
@app.route('/about')
def about():
    isLoggedIn = check_login(request.cookies.get('sid'))

    return render_template('about.html', display_login=not isLoggedIn)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    isLoggedIn = check_login(request.cookies.get('sid'))

    if request.method == 'POST':
        status = 'Request successfully submitted'
        return render_template('contact.html', display_login=not isLoggedIn, status=status)
    
    return render_template('contact.html', display_login=not isLoggedIn)
```

The index page takes an array which contains different posts and renders each of them. <br/>
```py
@app.route('/')
def index():
    isLoggedIn = check_login(request.cookies.get('sid'))

    return render_template('index.html', posts=posts, display_login=not isLoggedIn)
```

Using the `index.html` template several posts get rendered onto the webpge. <br/>
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="../static/style.css">
    <script src="https://kit.fontawesome.com/b7b4b27f8b.js" crossorigin="anonymous"></script>
    <title>R4P1D-BL0G</title>
</head>
<body>
    <nav id="navBar">
        <a class="navTitle" href="/">R4P1D-BL0G</a>
        <div class="navLinks">
            {% if not display_login %}
            <a class="navLink" href="/dashboard">Dashboard</a>
            {% endif %}
            {% if display_login %}
            <a class="navLink" href="/login">Login</a>
            {% endif %}
            <a class="navLink" href="/about">About</a>
            <a class="navLink" href="/contact">Contact</a>
        </div>
    </nav>

    <div id="posts">
        {% for post in posts %}
            <div class="postContainer">
                <h1 style="margin-top: 10px; margin-bottom: 10px;">{{ post.Title }}</h1>
                <p>{{ post.Content }}</p>
                <div class="postBottom">
                    <div class="author-info">Written by: {{ post.Author }}</div>
                    <ul class="social-icons">
                        <li><a href="{{ post.Socials.twitter }}" target="_blank"><i class="fab fa-twitter"></i></a></li>
                        <li><a href="{{ post.Socials.instagram }}" target="_blank"><i class="fab fa-instagram"></i></a></li>
                        <li><a href="{{ post.Socials.linkedin }}" target="_blank"><i class="fab fa-linkedin"></i></a></li>
                    </ul>
                </div>
            </div>
        {% endfor %}
    </div>
</body>
</html>
```

The posts array can be seen below. <br/>
```py
posts = [
    {
        "Author": "Test",
        "Title": "Test",
        "Content": "Test",
        "Socials": {
            "twitter": "https://twitter.com/Test",
            "instagram": "https://www.instagram.com/Test/",
            "linkedin": "https://www.linkedin.com/in/Test/"
        }
    },

    # -----------------------
]
```

To gain access to the admin dashboard a user first needs to login. <br/>
```py
@app.route('/login', methods=['GET', 'POST'])
def login():
    isLoggedIn = check_login(request.cookies.get('sid'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:

            response = make_response(redirect(url_for('index')))
            new_session = str(uuid.uuid4())
            sessions.append(new_session)
            response.set_cookie('sid', new_session)

            return response
        
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    
    return render_template('login.html', display_login=not isLoggedIn)
```

because this is a simple application the `user` is just being stored in a dictionary. <br/>
```py
users = {
    'Test': 'd0ck3rsw4rm'
}
```

After login the sessiosn are being stored in an array to verify the current session. <br/>
```py
sessions = []

def check_login(cookie):
    if cookie in sessions:
        return True
    else:
        return False
```

The `/dashboard` endpoint holds the main web-vulnerability which is `SSRF`. <br/>
```py
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    isLoggedIn = check_login(request.cookies.get('sid'))

    if isLoggedIn == False:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        url = request.form['url']

        try:
            output = subprocess.check_output(['curl', url])
            response = output.decode('utf-8')

        except subprocess.CalledProcessError:
            response = 'An error ocurred while sending the request!'

        return render_template('dashboard.html', display_login=not isLoggedIn, request_result=response)
    
    return render_template('dashboard.html', display_login=not isLoggedIn, request_result='')
```

To implement the vulnerability I added an option to curl an `URL`. <br/>
Because the protocol can be altered an end-user can simply read local files via `file:///etc/passwd`. <br/>

To add some realism to the webpage I also added another endpoint which is only accessible to authenticated users. <br/>
The `/blog` endpoint allows the addition of blog posts. <br/>
```py
@app.route('/blog', methods=['POST'])
def blog():
    isLoggedIn = check_login(request.cookies.get('sid'))

    if isLoggedIn == True:
        title = request.form['title']
        text = request.form['text']

        posts.append({
            "Author": "Test",
            "Title": title,
            "Content": text,
            "Socials": {
                "twitter": "https://twitter.com/Test",
                "instagram": "https://www.instagram.com/Test/",
                "linkedin": "https://www.linkedin.com/in/Test/"
            }
        })

        return render_template('dashboard.html', display_login=not isLoggedIn, blog_request_result="Post created successfully!")

    else:
        return redirect(url_for('index'))
```

There is of course the option to insert `HTML` code into the post and therefore creates a `Cross-Site-Scripting` vulnerability, but this shouldn't be the focus as there is no way to really exploit it in the challenge. <br/>
