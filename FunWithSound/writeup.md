# FunWithSound

Welcome to the Steganography Puzzle: 'FunWithSound'
I believe my best friend Wayne might be in danger since he sent me an odd audio file. 
Are there any traces of information in the file that was provided?


Flag:{Information}

If we listen to the wav file it sound like weird noise what could this mean:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/9e660c9e-32cd-44e9-a6db-08a9a09ece8b)

Perhaps there's something unseen behind the noise that we can't hear, just see.
We need to use a software called "Audacity" to look at the Spectogram:

![image](https://github.com/CTF-Citadel/challenges/assets/113849651/a72d1416-f8be-4e9d-a5e7-cd2cb5f8d77e)

If we import the file it looks like this:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/e04d991f-9ca6-4ec5-b77d-21dc8654f3b7)
Not much to see here, what now?

We need to click on the arrow next to the name of the file an choose the option "Spectogram":

![image](https://github.com/CTF-Citadel/challenges/assets/113849651/f1b79107-5737-4932-98dd-08a0be2f77ae)

This looks odd:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/46eb9aac-6aff-4cb0-9ba9-00e2458874f3)

A little tinkering with the zoom reveals that there is concealed morse code.
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/a5b80482-0100-4eca-94c4-1d4c8c72c31c)

The flag appears when we enter the recently found morse code into a translator:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/826c9cdc-4f85-4b91-9a2b-948f3ca31d38)
