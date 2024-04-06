## Elysium Realms

## Description
```
The alpha version of our MMO-RPG has been released.
Somebody reported a bug in one of our game features but didn't specifiy the exact issue.

Can you help us figure out what's wrong?
```

## Writeup

Starting off, we should take a look at the website. <br/>
The first thing we find is a signup/login, after creating an account we can access the actual web-application. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/805f52aa-de9f-4be0-974e-323f832b076d)

The game functions seem to work fine and we are able to get different things. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/7ab2b269-25c0-4f3b-b085-9f702b327798)

Testing the game functions some more doesn't reveal anything interesting. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/3dc0ada1-e8d8-417a-9059-a3a699c0ff21)

Taking a look at the menu we can find the items we just aquired in the inventory tab. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/3b58ac6c-b9b9-4963-b7ef-029db2190fc3)

Looking around some more in the menu we can find something interesting in the marketplace section. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/f0406c8a-7dea-4d21-accb-8d78def0ab8b)

Trying to buy the flag doesn't seem to work as we don't have any credits. <br/>
The buy function doesn't seem to contain any errors itself. <br/>
Knowing that we need enough credits to buy the flag we can look around for any way to somehow get credits. <br/>
The only other option we can find which could get us credits is the transfer function. <br/>
Testing if we can transfer money to ourselves returns an error. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/0149f43e-6f24-411a-a44d-9e39e3833981)

Creating a second account and testing if we can send an amount we don't have also doesn't return a positive result. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/a635461f-7a44-458c-9855-d2e197d08e79)

Testing some more we can find that we are able to transfer negative amounts of credits. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/63aff273-060a-4ad8-b6a2-768f1f94c60c)

Having sufficient credits to buy the flag we can navigate to the marketpalce again. <br/>
Seems like we successfully bought the flag. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/83148b6f-1722-40fb-8ffb-8b2caaaa21c4)

Looking into our inventory now reveals the actual flag in the item description which concludes this writeup. <br/>
![image](https://github.com/CTF-Citadel/challenges/assets/110562298/24f68d35-f588-44dc-b08e-fa51cc2dd3e1)

