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
