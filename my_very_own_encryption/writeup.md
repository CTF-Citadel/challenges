## Shadow Gateway

## Description
```
A second grader is proudly flexing his new encryption algorithm which he made during an ITP project. 

Can you humble the second grader by breaking his encryption?
```

## Writeup

Starting off we should take a look at the provided files. <br/>
```py
import os, base64, random

flag = "TH{" + str(os.environ.get("FLAG")) + "}"

def encrypt(flag):
    encoded_flag = list(bytes(flag, 'utf-8').hex())
    print(encoded_flag)

    for _ in range(99999):
        rndm_index_num = random.randrange(1,10)
        rndm_index_letter = random.randrange(1,26)
        for index, char in enumerate(encoded_flag):
            if char.isdigit():
                if char != 9:
                    num = int(char)
                    num %= (9 + rndm_index_num)
                    encoded_flag[index] = str(num)
            else:
                encoded_flag[index] = chr((ord(char) - ord('a') + rndm_index_letter) % 26 + ord('a'))

    print(encoded_flag)
    return base64.b64encode(bytes(''.join(encoded_flag), 'utf-8'))

with open('output', 'wb') as file: 
    file.write(encrypt(flag))
```

The important things to keep in mind are the different encryption/encoding stages. <br/>
After transforming the actual flag to a `hex` string the characters are being shifted randomly. <br/>
The important thing here is that they are being shifted equally which tells us that we are able to bruteforce it. <br/>
Knowing these steps anybody should be able to code a small script to decrypt the flag. <br/>
```py
import base64

for line in open("output", "r"):
    encrypted_flag = line

encrypted_flag = bytes.decode(base64.b64decode(encrypted_flag), "utf-8")
array = list(encrypted_flag)

for i1 in range(1, 26):
    arr_copy = array.copy() 
    for i2 in range(1, 11):
        for index, char in enumerate(arr_copy):
            if char.isdigit():
                num = int(char)
                num %= (9 + i2)
                arr_copy[index] = str(num)
            else:
                arr_copy[index] = chr((ord(str(char)) - ord('a') + i1) % 26 + ord('a'))
        
        try:
            yeet = bytes.fromhex(''.join(arr_copy)).decode('utf-8')
            if yeet.startswith("TH{"):
                print(yeet)
                break

        except ValueError:
            pass
```

In the script I first convert the file output to a hex string. <br/>
I than bruteforce the correct flag by looping through the letters and try out every possible one and for each letter-shift I bruteforce every possible number shift. <br/>
To get the flag I use `try` because the shift causes the output to not always be a valid `hex` string and if the output starts with the CTF prefix `TH{` print the output. <br/>

Using the script we are easily able to obtain the flag `TH{9c2d7d44f89b46bf9ecf7eee65107185}` and finish this challenge. 