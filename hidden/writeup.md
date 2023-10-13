# Introduction

Get started on the "Hidden" Image Challenge by downloading the image "wood.jpg." Then, delve into the challenge and reveal the cryptic secrets concealed within seemingly ordinary images. Can you decode the enigma and advance to the next level? 

Let's download the file and take a look at it!

![wood](https://github.com/CTF-Citadel/challenges/assets/115781703/c7b1b436-2a2f-49cd-91b5-dca11ab33cd0)

At first, we don't know what to do, so let's try and figure out something about the file's metadata.

Lets use the popular tool "steghide" with the command steghide --info 'file_name':

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/aad471b3-8eff-4140-8a91-f4746c5c63f4)


And we can see there's a 'goldnugget.txt' hidden inside. So, let's extract it using 'steghide extract -sf file_name':

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/189baa0f-019a-4994-9a38-d3cbf5f2cebd)

"We don't need to enter a passphrase to access the file. Now, you just need to see what's inside the file!

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/362c249b-b458-4db9-8069-12ee507b00bd)

There you go!
