import os
from pathlib import Path
from dotenv import load_dotenv
import requests

dotenv_path = Path('./env/.env')
load_dotenv(dotenv_path=dotenv_path)
api_key = os.getenv("METOFFICE_KEY")
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
# Choose one of these site IDs or use your own
#Manchester
site_id = "310013"
#url_fullSiteIDList=f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key={api_key}"
# Build the API request URL
def get_weather_manchester(api_key, site_id):
    url = f"http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/{site_id}?res=3hourly&key={api_key}"
    print(url)
# Send the request and get the response
    response = requests.get(url)

# Check for successful response
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()

        # Get current weather information
        current_weather = data["SiteRep"]["DV"]["Location"]["Period"][0]["Rep"][0]
        weather_cond=weather_dict.get(int(current_weather['W']), "Unknown")
        # Print basic weather data
        print(f"Location: {data['SiteRep']['DV']['Location']['name']}")
        print(f"Temperature: {current_weather['T']}°C")
        print(f"Wind: {current_weather['D']} {current_weather['S']} mph")
        print(f"Conditions: {weather_cond}")

    else:
      print(f"Error getting weather data: {response.status_code}")


  
get_weather_manchester(api_key, site_id)