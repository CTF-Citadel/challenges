import base64
from itertools import product

encrypted_flag = b'NjEzODMxNjEzOTY0MzczMzMyMzQzNjM3MzQzODYzMzczMzMxNjI2NjMwNjY2MjYyNjY2MjM1Mzg2MTdkNTQ0ODdiNjYzMjM3'

encrypted_flag = base64.b64decode(encrypted_flag)

pairs = [encrypted_flag[i:i+2] for i in range(0, len(encrypted_flag), 2)]

shift_ranges = [range(1, 25) for _ in range(999999)]

for shift_values in product(*shift_ranges):
    shifted_pairs = pairs
    for shift_value in shift_values:
        shifted_pairs = shifted_pairs[-shift_value:] + shifted_pairs[:-shift_value]

    decrypted_flag = bytes.fromhex(''.join([pair.decode('utf-8') for pair in shifted_pairs]))

    if decrypted_flag.startswith(b"TH{"):
        print(decrypted_flag.decode('utf-8'))

print(pairs)