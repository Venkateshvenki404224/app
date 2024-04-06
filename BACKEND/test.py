import requests

def get_geolocation(api_key):
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key=" + api_key
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "homeMobileCountryCode": 310,
        "homeMobileNetworkCode": 410,
        "radioType": "gsm",
        "carrier": "Vodafone",
        "considerIp": True
    }

    response = requests.post(url, headers=headers, json=data)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Request failed with status code " + str(response.status_code)}

# Replace 'YOUR_API_KEY' with your actual API key
api_key = 'AIzaSyCSbp6SvfkQQ9MRvLk1ouSJ5js6lxaOdGc'
result = get_geolocation(api_key)
print(result)


# My api = AIzaSyCAaRHlm9nfYaWBE-rNoMxMyUxYTvy0HKY
