import time

# Dictionary to store user stats and sessions with session-UUID as key
user_stats = {}

# store socket sessions (request.sid and cookie)
socket_sessions = []

# Time for a player to heal once
heal_interval = 10

# Function to regenerate user stats over time
def regenerate_stats(player):
    while user_stats[player]['regenerate'] == True:
        time.sleep(heal_interval) # Loop timer

        # regenerate stats
        if user_stats[player]['health'] < 100:
            user_stats[player]['health'] += 10
        if user_stats[player]['stamina'] < 100:
            user_stats[player]['stamina'] += 10

# Function to check cookie session for authentication
def check_session(session):
    if not session:
        return False
    if session not in user_stats:
        return False
    
    return True

# Time to throttle actions in seconds
throttle_interval = 2

# Function to throttle actions a user can execute in a certain amount of time
def throttle(session):
    if time.time() - user_stats[session]['last_action'] < throttle_interval:
        return True
    else:
        return False