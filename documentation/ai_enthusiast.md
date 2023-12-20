# AI-Enthusiast 

> [!NOTE]
>
> When brainstorming for the challenge idea, we wanted to go with an AI theme. We developed a storyline and created an Instagram account for an individual named 'ailover123_.' His entire account revolves around his self-made AI and the pictures he has created with it.
> To add a touch of realism, we utilized AI images generated with this repository (https://github.com/Aryt3/AIGen). We crafted 10 distinct images using the AI and posted them on the AI-themed Instagram account:
> ![image](https://github.com/CTF-Citadel/challenges/assets/115781703/e1d61e5e-e953-4977-b2eb-b8e3d9a36c99)


## Challenge creation

"After creating the account, we also needed fitting descriptions. Therefore, we asked ChatGPT to create picture descriptions for a person who loves their AI and the pictures it produces. Consequently, all the descriptions emphasize again how good the AI is and how beautiful the pictures look when created by it.
 
![image](https://github.com/CTF-Citadel/challenges/assets/115781703/915ca544-aa6d-41f0-afcb-c01a9936b070)

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/c1d7e4de-41d1-4315-b6b3-1fb5365bb5c5)


"We created 10 different descriptions and posted them under the pictures. Now, we needed a challenge, a puzzle, or something for the user to solve. So, we created another account called 'quandaledingle7600.' We came up with the idea that the newly created Instagram account would post comments under every Instagram post, including spelling mistakes. Combining those spelling mistakes would lead to a username. The issue with that is that it's hard to figure out, so we wanted to give everyone a little hint by including the following Base64 string in the profile description of 'quandaledingle7600':"

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/c3ec76e7-6be1-4d0a-b8c3-799ee9316020)


Hinting that "quandaledingle7600" is very confident in his English skills and would never make spelling mistakes. Now, some people might take a close look at his comments and spelling. The comments under the images were also created using ChatGPT, and the spelling mistakes were done by ourselves. We picked easier words and included obvious spelling mistakes so they can be found more easily by the user.

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/edaa032b-dfc0-4008-9a99-23e2474be8e0)


"Now that we found a new user by combining the spelling mistakes, we needed an account to lead the user to. So, we decided to create a GitHub account. The GitHub account was also made to fit the AI theme by pushing two repositories, 'Secret-Ai-Code' and 'Ai-Optimization,' also using an AI-created image as a profile picture. Making it seem like it's the GitHub account of 'ailover123' since he was always bragging about how good his AI is."

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/30c6f1ba-fd46-404a-b37b-e99f192a5d56)


"To lead the user to search on GitHub with the username found, we simply followed only 'github' on the Instagram account, which gives the user a little hint as well."

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/0e23d80e-dc8d-4ac7-aa56-f49e9ffc85d5)


"Now that the user is able to find the GitHub account, we just needed to add another small puzzle for the user to be able to find the flag. We decided to push four different files with code inside and asked the user to figure out what kind of programming language is used. To throw the user off a little, we changed the endings of the files to a different one than the programming language that was actually used:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/6548bf56-5154-4a06-9245-2bf08b2b10c2)


To generate the code used in the files, we requested ChatGPT to write a simple program in the 'programming language' and committed it to the repository.

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/cce3db50-73aa-4e21-9702-81b89c54f574)


Obviously, anyone can copy the code into any AI and ask what programming language it's written in. However, we still wanted to provide some hints regarding the potential programming language by writing hints in the commits. For example:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/3d0f3956-27fd-4b60-89f2-1fc5c1c96fca)

"I have heard Roblox games are written in this language," hinting that it's written in 'Lua'.


And to add one last little challenge for the user, we decided to delete one of the files. This way, the user would have to look at the commit history and find the deleted file there to combine everything and get the flag:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/fd7ae34a-5ab7-486d-b845-0552594104c9)


> [!NOTE]
> In conclusion, we aimed to create an AI-themed OSINT challenge, incorporating numerous AI-created images and elements to immerse the user in the challenge. Our goal was to give the user a genuine sense of an account belonging to someone who truly loves their AI.

