from model import models
from model.database import DBSession
import hashlib, random, secrets, string, os

# List of fantasy places for the text rpg 
locations = {
    'Mountain': ['Dragonspire Peaks', 'Mystic Summit', 'Thunderpeak Range', "Eagle's Eyrie", 'Celestial Crest'],
    'Forest': ['Enchanted Arbor', 'Moonshade Grove', 'Elderwood Realm', 'Feywild Thicket', 'Sylvan Whisperwoods'],
    'Swamp': ['Shadowfen Marsh', 'Mistwood Bog', "Serpent's Lair", 'Foghaven Wetlands', 'Fiery Swamp'],
    'Plains': ['Gilded Grasslands', 'Azure Savannah', 'Golden Horizon Fields', 'Elysian Meadowlands', 'Windswept Plains'],
    'Desert': ['Dunes of Mirage', 'Sands of Serenity', 'Eternal Sun Wastes', 'Oasis of Dreams', 'Quicksand Mirage']
}

base_img_URL = 'https://winklersblog.net/imgs/elysium_realms/'
error_msg = ['No place to travel to in this direction!', 'Invalid direction!']

materials = [
    "Wood", "Stone", "Iron Ore", "Gold Ore", "Copper Ore",
    "Silver Ore", "Diamond", "Coal", "Clay", "Flint", "Obsidian",
    "Sulfur", "Quartz", "Leather", "Wool", "Feathers", "Bone",
    "Hide", "Fur", "Shell", "Wolf-Fangs"
]

hunting_materials = [
    "Leather", "Wool", "Feathers", "Bone",
    "Hide", "Fur", "Shell", "Wolf-Fangs", 
]

collecting_materials = [
    "Wood", "Stone", "Iron Ore", "Gold Ore", "Copper Ore",
    "Silver Ore", "Diamond", "Coal", "Clay", "Flint", "Obsidian",
    "Sulfur", "Quartz"
]

def rndm_tool():
    choices = ['shovel', 'chisel', 'pickaxe']
    tool = random.choice(choices)

    ranks = ['common', 'rare', 'epic', 'legendary', 'mythic']
    rank = random.choice(ranks)

    properties = ['Sharp','Durable','Lightweight (baby!)','Efficient','Versatile','Sturdy','Wide-blade','Heavy-duty','Precision','Multi-functional']
    my_property = random.choice(properties)

    return {
        'toolname': f'{my_property} {tool}',
        'durability':random.uniform(1, 99),
        'efficiency': random.randrange(1, 10),
        'rank': rank,
        'type': f'tool_0{random.randrange(0, 5)}'
    }

def rndm_weapon():
    ranks = ['common', 'rare', 'epic', 'legendary', 'mythic']
    rank = random.choice(ranks)

    properties = ['Sharp','Durable','Lightweight (baby!)','Deahtly','Versatile','Sturdy','Wide','Heavy-duty','Precision','Multi-functional']
    my_property = random.choice(properties)

    return {
        'weaponname': f'{my_property} blade',
        'damage': random.randrange(1, 1000),
        'attack_speed': random.uniform(1, 1000),
        'durability': random.uniform(1, 99),
        'rank': rank,
        'type': f'blade_0{random.randrange(0, 6)}'
    }

# hash function for passwords
def sha256_hash(text):
    sha256 = hashlib.sha256()
    sha256.update(text.encode('utf-8'))
    return sha256.hexdigest()

# Function to inject fake data for
def inject_data():
    db = DBSession()

    # insert guilds
    for guild in open('data/guilds.txt', 'r'):
        check = db.query(models.Guild).filter(models.Guild.title == guild.split('\n')[0]).all()

        if check:
            continue

        if guild.strip() != 'Ainz Ooal Gown': # check for custom details
            new_guild = models.Guild(
                title=guild.strip(), level=random.randint(1, 6)
            )
        else:
            new_guild = models.Guild(
                title=guild.strip(), level=10
            )
        
        db.add(new_guild) # commit new entry to db
        db.commit()
        db.refresh(new_guild)

    # insert users
    for user in open('data/users.txt', 'r'):
        check = db.query(models.User).filter(models.User.username == user.strip()).all()

        if check:
            continue

        if user.strip() != 'Aryt3': # check for custom details
            new_user = models.User(
                username=user.strip(), password_hash=sha256_hash(''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))), level=random.randint(1, 99), affiliation=random.choice(open('data/guilds.txt').readlines()[1:]).rstrip('\n') if open('data/guilds.txt').readlines()[1:] else None
            )
        else:
            new_user = models.User(
                username=user.strip(), password_hash=sha256_hash(''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))), level=100, affiliation='Ainz Ooal Gown'
            )
        
        db.add(new_user) # commit new entry to db
        db.commit()
        db.refresh(new_user)

    # insert random items
    for _ in range(0, 50):
        new_item = models.Item(
            itemname=random.choice(materials), description='An item which is very dear to me.', quantity=random.randrange(1, 100), type='materials', price=random.randint(1000, 100000), affiliation='Aryt3'
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    
    for _ in range(0, 50):
        tool = rndm_tool()
        
        new_tool = models.Tool(
            toolname=tool['toolname'], description='A tool which is very dear to me.', durability=tool['durability'], efficiency=tool['efficiency'], rank=tool['rank'], type=tool['type'], price=random.randint(1000, 100000), affiliation='Aryt3'
        )
        db.add(new_tool)
        db.commit()
        db.refresh(new_tool)

    for _ in range(0, 50):
        weapon = rndm_weapon()

        new_weapon = models.Weapon(
            weaponname=weapon['weaponname'], description='A weapon which is very dear to me.', damage=weapon['damage'], attack_speed=weapon['attack_speed'], durability=weapon['durability'], rank=weapon['rank'], type=weapon['type'], price=random.randint(1000, 100000), affiliation='Aryt3'
        )
        db.add(new_weapon)
        db.commit()
        db.refresh(new_weapon)

    flag = models.Item(
        itemname='super secret flag', description=f'TH{{{os.environ.get("FLAG")}}}', quantity=1, type='flag', price=1234567890, affiliation='Aryt3'
    )
    db.add(flag)
    db.commit()
    db.refresh(flag)

    db.close()

# Function to determine next place to travel to
def travel(dir, cur_location):
    check_before, check_after = False, False

    # Loop to determine next place to travel to
    for index, biome in enumerate(locations):
        if check_after == True and index < 5: # Check if new location was found and set biome after
            biome_after = biome
            check_after = False
        if cur_location in locations[biome]: # Check if new location was found
            check_before = True
            check_after = True
            current_biome = biome
            current_index = index
        if check_before == False: # Check if new location was found and set biome before
            biome_before = biome

    # Get new place for direction
    match dir:
        case 'N': # Direction North
            if current_index > 0:
                new_location_index = locations[current_biome].index(cur_location)
                new_location = locations[biome_before][new_location_index]
            else:
                return error_msg[0]
            
        case 'NW': # Direction North-West
            if current_index > 0 and locations[current_biome].index(cur_location) > 0:
                new_location_index = locations[current_biome].index(cur_location) - 1
                new_location = locations[biome_before][new_location_index]
            else:
                return error_msg[0]

        case 'NE': # Direction North-East
            if current_index > 0 and locations[current_biome].index(cur_location) < 4:
                new_location_index = locations[current_biome].index(cur_location) + 1
                new_location = locations[biome_before][new_location_index]
            else:
                return error_msg[0]

        case 'E': # Direction East
            if locations[current_biome].index(cur_location) < 4:
                new_location_index = locations[current_biome].index(cur_location) + 1
                new_location = locations[current_biome][new_location_index]
            else:
                return error_msg[0]

        case 'S': # Direction South
            if current_index < 4:
                new_location_index = locations[current_biome].index(cur_location)
                new_location = locations[biome_after][new_location_index]
            else:
                return error_msg[0]

        case 'SW': # Direction South-West
            if current_index < 4 and locations[current_biome].index(cur_location) > 0:
                new_location_index = locations[current_biome].index(cur_location) - 1
                new_location = locations[biome_after][new_location_index]
            else:
                return error_msg[0]

        case 'SE': # Direction South-East
            if current_index < 4 and locations[current_biome].index(cur_location) < 4:
                new_location_index = locations[current_biome].index(cur_location) + 1
                new_location = locations[biome_after][new_location_index]
            else:
                return error_msg[0]

        case 'W': # Direction West
            if locations[current_biome].index(cur_location) > 0:
                new_location_index = locations[current_biome].index(cur_location) - 1
                new_location = locations[current_biome][new_location_index]
            else:
                return error_msg[0]

        case _: # else
            return error_msg[1]

    return new_location

# Function to generate image URL for current place
def get_img(name):
    for biome, locations_list in locations.items():
        if name in locations_list:
            # Get the index of the location in the list and format the image file name
            return f'{base_img_URL}{biome}_0{locations_list.index(name) + 1}.png'

    return None  # Return None if name is not found in any biome