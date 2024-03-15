# Cheap RSA

## Description
```
Generating secure RSA prime numbers can be computationally intensive.

To conserve resources I only calculated 1 prime number, this won't cause any security issues will it?
```

## Writeup

Starting off we should take a look at the provided files. <br/>
```py
from Crypto.Util.number import getPrime,  isPrime,bytes_to_long
import os

flag = f'TH{{{os.getenv("FLAG")}}}'
FLAG = bytes_to_long(flag.encode())

p = getPrime(300)

while (not isPrime(p + 50)):
    p = getPrime(300)

q = p + 50

n = p * q
e = 2**16 + 1
ct = pow(FLAG, e, n)

with open('output', 'w') as file: 
    file.write(f'n: {n}\n')
    file.write(f'e: {e}\n')
    file.write(f'ct: {ct}')
```

Output file:
```
n:2078832324228731447790279678521264622937524358213870232038624969453711831047420927353929881190933694234367577893391554039073337891263645200449769076050843775639572116959977816218771
e:65537
ct:1048843354298783836933905023359185221673454065719524304829818787493786473233269969532172689974228809662310406519830770820224280376080800298026961099807957814754745871433620359679070
```

Now the important thing to notice above is that we are able to calculate `p` and `q` from `n`. <br/>
To do that we can use the equation below. <br/>
```
p * (p + 50) = 2078832324228731447790279678521264622937524358213870232038624969453711831047420927353929881190933694234367577893391554039073337891263645200449769076050843775639572116959977816218771
```

Using this equation with simple `RSA` functions from the `pycrypto` library we can make a script to decrypt the flag. <br/>
```py
import sympy as sp
from Crypto.Util.number import long_to_bytes, inverse

n,e,ct = 0,0,0

for line in open('output', 'r'):
    if line.split()[0][0] == 'n':
        n = int(line.split()[1])
    elif line.split()[0][0] == 'e':
        e = int(line.split()[1])
    elif line.split()[0].split(':')[0] == 'ct':
        ct = int(line.split()[1])


p0 = sp.Symbol('p0')

equation = p0 * (p0 + 50) - n

p_sol = sp.solve(equation, p0)


valid_solutions = [sol for sol in p_sol if sol.is_integer and sol > 0]

if valid_solutions:

    p = valid_solutions[0]
    q = p + 50

    n = p * q

    phi = (p - 1) * (q - 1)
    d = inverse(int(e), int(phi))
    pt = pow(int(ct), int(d), int(n))
    flag = long_to_bytes(pt)

    print(flag.decode())
```

Executing this script reveals the flag which concludes this writeup. <br/>
```sh
$ python3 solve.py 
TH{4bc2b7a9-fb20-4cd3-956a-63e607f5fb5c}
```
