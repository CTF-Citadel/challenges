import os, zipfile

env_variable = os.getenv("FLAG")  # Updated to use "flag" as the environment variable

# Set the flag for the file content 
flag = f"TH{{{env_variable}}}"



# Fix this
while True:
    # Create the goldnugget.txt file
    file_content = flag.encode("utf-8")
    with open("goldnugget.txt", "wb") as file:
        file.write(file_content)

    # Zip the file 100 times
    for _ in range(100):
        with zipfile.ZipFile("goldnugget.zip", "w") as zip_file:
            zip_file.write("goldnugget.txt")

        # Update the content to be the zipped file
        with open("goldnugget.txt", "rb") as file:
            file_content = file.read()

        # Write the zipped content back to the file
        with open("goldnugget.txt", "wb") as file:
            file.write(file_content)