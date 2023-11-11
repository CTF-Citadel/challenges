#!/bin/bash

# Input file
input_file="./input.pcapng"

# Output file
output_file="./capture.pcapng"

# Generate a UUID with the format "TH{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}"
new_password="TH{$(python3 -c 'import uuid; print(str(uuid.uuid4()))' | tr -d '-' | tr '[:upper:]' '[:lower:]')}"

# Replace the password in the pcapng file and remove the trailing "test"
awk -v new_pass="$new_password" 'BEGIN {FS=OFS="="} $1=="uname" && $2=="test&pass" {print $1, $2, new_pass; next} {print}' $input_file > $output_file

echo "Password changed successfully to $new_password. Modified file: $output_file"
