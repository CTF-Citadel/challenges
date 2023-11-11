#!/bin/bash

# Input file
input_file="./input.pcapng"

# Output file
output_file="./capture.pcapng"

# Generate a UUID with the format "TH{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}"
new_password="TH{$(python3 -c 'import uuid; print(str(uuid.uuid4()))' | tr -d '-' | tr '[:upper:]' '[:lower:]')}"

# Convert the pcapng file to a hex dump
xxd -p $input_file > temp_hex_dump.txt

# Find the position of the password in the hex dump
position=$(grep -ob 'uname=test&pass=' temp_hex_dump.txt | cut -d ":" -f 1)

# Calculate the length of the password (in hex)
password_length=$(echo -n "test" | xxd -p | tr -d '\n')

# Replace the password in the hex dump
sed -i "${position}s/${password_length}/$(echo -n "$new_password" | xxd -p | tr -d '\n')/g" temp_hex_dump.txt

# Convert the hex dump back to binary
xxd -r -p temp_hex_dump.txt > $output_file

# Clean up temporary files
rm temp_hex_dump.txt

echo "Password changed successfully. Modified file: $output_file"
