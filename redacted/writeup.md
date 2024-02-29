## Redacted

## Description
```
Apparently some chat messages between 2 of our employees have been leaked.

Fortunately the sensitive information has been redacted, or has it?
```

## Writeup

Starting off we should take a look at the `.pdf` file. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/ef6c06eb-5c64-4282-9d9a-5d2eb9917fab)

In the `.pdf` file we can see that the flag is blacked out. <br/>
Knowing this we can try to extract different things from the file. <br/>
We may try to extract different ressource types like images or strings. <br/>
Starting off we can try a `strings` command. <br/>
```
BT 1 0 0 1 50 800 Tm (Agent_Bob:   It has come to my attention that we may have a mole in our company.) Tj T* ET
BT 1 0 0 1 50 760 Tm (Agent_Alice: Is there any evidence for your superstition?) Tj T* ET
BT 1 0 0 1 50 720 Tm (Agent_Bob:   Apparently somebody leaked the flag: ) Tj T* ET
BT 1 0 0 1 50 680 Tm (Agent_Alice: It would be pretty serious if someone leaked confidential documents.) Tj T* ET
BT 1 0 0 1 50 640 Tm (Agent_Bob:   No shit!) Tj T* ET
BT 1 0 0 1 50 600 Tm (Agent_Alice: Do you have any suspects in mind?) Tj T* ET
BT 1 0 0 1 50 560 Tm (Agent_Bob:   I did think that 2 employees were acting really suspicious today.) Tj T* ET
BT 1 0 0 1 50 520 Tm (Agent_Alice: I think you should report it to the higher-ups.) Tj T* ET
BT 1 0 0 1 50 480 Tm (Agent_Bob:   I'm afraid I will be framed as a scapegoat.) Tj T* ET
BT 1 0 0 1 50 440 Tm (Agent_Alice: That's a risk you have to take. If you delay it further the punishment will be worse.) Tj T* ET
BT 1 0 0 1 50 400 Tm (Agent_Bob:   I guess you're right, I will commence an emergency meeting now.) Tj T* ET
```

The text inside the `.pdf` file didn't reveal anything interesting. <br/>
Next we can use an online tool like https://pdfcandy.com/extract-images.html to extract the images from a `.pdf` file. <br/>
The online tool returns an image which contains the flag. This concludes the writeup. <br/>
![hidden_text](https://github.com/CTF-Citadel/challenges/assets/110562298/48dc2169-a3bd-4c5c-9e3e-0af93e394d66)



