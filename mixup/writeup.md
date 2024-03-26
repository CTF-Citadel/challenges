## Mixup

## Description
```
One of our people caught some kind of encrypted message about an `emergency situation`.

Can you decrypt it?
```

## Provided Files
```
- output
```

## Writeup

Starting off we should take a look at the provided file. <br/>
```py
zyzwizvng trlsplrhv!
pxxpwzvlqg pv pizvl hj hswt fpt cpnezo, cz lztlrjrzo lcpl cz fpt rv lcz xwhnztt hj lwpvtyrllrvi pv ryxhwlpvl xrznz hj zmrozvnz.
pnnhworvi lh pvhlczw frlvztt lcz jqpi lcTIzFADJCnQzkEFQBBzzQkDEkQJJJnHAGGAGDjX fpt qzpezo.

lcz vsykzwt xwztzvl rv lcz jqpi jhqqhf lcrt ypxxrvi:
dzwh nhwwztxhvot lh J, hvz rt ypxxzo lh B pvo lfh ypg kz nhwwzqplzo frlc H
lcwzz rt D, jhsw rt croozv pt G, jrmz rt nhvvznlzo lh E
tru qhhet qrez I, tzmzv ypg kz F, zricl tchsqo kz C pvo vrvz rt ptthnrplzo frlc A
lcz qzjl nswmzo nswqg kwpnz rt T, lcz wricl nswmzo nswqg kwpnz rt X pvo lcz cgxczv rt nhvvznlzo lh Q
```

The content of the file we got looks like some scrambled up letters, this may indicate that it is a substitution-cipher. <br/>

> [!NOTE] 
> A subsitution-cipher basically replaces the letters of the original word with other letters. <br/>
> This essentially means that the alphabet gets mapped differently. (Bsp.: testing -> ogronyk) <br/>

Now the only clue we got from the description was the highlighted `emergency situation`. <br/>
This might indicate that it can be mapped to the provided output piece. <br/>
To check this we can use a small python script. <br/>
```py
# vqvykvglr bzfwsfzmg!
# emergency situation!

known_chars = {
    'z': 'e',
    'y': 'm',
    'w': 'r',
    'i': 'g',
    'v': 'n',
    'n': 'c',
    'g': 'y',
    't': 's',
    'r': 'i',
    'l': 't',
    's': 'u',
    'p': 'a',
    'h': 'o'
}

with open('out.txt', 'r') as file:
    out = ''
    for line in file:
        for char in line:
            if char in known_chars.keys():
                out += known_chars[char]
            elif char == ' ':
                out += ' '
            elif char in ['!', ',', ':', '.']:
                out += char
            elif char == '\n':
                out += '\n'
            else:
                out += 'X'

print(out)
```

Script output: <br/>
```sh
$ python3 ./solve.py

emergency situation!
aXXarentXy an agent oX ours Xas XacXeX, Xe testiXieX tXat Xe Xas in tXe Xrocess oX transmitting an imXortant Xiece oX eXiXence.
accorXing to anotXer Xitness tXe XXag tXXXeXXXXXcXeXXXXXXeeXXXXXXXXXcXXXXXXXXX Xas XeaXeX.

tXe numXers Xresent in tXe XXag XoXXoX tXis maXXing:
Xero corresXonXs to X, one is maXXeX to X anX tXo may Xe correXateX XitX X
tXree is X, Xour is XiXXen as X, XiXe is connecteX to X
siX XooXs XiXe X, seXen may Xe X, eigXt sXouXX Xe X anX nine is associateX XitX X
tXe XeXt curXeX curXy Xrace is t, tXe rigXt curXeX curXy Xrace is X anX tXe XyXXen is connecteX to X
```

The script reveals partially decrypted text which with further mapping reveals the full output. <br/>
```py
# zyzwizvng trlsplrhv!
# emergency situation!

known_chars = {
    # Old found chars
    'z': 'e',
    'y': 'm',
    'w': 'r',
    'i': 'g',
    'v': 'n',
    'n': 'c',
    'g': 'y',
    't': 's',
    'r': 'i',
    'l': 't',
    's': 'u',
    'p': 'a',
    'h': 'o',

    # New found chars
    'x': 'p',
    'j': 'f',
    'q': 'l',
    'c': 'h',
    'o': 'd',
    'f': 'w',
    'e': 'k',
    'm': 'v',
    'k': 'b',
    'd': 'z',
    'u': 'x'
}

with open('out.txt', 'r') as file:
    out = ''
    for line in file:
        for char in line:
            if char in known_chars.keys():
                out += known_chars[char]
            elif char == ' ':
                out += ' '
            elif char in ['!', ',', ':', '.', '{', '}', '-', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'Q', 'T', 'X']:
                out += char
            elif char == '\n':
                out += '\n'
            else:
                out += '$'

print(out)
```

Running the script again we gain fully readable sentences. <br/>
```sh
$ python3 ./solve_v2.py
emergency situation!
apparently an agent of ours was hacked, he testified that he was in the process of transmitting an important piece of evidence.
according to another witness the flag thTIeFADJCcQebEFQBBeeQbDEbQJJJcHAGGAGDfX was leaked.

the numbers present in the flag follow this mapping:
zero corresponds to J, one is mapped to B and two may be correlated with H
three is D, four is hidden as G, five is connected to E
six looks like I, seven may be F, eight should be C and nine is associated with A
the left curved curly brace is T, the right curved curly brace is X and the hyphen is connected to Q
```

Being able to read the text we can fully decrypt the flag with the given information. <br/>
```py
known_chars = {
    # Old found chars
    'z': 'e',
    'y': 'm',
    'w': 'r',
    'i': 'g',
    'v': 'n',
    'n': 'c',
    'g': 'y',
    't': 's',
    'r': 'i',
    'l': 't',
    's': 'u',
    'p': 'a',
    'h': 'o',

    # New found chars
    'x': 'p',
    'j': 'f',
    'q': 'l',
    'c': 'h',
    'o': 'd',
    'f': 'w',
    'e': 'k',
    'm': 'v',
    'k': 'b',
    'd': 'z',
    'u': 'x',

    # Numbers and Special chars
    'J': '0',
    'B': '1',
    'H': '2',
    'D': '3',
    'G': '4',
    'E': '5',
    'I': '6',
    'F': '7',
    'C': '8',
    'A': '9',
    'T': '{',
    'X': '}',
    'Q': '-'
}
```

Running the script reveals the flag which concludes this writeup. <br/>
```sh
$ python3 ./solve_v3.py
emergency situation!
apparently an agent of ours was hacked, he testified that he was in the process of transmitting an important piece of evidence.
according to another witness the flag th{6e79308c-eb57-11ee-b35b-000c2944943f} was leaked.

the numbers present in the flag follow this mapping:
zero corresponds to 0, one is mapped to 1 and two may be correlated with 2
three is 3, four is hidden as 4, five is connected to 5
six looks like 6, seven may be 7, eight should be 8 and nine is associated with 9
the left curved curly brace is {, the right curved curly brace is } and the hyphen is connected to -
```