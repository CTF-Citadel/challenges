## Shadow Gateway

## Description
```
A first grader is proudly flexing his new encryption algorithm which he made during an ITP project. 

Can you humble the first grader by breaking his encryption?
```

## Writeup

Starting off we should take a look at the provided files. <br/>
```py
import os, base64, random

flag = "TH{" + str(os.environ.get("FLAG")) + "}" 

def encrypt(flag):
    encoded_flag = bytes(flag, 'utf-8').hex()

    shifted_pairs = [encoded_flag[i:i + 2] for i in range(0, len(encoded_flag), 2)]

    for i in range(999999):
        rndm = random.randint(1, 25)
        shifted_pairs = shifted_pairs[-rndm:] + shifted_pairs[:-rndm]

    encrypted_flag = ''.join(shifted_pairs)

    return base64.b64encode(bytes.fromhex(encrypted_flag))

print(encrypt(flag))
```

The important things to see are the different convertions. <br/>
From `string` to `hex`, from `hex` to `string pairs`, from `string pairs` to `random string pairs`, from `random string pairs` to `string` and from `string` to `base64`. <br/>
Knowing these steps anybody should be able to code a small script to decrypt the flag. <br/>
```py
import base64

with open("output", "r") as file:
    encrypted_flag = file.readline().strip()

encrypted_flag = base64.b64decode(encrypted_flag)

hex_pairs = [hex(byte)[2:].zfill(2) for byte in encrypted_flag]

for num in range(len(hex_pairs)):
    shifted_pairs = hex_pairs[-num:] + hex_pairs[:-num]
    decrypted_flag = bytes.fromhex(''.join(shifted_pairs)).decode('utf-8', 'ignore')

    if decrypted_flag.startswith("TH{"):
        print(decrypted_flag)
        break
```

This script first decodes from `base64` than converts the `hex` string to `string pairs`. <br/>
The main problem is amount of loops and random shift. <br/>
The problem with that is that it doesnt really matter how often you shift if the amounts of possible shifts is predictable. <br/>
In our case we can jsut shift through the pairs until we find `TH{` at the beginning. <br/>

Using the script we are easily able to obtain the flag `TH{REDACTED}` and finish this challenge. 