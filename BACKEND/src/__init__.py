import json
import random
import secrets

# Function to get the value of a key from config.json
def get_config(key):
    config_file = "D:\\Venkatesh\\app\\BACKEND\\src\\config.json" # always use absolute path, not relative path
    file = open(config_file, "r")
    config = json.loads(file.read())
    file.close()
    
    if key in config:
        return config[key]
    else:
        raise Exception("Key {} is not found in config.json".format(key))



# Function to generate a random OTP using secrets module

def generate_otp():
    otp = secrets.randbelow(1000000)  # Generate a random 6-digit OTP
    return otp
