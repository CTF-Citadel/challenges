# Pcap Analysis

This traffic was caught by me on our network. Perhaps you could locate something?
Find anything that you mind find suspicious

##Solution
For this challenge we got a pcap file.
When we open it in Wireshark it looks like this:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/a96d864c-4397-41e5-9806-148513a531af)
We see something suspicious... evilcorp.com, what's that?

Next we filter for this suspicous source:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/054782c6-9d06-4c2f-9115-083eb1826739)

We export the filtered pcap file for a better overview:

![image](https://github.com/CTF-Citadel/challenges/assets/113849651/4fae5684-4cd0-44a5-8e74-66c5625d0962)

Next we use Kali Linux to extract usefull information from the new pcap file:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/616fd7bc-46d4-4a40-9e34-cb022f3bb27d)

With CyberChef we find the xml file:
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/34089662-73b2-43ba-966e-03f78b039cb0)
![image](https://github.com/CTF-Citadel/challenges/assets/113849651/7adf3f8f-488f-419d-ab26-e7df3a8967b4)

In the excel file we find the flag:

![image](https://github.com/CTF-Citadel/challenges/assets/113849651/a24fde01-273d-4087-b64e-4693f2e5dd81)
