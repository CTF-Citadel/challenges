import os
from fastapi import FastAPI, HTTPException, status
from cryptography.fernet import Fernet

app = FastAPI()

# Secret key for encryption
encryption_key = b'trDjYU54SfgXrKJ5v70kIouVi1dnt7vGQIQSo5cVakg='

# Convert the encryption key to a Fernet key
cipher_suite = Fernet(encryption_key)

@app.get('/code', status_code=status.HTTP_200_OK)
async def get_flag():
    # Fetch the FLAG environment variable
    flag = 'TH{' + os.getenv('FLAG') + '}'
    backup_code = '7A8B9C'

    if not flag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Flag not found')

    # Encrypt the flag
    encrypted_flag = cipher_suite.encrypt(flag.encode()).decode()
    encrypted_backup_code = cipher_suite.encrypt(backup_code.encode()).decode()

    return {'code': encrypted_flag, 'backup_code': encrypted_backup_code}

# Download the apk file automatically when the user visits the root path
@app.get('/', status_code=status.HTTP_200_OK)
async def download_apk():
    return {'download': 'http://localhost:8000/static/StormCast-Authenticator.apk'}

@app.get('/health', status_code=status.HTTP_200_OK)
async def health():
    return {'status': 'OK'}


