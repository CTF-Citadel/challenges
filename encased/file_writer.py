import os, random, py_compile, string

flag = f'TH{{{os.getenv("FLAG")}}}'

# Created list for flag
listed_flag = list(flag)

rndm_num = random.randint(1, 100000000000)

# shuffle flag
random.seed(rndm_num)
random.shuffle(listed_flag)

# Function to write functions to output file
def write_functions(funcName, seed):
    file.write(f'def {funcName}(shuffled_list):\n\n')
    file.write(f'    random.seed({seed})\n\n')
    file.write(f'    indices = list(range(len(shuffled_list)))\n')
    file.write(f'    random.shuffle(indices)\n\n')
    file.write(f'    reversed_list = [None] * len(shuffled_list)\n')
    file.write(f'    for i, j in zip(indices, range(len(shuffled_list))):\n')
    file.write(f'        reversed_list[i] = shuffled_list[j]\n\n')
    file.write(f'    reversed_string = "".join(reversed_list)\n\n')
    file.write(f'    return reversed_string\n\n')

# Open output file to add content
with open('yeet.py', 'w') as file:
    file.write('import random\n\n')
    file.write(f'shuffled_input = {listed_flag}\n\n')

    # Generate fake functions
    for _ in range(1, 30):
        write_functions("".join(random.choice((str.upper, str.lower))(char) for char in "iknowsomeonewhodoesnotshower"), random.randint(1, 100000000000))

    # Actual function to solve challenge
    trueFuncName = "".join(random.choice((str.upper, str.lower))(char) for char in "iknowsomeonewh0doesnotshower")

    write_functions(trueFuncName, rndm_num)

    # Generate fake functions
    for _ in range(1, 30):
        write_functions("".join(random.choice((str.upper, str.lower))(char) for char in "iknowsomeonewhodoesnotshower"), random.randint(1, 100000000000))

    # hardcode password as main challenge
    file.write('password = input("Enter password: ")\n')
    file.write(f'if password == "{"".join(random.choice(string.ascii_letters + string.digits) for _ in range(20))}":\n')
    file.write(f'    print({trueFuncName}(shuffled_input))\n')
    file.write('else:\n')
    file.write('    print("Wrong Password!")\n\n')

    # Generate fake functions
    for _ in range(1, 30):
        write_functions("".join(random.choice((str.upper, str.lower))(char) for char in "iknowsomeonewhodoesnotshower"), random.randint(1, 100))

# Compile .py file to .pyc file
py_compile.compile("yeet.py")