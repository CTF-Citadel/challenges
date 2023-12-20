# FileNigma Walkthrough

## Introduction

We've stumbled upon a cluster of files, and hidden within it lies the flag. Can you uncover its location?

Let's go ahead and start the container, and we can see a bunch of files:
![image](https://github.com/CTF-Citadel/challenges/assets/115781703/5c85ed11-9c18-4a57-b5e0-4fbdfd2047ab)


Since we are searching for the flag with the format 'TH{,' we can use the following script to get the files:
```sh
#!/bin/bash

for i in {1..99}; do
        wget http://10.1.1.128/file_$i.txt
done
```
The script uses the "wget" command to get all the files to our local file system and then we can use the "grep" command to search for the flag format:

```sh
grep -ro 'TH{.*}' *
```

And we get the flag!





