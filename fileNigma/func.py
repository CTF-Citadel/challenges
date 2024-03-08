import os
import random
import string

flag = os.environ.get('FLAG', 'default_value')

# Function to generate10,000 different letters
def generate_large_random_string():
    content = ''

    while len(content) < 10000:
        num_chars_in_paragraph = random.randint(100, 500)  # Adjust the range as needed
        content += ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(num_chars_in_paragraph))
        
       
        if len(content) < 10000 and random.choice([True, False]):
            content += '\n\n'
    
    return content

directory = '/usr/local/apache2/htdocs'

# File creation
for i in range(1, 101):
    filename = os.path.join(directory, f'file_{i}.txt')

    if i == 1:
        content = generate_large_random_string()
    else:
        content = generate_large_random_string()

    with open(filename, 'w') as file:
        file.write(content)

chosen_file = os.path.join(directory, random.choice([f for f in os.listdir(directory) if f.endswith('.txt')]))

content = 'TH{' + flag + '}' + generate_large_random_string()

# Write the content to a random location in the file
with open(chosen_file, 'r') as file:
    file_content = file.read()

    # Choose a random position to insert the content
    insert_position = random.randint(0, len(file_content))

    updated_content = file_content[:insert_position] + content + file_content[insert_position:]

# Write the updated content back to the file
with open(chosen_file, 'w') as file:
    file.write(updated_content)

