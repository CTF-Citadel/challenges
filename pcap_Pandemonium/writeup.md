# Pcap Pandemonium

I captured this traffic from our network. I have been told that Marc from next door is using a testing user to access weird websites.
But I can't bruteforce his password. Maybe you can find something?

## Task

Find anything that you mind find suspicious

## Solution

Start the challenge by downloading the `capture.pcapng` file.
Damn, that is a big file. 

Let's try opening it in Wireshark

![image](https://github.com/CTF-Citadel/challenges/assets/66524685/c55bf494-eaa3-4814-a32c-097a177c1fa9)


Whoops! Ok, that won't work.

Maybe try the good old `strings`?

![image](https://github.com/CTF-Citadel/challenges/assets/66524685/9e69348c-080c-4a75-932d-0e4af73006fe)


Now we have a output! Let's try a combination with grep. We only have a few options for the username because it is a testing user: testuser, tester, test, testing, etc.

```Bash
patterns=("testuser" "tester" "test" "testing"); file_path="/path/to/capture.pcapng"; for pattern in "${patterns[@]}"; do echo "Searching for: $pattern"; strings "$file_path" | grep "$pattern"; done
```
![image](https://github.com/CTF-Citadel/challenges/assets/66524685/7e1c6356-07b1-471d-af5d-51bc13b9940d)

And we have our flag! (*might be different than your flag*)
`TH{f0e4d9e0a0f5458a9711727512fef7ac}`
