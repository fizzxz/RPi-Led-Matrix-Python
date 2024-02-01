import os
from pathlib import Path
from dotenv import load_dotenv
import utilities
import requests
import json
import time

dotenv_path = Path('./env/.env')
load_dotenv(dotenv_path=dotenv_path)
api_key = os.getenv("METOFFICE_KEY")
site_id = os.getenv("SITE_ID")
weather_dict = {
    -1: "Trace rain",
    0: "Clear night",
    1: "Sunny day",
    2: "Partly cloudy (night)",
    3: "Partly cloudy (day)",
    4: "Not used",
    5: "Mist",
    6: "Fog",
    7: "Cloudy",
    8: "Overcast",
    9: "Light rain shower (night)",
    10: "Light rain shower (day)",
    11: "Drizzle",
    12: "Light rain",
    13: "Heavy rain shower (night)",
    14: "Heavy rain shower (day)",
    15: "Heavy rain",
    16: "Sleet shower (night)",
    17: "Sleet shower (day)",
    18: "Sleet",
    19: "Hail shower (night)",
    20: "Hail shower (day)",
    21: "Hail",
    22: "Light snow shower (night)",
    23: "Light snow shower (day)",
    24: "Light snow",
    25: "Heavy snow shower (night)",
    26: "Heavy snow shower (day)",
    27: "Heavy snow",
    28: "Thunder shower (night)",
    29: "Thunder shower (day)",
    30: "Thunder",
}

# Choose one of these site IDs provided here
#url_fullSiteIDList=f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key={api_key}"

def get_weather_data():
    """Retrieves weather data, either from the API or a cached file."""
    cache_file = "./metoffice/weather_data.json"
    max_cache_age = 3 * 60 * 60  # 3 hours in seconds

    # Check if cached data exists and is recent enough
    if (
        os.path.exists(cache_file)
        and time.time() - os.path.getmtime(cache_file) < max_cache_age
    ):
        with open(cache_file, "r") as f:
            data = json.load(f)
        print("Loading weather data from cache...")
    else:
        # Call the API to fetch fresh data
        data = get_weather_json()
        with open(cache_file, "w") as f:
            json.dump(data, f)
        print("Fetched new weather data from API.")
    return data

def get_weather_json():
    # Build the API request URL
    url = f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/{site_id}?res=3hourly&key={api_key}"
    
    # Send the request and get the response
    response = requests.get(url)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        return data

    else:
      return (f"Error getting weather data: {response.status_code}")

def print_weather_data(data):
    current_weather = data["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"][0]
    weather_cond=weather_dict.get(int(current_weather['W']), "Unknown")
    # Print basic weather data
    print(f"Location: {data['SiteRep']['DV']['Location']['name']}")
    print(f"Temperature: {current_weather['T']}°C")
    print(f"Wind: {current_weather['D']} {current_weather['S']} mph")
    print(f"Conditions: {weather_cond}")

def get_weather_forecast():
    #sleep for 3 minutes
    #when rebooting rpi time is incorrect at initial boot
    #wait for wifi to connect and time sync to occur
    time.sleep(180) 
    while True:
        utilities.weather_data = get_weather_data()
        time.sleep(10800)