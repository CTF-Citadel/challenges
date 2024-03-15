# lethimcook Walkthrough

## Introduction

We found a string, but we can't decipher it. Can you? When connecting to the IP and the port, we are met with a string that appears to be a basic Base64 encoding:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/fb8b34d3-aa12-4126-a234-40f49c011d98)

So let's go to CyberChef (https://cyberchef.org/) and enter our string. We'll use the 'magic' filter from the 'Operations' tab. The magic filter automatically tries to crack the string:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/648627fe-86a4-4931-87c1-2776299fd307)

And we get the flag!
