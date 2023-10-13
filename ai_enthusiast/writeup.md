# AI-Enthusiast Walkthrough

## Introduction:
Welcome to the OSINT (Open-Source Intelligence) Puzzle: 'The AI Enthusiast!'
In this captivating online challenge, you will embark on a thrilling search across the
vast expanse of the internet to uncover the secrets of a passionate individual known
only by the username "ailover123_". Your mission is to gather information about this
enigmatic person who loves sharing captivating pictures from their self-made AI.


So, starting with the introduction, we can infer that we need to gather information
about an individual named 'ailover123_' Searching on different social media
accounts will eventually lead us to this Instagram account
(https://www.instagram.com/ailover123_/):
![image](https://github.com/CTF-Citadel/challenges/assets/115781703/14100eb7-c677-4eef-bd7b-42219182681c)


While going through the account, we can figure out some details. Let's begin by
examining the comments and picture descriptions. One noticeable pattern is that
beneath every post, an individual named 'quandaledingle7600' wrote a comment:
![image](https://github.com/CTF-Citadel/challenges/assets/115781703/cf6e0d1d-846c-43d5-93a3-04d8e6aac825)


In their Instagram profile description, there appears to be something encrypted. It
resembles Base64, but you can use https://www.boxentriq.com/codebreaking/
cipher-identifier to decipher it:
![image](https://github.com/CTF-Citadel/challenges/assets/115781703/4acb70a5-0c42-47db-b58e-93e5de9a67d6)

So, let's decrypt it by inputting it into https://gchq.github.io/CyberChef/. When
using Base64, we quickly obtain this result:
![image](https://github.com/CTF-Citadel/challenges/assets/115781703/d1da13d1-947f-4a5c-8045-8faf5e200b39)

It says, 'I studied English at Harvard, so I am really confident in my skills.' This could
be a hint. Let's also revisit the other Instagram account.

Looking at the first post, we quickly notice a spelling mistake in the comment from
'quandaledingle7600.' It says 'recist' instead of 'resist'.
![image](https://github.com/CTF-Citadel/challenges/assets/115781703/6dfd3b04-d712-4078-9437-001c63c11aaa)

Let's write down the 's' for now and see where this takes us.

Let's check out every other post and find the spelling mistakes there:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/2335b7e5-9902-4fd4-8b9a-8504f2d6d4ef)
  
“muntain” instead of “mountain”. So we write down the “o”


![image](https://github.com/CTF-Citadel/challenges/assets/115781703/dbb92f40-70ca-4d5a-bf1c-397f2bdb9e43)

“ceptivating” instead of “captivating. So we write down the “a”.


![image](https://github.com/CTF-Citadel/challenges/assets/115781703/c76d8370-3621-441e-a67a-67174fcf1ab9)

“fhoto” instead of “photo”. so we write down the “p”.


 ![image](https://github.com/CTF-Citadel/challenges/assets/115781703/95435134-7bfa-41f1-aa7a-894aeea1fbde)

“vorld” instead of “world. So we write down the “w”.


![image](https://github.com/CTF-Citadel/challenges/assets/115781703/40d3fd21-5c11-4233-ab90-7188d369c547)
  
“holt” instead of “hold”. So we write down the “d”.


![image](https://github.com/CTF-Citadel/challenges/assets/115781703/26ec9018-35a9-4858-901b-d7138a5ea1eb)

The “j” is missing in “maiesty”. So we write down the “j”.


![image](https://github.com/CTF-Citadel/challenges/assets/115781703/c45f3225-41a8-486e-bb3e-a3ce71555b46)
  
“vondrous” instead of “wondrous”. So we write down the “w”.


![image](https://github.com/CTF-Citadel/challenges/assets/115781703/8d613537-8abb-4b5c-ad4d-ea1e6eae3ed6)

“testament” instead of “tesdament”. So we write down the “t”.


![image](https://github.com/CTF-Citadel/challenges/assets/115781703/a10d9cc3-31c3-4408-808a-b8b2a366bb30)

“skyscreper” instead of “skyscraper”. So we write down the “a”.

Putting all of these together at the end, we get 'soapwdjwta.' Maybe a social media
account name? Let's see who he is following:
![image](https://github.com/CTF-Citadel/challenges/assets/115781703/60c8c32e-4d57-45a8-ad36-5e89a0382214)

Since he is only follwing github, lets try and search the User name there:
![image](https://github.com/CTF-Citadel/challenges/assets/115781703/9bc8773d-ef66-4f5e-af3e-3aae18866c49)
![image](https://github.com/CTF-Citadel/challenges/assets/115781703/a1370bde-dc0c-497d-8f81-4f6469831b08)

We find this account ‘https://github.com/soapwdjwta’.

"Let's look at the 'Ai-optimization' repository first:
  ![image](https://github.com/CTF-Citadel/challenges/assets/115781703/4c010de0-7e55-4ac1-89a1-95f7f6e34fd8)


We found three files and a README.md that says 'Figure out the flag by combining
the programming languages of the committed files CTF{File_1, File_2, File_3,
File_4}.’ So lets do that!

We can simply paste the code into ChatGPT and ask it to identify the programming
language. I'm sure you can figure that out yourself.

The only thing missing is “File_1”, so w´here could that be? Lets look at the commits:
![image](https://github.com/CTF-Citadel/challenges/assets/115781703/d941f9e4-3c36-4d5f-bec0-916821d4e594)

"And we can see that 'File_1.txt' got deleted, so we need to find it here.

By combining these, we can obtain the flag!
