## Zero to Hero

## Description
```
Some things seem to have been scrambled up.

Can you untagle the output?
```

## Writeup

Starting off we should take a look at the provided `output` file. <br/>
```
10101011
10110111
10000100
10011001
11001111
10011101
11001001
10011011
11001010
11001111
10011110
11010010
11001110
11001100
11001010
11001000
11010010
11001011
11000111
11001010
10011011
11010010
11000110
11001001
10011011
11001010
11010010
11001100
11001110
11001101
10011001
11001000
11000111
11001001
11001111
11001101
10011011
10011100
10011010
10000010
```

Seeing the content of the `output` file anyone should realize that this is binary. <br/>
Trying to directly convert it to binary results in nothing. Knowing this I built a small python script to convert 1s to 0s and 0s to 1s.  <br/>
```py
with open('output', 'r') as file:
    flag = ''.join(chr(int(line.split()[0].translate(str.maketrans('01', '10')), 2)) for line in file)

print(flag)
```

Executing the script results in us getting the flag and concludes this writeup. <br/>
```sh
kali@kali python3 solve.py 

TH{f0b6d50a-1357-485d-96d5-312f78602dce}
```
