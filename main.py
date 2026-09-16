import requests
import datetime
from zoneinfo import ZoneInfo

MY_LAT = 38.016874
MY_LONG = -121.889160

def is_dark():
    global MY_LAT, MY_LONG
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }
    response = requests.get('https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = datetime.datetime.fromisoformat(data['results']['sunrise'])
    sunrise_pst = sunrise.astimezone(ZoneInfo("America/Los_Angeles"))
    sunset = datetime.datetime.fromisoformat(data['results']['sunset'])
    sunset_pst = sunset.astimezone(ZoneInfo("America/Los_Angeles"))
        
    print(f"sunset is {sunrise_pst}")


response = requests.get('http://api.open-notify.org/iss-now.json')
response.raise_for_status()
response_code = response.status_code
print(response_code)
if(response_code == 200):
    print(response.json()["iss_position"])
else:
    print("something broke")

is_dark()