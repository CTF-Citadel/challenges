from Crypto.Util.number import getPrime, isPrime, bytes_to_long
import os

flag = f'TH{{{os.getenv("FLAG")}}}'
FLAG = bytes_to_long(flag.encode())

p = getPrime(300)

while (not isPrime(p + 50)):
    p = getPrime(300)

q = p + 50

n = p * q
e = 65537
ct = pow(FLAG, e, n)

with open('output', 'w') as file: 
    file.write(f'n: {n}\n')
    file.write(f'e: {e}\n')
    file.write(f'ct: {ct}')