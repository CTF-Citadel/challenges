# Social_chronicle Walkthrough

## Introduction
After reading the description, the most logical step is to access the provided domain 'winklersblog.net.' Upon accessing the domain, we see the following:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/7b056d35-4517-45b0-baf9-b30146c29c7e)


So there is not much we can deduce from that. After attempting some basic actions, such as checking the HTML code, we still can't find anything. However, the description mentioned that the blog post was seen a while ago, so perhaps we should check on the Wayback Machine (https://web.archive.org/)

After checking the domain on the Wayback Machine, we can see that it has been saved once. So, let's check that:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/44654aae-ef88-4046-8aa4-4ee0ad770a55)


The snapshot from the website:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/b7e6538e-cff9-41a8-9494-a2d9445bdb6f)


There is a lot of information in that blog post, but after reading through it, everything seems kind of useless except the last part: 'Anyway, if you want to find out more about my AI and how it works, make sure to join here: 1121776392359649290/1121776392833597552/1122243012668424222.' Let's try and figure out how to join that; it seems like a random string, but some people might recognize what it is. The pattern seems exactly like a Discord ID; the first ID is the server, the second is a channel ID, and the last one a message ID. So, let's try to convert the server ID so we can join it since it doesn't work pasting the link anywhere.

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/8b4260fb-5d99-4813-b0e8-5aab70e74b4d)

After some thorough searching and with a bit of experience, individuals may come across a tool known as 'Discord Snowflake.' This tool is capable of converting and extracting information from IDs. Now, all we need to do is find the appropriate converter.

I found this tool (https://discordtools.io/snowflake), and after converting the ID, I got the server invite:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/f9046ced-62a2-4105-9108-780665bbc6c6)

The server is called 'social_chronicle,' so let's join the Discord and see if we can find anything. At first glance, there isn't much to see except for some users. However, there is a Discord bot with the same name as mentioned before in the blog post, 'LostInThought':

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/db0839f0-6dd2-497b-b6c9-b41c03efccf5)

Let's message the bot, and we receive a reply:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/ae25df82-17c0-413a-a456-246229874b82)

It looks like a Caesar cipher, so we can decode it using dcode.fr:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/4f1f3d17-f680-4aec-a2a6-078ef8cc9869)

"I am the guardian of secrets, keeping them locked away. People trust me to secure their data night and day. I am strong and complex, yet vulnerable to a flaw. What am I?"

The answer to that should be obvious, so let's reply to the bot with 'Password':

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/30ba3b21-6011-4db5-8323-47e3cdf8b9ae)

We received another riddle, so let's decode it again and reply with the correct answer:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/a79c5a1f-d5fa-436f-ad88-9bb3d3143e5d)

"I am a vigilant guardian, shielding networks from danger. Intruders test my defenses, but I swiftly sound the alarm. I scrutinize data flow, sieving out the malevolent. With my protective measures, safety is assured. What am I?"

The answer should be 'Firewall':

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/49385145-0e9a-4509-98c7-07707e12e2d2)

And the last riddle:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/bcb5f758-b7e4-43b0-af1b-88fda13a4823)

"I lurk in the shadows, unseen and unknown. Exploiting weaknesses, my presence is never shown. I infiltrate networks, spreading like a plague. A malicious force, causing havoc at my stage. What am I?"

Answer with 'Malware', and we get the flag:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/0bf96a15-2d0f-421e-9f85-e1f61c6784fe)

