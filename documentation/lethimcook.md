# lethimcook

## Idea
>[!NOTE]
> The challenge is intended to serve as an easy junior-level exercise, providing a basic introduction to CyberChef and simple encoding languages such as base64 and HEX.


## Challenge Components

The challenge consists of the same components as the previous challenge, including a Dockerfile and a docker-compose.yml to dynamically deploy the challenge flags.


The main component of the challenge is the Python file

```py
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
```

- This function takes a flag as input and encodes it using the following steps:
- Formats the flag as "TH{flag}".
- Encodes the flag with HEX.
- Encodes the HEX string with Base85.
- Encodes the Base85 string with Base64.

```py
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
```


- This route is the root endpoint of the Flask application.
- When accessed, it checks if the environment variable flag is set.
- If the flag is provided, it calls the encode_hex_base85_base64 function to encode the flag and returns the encoded string.
- If no flag is provided, it returns a message indicating that no flag was provided.