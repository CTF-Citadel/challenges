# Behind the Curtain

> [!NOTE]
>
> I needed a simple web challenge to start off the web category, for this purpose I made this challenge with the most basic vulnerability there is. <br/>
> This challenge is about the issue of storing information on the client-side instead of server-side.

## Challenge Development

> [!NOTE]
> 
> For a better user experience every CTF challenge needs some kind of storyline. <br/>
> In this challenge I tried to build the storyline around some kind of online news platform providing a paid subscriber section. The vulnerability here is that the content is being loaded and just being hidden behind the paywall instead of being loaded separately.

For this challenge only 1 container is required to host the website. <br/>
```yml
version: '3.9'

services:
  flask:
    build:
      context: .
      args:
        FLAG: ${FLAG}
    restart: always
    ports:
      - "80:5000"
```

This `docker-compose.yml` file is used to host a flask service inside a container and load the flag from and envrionment variable. <br/>

The `Dockerfile` sets up the container with the latest python image and installs dependencies. <br/>
```docker
FROM python:latest

WORKDIR .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG FLAG
ENV FLAG=${FLAG}

EXPOSE 5000

CMD ["python3", "service.py"]
```

The `Python-Flask` service just provides the html files with the flag parameter on the `index.html` file. <br/>
```py
import os
from flask import Flask, render_template, request

app = Flask(__name__)

flag = f'TH{{{os.getenv("FLAG")}}}'

# Index Page
@app.route('/')
def index():
    return render_template('index.html', flag=flag)

# News Page
@app.route('/news')
def news():
    return render_template('news.html')

# Contact Page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return render_template('index.html', flag=flag)
    else:
        return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

The `index.html` file contains a simple paywall with the actual content being stacked behind the paywall. `{{ flag }}` loads the flag dynamically via `Flask`. <br/>
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Behind the Curtains</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 20px;
            text-align: center;
        }
        nav {
            background-color: #444;
            padding: 10px;
            text-align: center;
        }
        nav a {
            color: #fff;
            text-decoration: none;
            padding: 10px 20px;
            margin: 0 5px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        nav a:hover {
            background-color: #555;
        }
        .container {
            max-width: 800px;
            min-height: 400px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            position: relative; /* Added */
            z-index: 0; /* Added */
        }
        .paywall {
            background-color: #ffcc00;
            padding: 20px;
            margin-top: 20px;
            border-radius: 5px;
            position: relative; /* Added */
            z-index: 1; /* Added */
        }
        .paywall h2 {
            color: #333;
            margin-bottom: 10px;
        }
        .paywall p {
            color: #666;
        }
        .paywall form {
            margin-top: 10px;
        }
        .paywall button {
            background-color: #333;
            color: #fff;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .paywall button:hover {
            background-color: #444;
        }
        .content {
            width: 100%;
            text-align: center;
            position: absolute; 
            top: 40%; 
            left: 50%; 
            transform: translate(-50%, -50%);
            z-index: 0; 
        }
        .content h2 {
            color: #333;
        }
    </style>
</head>
<body>
    <header>
        <h1>Behind the Curtains</h1>
    </header>
    <nav>
        <a href="/">Home</a>
        <a href="/news">News</a>
        <a href="/contact">Contact</a>
    </nav>
    <div class="container">
        <h2>Welcome to Behind the Curtains</h2>
        <p>Discover exclusive stories and hidden secrets behind the scenes!</p>
        <div class="paywall">
            <h2>Exclusive Content</h2>
            <p>To access our premium content and uncover the hidden flag, please make a payment.</p>
            <form action="/">
                <input type="hidden">
                <button type="submit">Pay Now</button>
            </form>
        </div>
        <div class="content">
            <h2>{{ flag }}</h2>
        </div>
        <br/>
    </div>
</body>
</html>
```