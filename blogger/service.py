from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
import uuid, subprocess
from blog import posts

app = Flask(__name__)

users = {
    'Winkla': 'd0ck3rsw4rm'
}

sessions = []

def check_login(cookie):
    if cookie in sessions:
        return True
    else:
        return False

# Index page with login and signup links
@app.route('/')
def index():
    isLoggedIn = check_login(request.cookies.get('sid'))

    return render_template('index.html', posts=posts, display_login=not isLoggedIn)

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

@app.route('/blog', methods=['POST'])
def blog():
    isLoggedIn = check_login(request.cookies.get('sid'))

    if isLoggedIn == True:
        title = request.form['title']
        text = request.form['text']

        posts.append({
            "Author": "Winkla",
            "Title": title,
            "Content": text,
            "Socials": {
                "twitter": "https://twitter.com/bozo_kiss",
                "instagram": "https://www.instagram.com/mr__whoam.i/",
                "linkedin": "https://www.linkedin.com/in/jeff-delaney/"
            }
        })

        return render_template('dashboard.html', display_login=not isLoggedIn, blog_request_result="Post created successfully!")

    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')