# StormCast 1

## Overview
```

I have obtained a prototype of the new authentication app for the StormCast Messenger. 
My contact on the inside told me that they are using an advanced security code system called SEC_CODE. 
If we want to get the backup code, we need to find a way to tamper with the SEC_CODE system to get the backup codes.
```

StromCast is a mobile analysis and exploitation challenge. It is designed to be solvable without the need of live patching or having a rooted phone. To solve it, ADB is needed.

## Creation
Because it is a mobile android challenge we need an APK. To make this challenge also dynamic, an API service is needed to send the flag to the app.

### Creating an exploitable APK
The app is very simple. It consist out of a input filed for the API URL and a button that fetches the "SEC_CODE" aka the flag:

```Kotlin
Button(  
    onClick = {  
        if (apiUrl.isNotEmpty()) {  
  
            scope.run {  
                launch {  
                    context.registerReceiver(stormBroadcastReceiver, IntentFilter("com.appweather.stormcast.SEC_CODE_READY"))  
                    delay(2000) // Delay to allow time for the broadcast to be received  
  
                    if (stormBroadcastReceiver.secCodeReady) {  
                        val encryptedCode = fetchEncryptedSecCode(apiUrl)  
                        decryptedCode = decryptCode(encryptedCode)  
                    } else {  
                        Toast.makeText(context, "Please wait for the security code to be ready", Toast.LENGTH_SHORT).show()  
                    }  
                }  
            }  
        } else {  
            // Handle case where URL is empty  
            Toast.makeText(context, "Please enter a valid URL", Toast.LENGTH_SHORT).show()  
        }  
    },  
    modifier = Modifier  
        .fillMaxWidth()  
        .padding(bottom = 16.dp),  
) {  
    Text(  
        text = "Get Security Code",  
        color = if (isSystemInDarkTheme()) MaterialTheme.colors.onSurface else MaterialTheme.colors.onBackground  
    )  
}
```

To make things a little bit more challenging, the app also needs a variable called `secCodeReady` to be `true`. This is a broadcast intent. This means that it can be send also by a connected device with ADB.

When the broadcast is received, `secCodeReady` is set to `true`:
```Kotlin
class StormBroadcastReceiver : BroadcastReceiver() {  
  
    var secCodeReady = false // Variable to indicate if flag fetching is allowed  
  
    override fun onReceive(context: Context?, intent: Intent?) {  
        if (intent?.action == "com.appweather.stormcast.SEC_CODE_READY") {  
            // Custom broadcast action received, set the flagReady variable to true  
            secCodeReady = true  
        }  
    }  
}
```

After the check is passed, the app fetches the flag from the API endpoint: 
```Kotlin
if (stormBroadcastReceiver.secCodeReady) {  
    val encryptedCode = fetchEncryptedSecCode(apiUrl)  
    decryptedCode = decryptCode(encryptedCode)  
} else {  
    Toast.makeText(context, "Please wait for the security code to be ready", Toast.LENGTH_SHORT).show()  
}
```

To make sure that the flag is not intercepted when it is send over http, I opted for an additional encryption by using fernet. The flag is being decrypted by using the `decryptCode()` function:
```Kotlin
fun decryptCode(encryptedMessage: String): String {  
    val encryptionKey = "trDjYU54SfgXrKJ5v70kIouVi1dnt7vGQIQSo5cVakg="  
  
    //extract the encrypted message from the JSON response  
    val jsonResponse = JSONObject(encryptedMessage)  
    val encryptedMessage = jsonResponse.getString("code")  
  
    // Create a Key object using your Fernet key  
    val key = Key(encryptionKey)  
  
    // Create a Token object from the encrypted message  
    val token = Token.fromString(encryptedMessage)  
  
    // Define a Validator object. This object is used to set the time-to-live (TTL) for the token.  
    val validator: Validator<String> = object : StringValidator {  
        override fun getTimeToLive(): TemporalAmount {  
            return Duration.ofHours(24)  
        }  
    }  
  
    // Return the decrypted message  
    return token.validateAndDecrypt(key, validator)  
}
```

In theory this would also open up the opportunity to read out all strings of the APK, intercept the response and then decrypt it with the `encryptionKey`.

After decrypting, the flag is printed out on the screen.

### Creating the API service
For the API service I used a simple fastAPI application. The API provides the APK file, some source code and the endpoint for sending the flag to the android app.

The `/` endpoint is some sort of a welcome screen that gives the user the instructions to go to a specific endpoint:
```Python
@app.get('/', status_code=status.HTTP_200_OK)
async def download_response():
    return {'message': 'Download the apk file at /confidential.zip'}
```

When going to `/confidential.zip` the user gets the APK and redacted source code:
```Python
@app.get('/confidential.zip', status_code=status.HTTP_200_OK)
async def zip_file():
    # download the zip file with the kotlin source code and the apk file
    return FileResponse('confidential.zip')
```

The `/code` endpoint is crucial for the app. It encrypts the flag using fernet.
```Python
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
```
At first, the flag gets read from the environment and then encrypted alongside with a static variable called `backup_code`. 
The encryption key is a pre-shared secret that is also baked into the APK. 

### Creating Dockerfile and docker-compose.yml
The Dockerfile is a very simple python 3.8-slim-buster image that installs the necessary requirements and starts the app.
```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the confidential.zip file into the container
COPY confidential.zip /app/confidential.zip

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ARG FLAG
ENV FLAG=${FLAG}

# Run main.py when the container launches
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

The docker-file is also very simple:
```yml
version: '3.9'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - FLAG=$FLAG
```
