import json

# Function to get the value of a key from config.json
def get_config(key):
    config_file = "/home/Mystery700/app/BACKEND/src/config.json" # always use absolute path, not relative path
    file = open(config_file, "r")
    config = json.loads(file.read())
    file.close()
    
    if key in config:
        return config[key]
    else:
        raise Exception("Key {} is not found in config.json".format(key))
