# Bella Italia

We have experienced a data breach, leading to the exposure of sensitive information. We must analyze various sources to uncover leaked data.
Utilize forensic analysis techniques to trace the hidden informations.
Investigate online platforms, forums, or databases where leaked information might be traded or shared.
Employ OSINT (Open Source Intelligence) methodologies to gather clues and piece together the extent of the breach.
You need to find out what got leaked.

Flag:{Leak}

All we got is this image:
![building](https://github.com/CTF-Citadel/challenges/assets/113849651/f560fe9d-9ad0-4e1c-b294-406253f2b1c4)

With a reverse image search we find out the building in question is the Palazzo Madama in Italy
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/5f173692-7b8f-470a-a323-bc944cea922f)

Next we look into the meta data of the image and find two hidden base64 messages:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/b7393371-bdf0-46c4-ad6e-07d6359709de)

Now we use CyberChef:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/f6124c39-7a12-4a01-bc56-7a53ec8da1b6)
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/c5411c14-4ca0-4cb7-9c78-1e0420bc1b91)


Next step we translate the information:

![image](https://github.com/CTF-Citadel/challenges/assets/113849651/efc2e46e-f277-4f69-841e-96bf15e13553)
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/37d5a351-184f-42fb-ab8b-5a1904477f3f)

After a quick Google search with the information given we find the person the hint is talking about:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/c70a35b9-67b9-46da-b95c-7cff4a6fa072)

The other hint was talking about needing followers, we found a account with 0 followers and a hidden message:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/3c988c8f-37f7-4a79-8daa-8444fc5099be)
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/be0b4c77-a294-4a75-bb4f-ba5e1549b18f)

The message we found:

![image](https://github.com/CTF-Citadel/challenges/assets/113849651/c0651bd5-a365-411a-a8be-f7eea131ee12)

What is something he could have lost?

Twitter is the solution for the problem:

![image](https://github.com/CTF-Citadel/challenges/assets/113849651/86ebfb49-8778-4480-8f94-92b5896646e6)

He lost something to lock something, lets search for Gasparri Maurizio Password

![image](https://github.com/CTF-Citadel/challenges/assets/113849651/defb8a91-672b-4946-87a3-73a69c80b13e)
We found the leaked information!
