import os

flag = f'TH{{{os.getenv("FLAG")}}}'

for char in flag:
    # convertion to ascii and aftrwards to binary
    binary_repr = bin(ord(char))[2:] 

    # Pad the binary representation with leading zeros to ensure each chunk is 8 bits long
    binary_repr_padded = binary_repr.zfill(8)

    # Split the binary representation into chunks of 8 bits
    inverted_binary_repr = binary_repr_padded.translate(str.maketrans('01', '10'))

    # Split single string into multiple
    binary_chunks = [inverted_binary_repr[i:i+8] for i in range(0, len(inverted_binary_repr), 8)]

    # Write binary to file
    with open('output', 'a') as file:
        for char in binary_chunks:
            file.write(f'{char}\n')
