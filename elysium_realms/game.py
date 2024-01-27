
# List of fantasy places for the text rpg 
locations = {
    'Mountain': ['Dragonspire Peaks', 'Mystic Summit', 'Thunderpeak Range', "Eagle's Eyrie", 'Celestial Crest'],
    'Forest': ['Enchanted Arbor', 'Moonshade Grove', 'Elderwood Realm', 'Feywild Thicket', 'Sylvan Whisperwoods'],
    'Swamp': ['Shadowfen Marsh', 'Mistwood Bog', "Serpent's Lair", 'Foghaven Wetlands', 'Fiery Swamp'],
    'Plains': ['Gilded Grasslands', 'Azure Savannah', 'Golden Horizon Fields', 'Elysian Meadowlands', 'Windswept Plains'],
    'Desert': ['Dunes of Mirage', 'Sands of Serenity', 'Eternal Sun Wastes', 'Oasis of Dreams', 'Quicksand Mirage']
}

base_img_URL = 'https://tophack.at/imgs/'

err_map_ending = 'No place to travel to in this direction!'

# Function to determine next place to travel to
def travel(dir, cur_location):
    check_before, check_after, image_path = False, False, ''

    # Get biome of current place
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
                image_path = f'{base_img_URL}{biome_before}_0{new_location_index + 1}.png'
            else:
                return err_map_ending
            
        case 'NW': # Direction North-West
            if current_index > 0 and locations[current_biome].index(cur_location) > 0:
                new_location_index = locations[current_biome].index(cur_location) - 1
                new_location = locations[biome_before][new_location_index]
                image_path = f'{base_img_URL}{biome_before}_0{new_location_index + 1}.png'
            else:
                return err_map_ending

        case 'NE': # Direction North-East
            if current_index > 0 and locations[current_biome].index(cur_location) < 4:
                new_location_index = locations[current_biome].index(cur_location) + 1
                new_location = locations[biome_before][new_location_index]
                image_path = f'{base_img_URL}{biome_before}_0{new_location_index + 1}.png'
            else:
                return err_map_ending

        case 'E': # Direction East
            if locations[current_biome].index(cur_location) < 4:
                new_location_index = locations[current_biome].index(cur_location) + 1
                new_location = locations[current_biome][new_location_index]
                image_path = f'{base_img_URL}{current_biome}_0{new_location_index + 1}.png'
            else:
                return err_map_ending

        case 'S': # Direction South
            if current_index < 4:
                new_location_index = locations[current_biome].index(cur_location)
                new_location = locations[biome_after][new_location_index]
                image_path = f'{base_img_URL}{biome_after}_0{new_location_index + 1}.png'
            else:
                return err_map_ending

        case 'SW': # Direction South-West
            if current_index < 4 and locations[current_biome].index(cur_location) > 0:
                new_location_index = locations[current_biome].index(cur_location) - 1
                new_location = locations[biome_after][new_location_index]
                image_path = f'{base_img_URL}{biome_after}_0{new_location_index + 1}.png'
            else:
                return err_map_ending

        case 'SE': # Direction South-East
            if current_index < 4 and locations[current_biome].index(cur_location) < 4:
                new_location_index = locations[current_biome].index(cur_location) + 1
                new_location = locations[biome_after][new_location_index]
                image_path = f'{base_img_URL}{biome_after}_0{new_location_index + 1}.png'
            else:
                return err_map_ending

        case 'W': # Direction West
            if locations[current_biome].index(cur_location) > 0:
                new_location_index = locations[current_biome].index(cur_location) - 1
                new_location = locations[current_biome][new_location_index]
                image_path = f'{base_img_URL}{current_biome}_0{new_location_index + 1}.png'
            else:
                return err_map_ending

        case _: # else
            return 'Invalid direction!'

    return new_location, image_path