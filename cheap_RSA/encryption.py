from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_faulty_key_pair():
    key = RSA.generate(2048, e=1)  # Set e to 1
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_flag(flag, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    encrypted_flag = cipher.encrypt(flag.encode())
    return encrypted_flag

if __name__ == "__main__":
    # Generate faulty RSA key pair with e=1
    private_key, public_key = generate_faulty_key_pair()

    # Extract e and N from the public key
    key = RSA.import_key(public_key)
    e = key.e
    N = key.n

    # Your flag to be encrypted
    flag = "CTF{YourFlagHere}"

    # Encrypt the flag using e=1
    encrypted_flag = encrypt_flag(flag, public_key)

    # Display results
    print(f"e = {e}")
    print(f"c = {int.from_bytes(encrypted_flag, 'big')}")
    print(f"n = {N}")
