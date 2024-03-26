import random, os

def switch_characters(input_str):
    # dictionary to store letter mapping
    char_map = {}

    # generate random order for letters A-J
    letters = [chr(i) for i in range(65, 75)]
    random.shuffle(letters)

    # map numbers 0-9 to letters A-J (for UUID)
    for i in range(10):
        char_map[str(i)] = letters[i]

    output_str = ''
    for char in input_str:
        if char.isalpha() or char.isdigit():
            if char.isdigit():
                output_str += char_map[char]
            elif char.isalpha() and char.lower() not in char_map:
                new_char = char
                while new_char == char or new_char.lower() in char_map.values():
                    new_char = chr(random.randint(65, 90)) if char.isupper() else chr(random.randint(97, 122))
                char_map[char.lower()] = new_char.lower() if char.islower() else new_char.upper()
                output_str += char_map[char.lower()] if char.islower() else char_map[char.lower()].upper()
            else:
                output_str += char_map.get(char.lower(), char) if char.isalpha() else char
        elif char == '{':
            output_str += 'T'
        elif char == '}':
            output_str += 'X'
        elif char == '-':
            output_str += 'Q'
        else:
            output_str += char

    return output_str

input = f"""emergency situation!
apparently an agent of ours was hacked, he testified that he was in the process of transmitting an important piece of evidence.
according to another witness the flag th{{{os.environ['FLAG']}}} was leaked.

the numbers present in the flag follow this mapping:
zero corresponds to 0, one is mapped to 1 and two may be correlated with 2
three is 3, four is hidden as 4, five is connected to 5
six looks like 6, seven may be 7, eight should be 8 and nine is associated with 9
the left curved curly brace is {{, the right curved curly brace is }} and the hyphen is connected to -"""

with open('output', 'w') as file: 
    file.write(switch_characters(input))