package com.appweather.stormcast

import android.content.IntentFilter
############################################################
############################################################
########################## BROKEN ##########################
############################################################
############################################################
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import com.appweather.stormcast.ui.StormCastTheme
import kotlinx.coroutines.delay

class MainActivity : AppCompatActivity() {

    val stormBroadcastReceiver = StormBroadcastReceiver()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

############################################################
############################################################
########################## BROKEN ##########################
############################################################
############################################################
      
    val scope = rememberCoroutineScope()
    val context = LocalContext.current

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.Top,
        horizontalAlignment = Alignment.CenterHorizontally,

############################################################
############################################################
########################## BROKEN ##########################
############################################################
############################################################
      
        OutlinedTextField(
            value = apiUrl,
            onValueChange = { apiUrl = it },
            label = { Text(
                text = "API URL",
                color = if (isSystemInDarkTheme()) MaterialTheme.colors.onSurface else MaterialTheme.colors.onBackground
            ) },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            colors = TextFieldDefaults.outlinedTextFieldColors(
                focusedBorderColor = if (isSystemInDarkTheme()) MaterialTheme.colors.onSurface else MaterialTheme.colors.onBackground,
                unfocusedBorderColor = if (isSystemInDarkTheme()) MaterialTheme.colors.onSurface else MaterialTheme.colors.onBackground,
                textColor = if (isSystemInDarkTheme()) MaterialTheme.colors.onSurface else MaterialTheme.colors.onBackground
            )
        )

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
                            
############################################################
############################################################
########################## BROKEN ##########################
############################################################
############################################################
                          
}
