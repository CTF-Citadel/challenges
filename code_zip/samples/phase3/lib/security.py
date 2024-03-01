import os

def check_password():
    expected_password = os.getenv("CIRCLE_CALCULATOR_PASSWORD")

    if not expected_password:
        raise ValueError("Password not set. Please set CIRCLE_CALCULATOR_PASSWORD environment variable.")

    password = input("Enter the password: ")
    return password == expected_password
