# Introduction

Get started on the "Hidden" Image Challenge by downloading the image "wood.jpg." Then, delve into the challenge and reveal the cryptic secrets concealed within seemingly ordinary images. Can you decode the enigma and advance to the next level? 

Let's acces 127.0.0.1:8080 and download the file!

![wood](https://github.com/CTF-Citadel/challenges/assets/115781703/c7b1b436-2a2f-49cd-91b5-dca11ab33cd0)

At first, we don't know what to do, so let's try and figure out something about the file's metadata.

Lets use the popular tool "steghide" with the command steghide --info 'file_name':

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/e3faf4d5-1769-4cf7-b3ce-eaa4f9a62f23)

The issue we run into is that the image has a passphrase we don't know. So, I am going to use StegCracker to try and brute-force it (https://github.com/Paradoxis/StegCracker)."

We use the command "stegracker <filename> <wordlist> and we can see it finds the password quite quickly:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/dd901e3a-d023-4b86-8ebb-628e7f1447b3)

Now we just need to see whats inside the "wood.jpeg.out"

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/2c472a15-8592-47cd-8244-71c78d76c869)




There you go!
