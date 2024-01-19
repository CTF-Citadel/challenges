import discord, asyncio, os, random
from discord.ext import commands
from model.database import DBSession, engine
from model import models

# Caesar Cipher Function
def caesar_cipher(text, shift):
    shifted_text = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            shifted_char = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            shifted_text += shifted_char
        else:
            shifted_text += char
    return shifted_text

# set intents for discord-bot
intents = discord.Intents.default()
intents.message_content = True

# Adding a prefix so the bot doesn't read every message in chat
bot = commands.Bot(command_prefix="!", intents=intents)

# async function to print smt when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # set discord bot status
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game('Generating Image'))

# async func which gets activated for every direct message
@bot.event
async def on_message(message):
    db = DBSession() # open session with database

    if message.author == bot.user:
        return

    users = db.query(models.User).filter(models.User.name == message.author).all() # check if email already created 

    if users:
        pass
    else:
        new_flag = ''
        for flag in open('flags.txt', 'r'):
            flags = db.query(models.User).filter(models.User.flag == flag.strip()).all() # check if email already created 

            if flags:
                pass
            else:
                new_flag = flag.split()
                break

        new_user = models.User( # create the new user locally
            id=message.author.id, name=message.author.name, flag=new_flag
        )
        db.add(new_user) 
        db.commit()
        db.refresh(new_user)
        db.close()
        print(f"Added new user: {message.author.name}")

        bot.initialized = True
        channel = message.channel

        if isinstance(channel, discord.TextChannel):
            await channel.trigger_typing()  # Show typing indicator

        async with message.channel.typing(): # Easter Egg
            loading_message = await channel.send("```SWNoIGthbm4gbmljaHQgbWVociwgaWNoIHdpbGwgbmljaHQgbWVociwgaWNoIGhhbHRlIGRhcyBhbGxlcyBuaWNodCBtZWhyIGF1cyE=```")
            await asyncio.sleep(1)

        # Activate Trigger Typing
        async with message.channel.typing():
            count = 1
            for _ in range(10):
                # Creating Loading Animation with dots
                for _ in range(2):
                    await asyncio.sleep(0.2)
                    await loading_message.edit(content=f"```Loading {'.' * count}```")
                    if count < 3:
                        count += 1
                    else:
                        count = 1

                await asyncio.sleep(1)

            await asyncio.sleep(0.5)  # Wait for 1 second

        red_message_formatted = f"```diff\n- 3rr0r\n```"
        await loading_message.edit(content=red_message_formatted)

        return

    # Lists of words I want to scan out
    words_to_check = ["flag", "flags"]

    # Checking for all the words in the message
    if any(word in message.content.lower() for word in words_to_check):
        with open("replies", "r") as file:
            lines = file.readlines()
            random_line = random.choice(lines)

        # Send back message with random line from file
        await message.channel.send(random_line.strip())
        return

    words = message.content.lower().split()

    response_sent = False

    # for loop to check if the correct solution has been found
    for word in words:
        if word.lower() == "password" or word.lower() == "passwort":
            encrypted_text = caesar_cipher("I am a vigilant guardian, shielding networks from danger. Intruders test my defenses, but I swiftly sound the alarm. I scrutinize data flow, sieving out the malevolent. With my protective measures, safety is assured. What am I?", 2)
            
            async with message.channel.typing():
                await message.channel.send(f"```{encrypted_text}```")

            response_sent = True
            break

        elif word.lower() == "firewall":
            encrypted_text = caesar_cipher("I lurk in the shadows, unseen and unknown. Exploiting weaknesses, my presence is never shown. I infiltrate networks, spreading like a plague. A malicious force, causing havoc at my stage. What am I?", 1)
            
            async with message.channel.typing():
                await message.channel.send(f"```{encrypted_text}```")

            response_sent = True
            break

        elif word.lower() == "malware":
            async with message.channel.typing():
                await message.channel.send(f"```Congratulations, the flag is:\nTH{{{db.query(models.User.flag).filter(models.User.name == message.author.name).scalar()}}}```")
            
            response_sent = True

    # default starter question
    if not response_sent:
        async with message.channel.typing():
            encrypted_text = caesar_cipher("I am the guardian of secrets, keeping them locked away. People trust me to secure their data night and day. I am strong and complex, yet vulnerable to a flaw. What am I?", 6)
        
        await message.channel.send(f"```{encrypted_text}```")

    # Checking if a red message is needed (for an Error message)
    if isinstance(message.channel, discord.DMChannel) and message.content.lower() == "send red":
        red_message = "This is a red-colored message."
        red_message_formatted = f"```diff\n- {red_message}\n```"
        await message.channel.send(red_message_formatted)

# Setting up red colored message
async def red_message(ctx, *, message):
    embed = discord.Embed(description=message, color=discord.Color.red())
    await ctx.send(embed=embed)

bot.run(os.environ.get("DC_TOKEN"))
