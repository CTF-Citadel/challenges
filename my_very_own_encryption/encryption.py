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
