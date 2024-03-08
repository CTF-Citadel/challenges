import os
import base64
from flask import Flask

app = Flask(__name__)

def encode_hex_base85_base64(flag):
    # Format the flag as TH{UUID}
    formatted_flag = f"TH{{{flag}}}"

    # Encode flag with HEX
    hex_encoded = formatted_flag.encode('utf-8').hex()

    # Encode HEX string with Base85
    base85_encoded = base64.b85encode(hex_encoded.encode('utf-8')).decode('utf-8')

    # Encode Base85 string with Base64
    base64_encoded = base64.b64encode(base85_encoded.encode('utf-8')).decode('utf-8')

    return base64_encoded

@app.route('/')
def encode_flag():
    flag = os.getenv('flag')
    if flag:
        final_base64_encoded = encode_hex_base85_base64(flag)
        return f"String: {final_base64_encoded}"
    else:
        return "No flag provided."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
