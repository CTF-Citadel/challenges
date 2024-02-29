# Code Zip

## Description

```
Jake was just hired by a company who fired their former system administrator. He was very reluctant about giving out passwords to all the servers, but left a few code samples behind. 

Unfortunately its just some random python program that doesnt really do anything. If only there was a way to recover the password.
```

## Writeup

This is a really easy challenge for the trained eye that has worked with git before.

Sometimes developers forget things they add to code, for example secrets or access tokens.

By examining the downloaded `.zip` and extracting it, we can quickly observe that this is a git repository by executing f.E. `ls -la`

```bash
❯ unzip code.zip
# -- output omitted ---
❯ cd code/
❯ ls -la
total 36
drwxr-xr-x 4 user user  4096 Mar  1 00:24 .
drwxr-xr-x 3 k1f0 user  4096 Mar  1 00:25 ..
drwxr-xr-x 8 user user  4096 Mar  1 00:24 .git
# -- output omitted ---
```

Now we can dig deeper and think to ourselves what could have happened here, maybe we browse through the repo a bit and find a interesting file named `security.py`.

```py
import os

def check_password():
    expected_password = os.getenv("CIRCLE_CALCULATOR_PASSWORD")

    if not expected_password:
        raise ValueError("Password not set. Please set CIRCLE_CALCULATOR_PASSWORD environment variable.")

    password = input("Enter the password: ")
    return password == expected_password
```

Which seems to read a password from the environment. But remember what i said earlier, this is not the standard approach. Maybe going back in time will help?

```bash
❯ git log
# -- output omitted ---
commit 8e5d61425b916e0294892c9430a1f70963f3b70d
Author: bob <bob@security.org>
Date:   Sat Feb 9 08:16:00 2019 +0100

    add security.py
# -- output omitted ---
```

Let's see what the initial version of this file looked like, shouldn't we?

```bash
❯ git checkout 8e5d61425b916e0294892c9430a1f70963f3b70d
# -- output omitted ---
HEAD is now at 8e5d614 add security.py
❯ cat lib/security.py
def check_password():
    expected_password = "c3b74a03-b028-45a6-a6a5-32516b662b62"
    password = input("Enter the password: ")
    return password == expected_password
```

Well, that wasn't so hard, was it?
