import requests
import datetime
from zoneinfo import ZoneInfo
import smtplib
from geopy.distance import geodesic
import personal

MY_LAT = 38.016874
MY_LONG = -121.889160
MAX_DIST = 200

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

    current_hour = datetime.datetime.now().hour
    if current_hour > sunrise_pst.hour and current_hour < sunset_pst.hour:
        return True
    else:
        return False

def send_email():
    my_email = personal.my_email
    password = personal.password
    connection = smtplib.SMTP('smtp.gmail.com', 587)

    connection.starttls()

    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs="dipesh267@hotmail.com",
        msg = f"Subject: Look up for ISS near your \n\n look up dude the ISS is passing over your"
    )

def check_near_mylocation(lat, long):
    global MY_LAT, MY_LONG, MAX_DIST
    my_location = (MY_LAT, MY_LONG)
    target_location = (lat, long)

    distance = geodesic(my_location, target_location)

    if distance > MAX_DIST:
        send_email()
    else:
        print("not near you")

if is_dark():
    response = requests.get('http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    response_code = response.status_code
    if(response_code == 200):
        iss_position = response.json()["iss_position"]
        check_near_mylocation(iss_position['latitude'], iss_position['longitude'])
    else:
        print("something broke")
else:
    pass