import requests
from datetime import datetime
import smtplib
import time
import os

UTC_OFFSET = 11
def convert_to_local_time(utc_time):
    if utc_time - UTC_OFFSET < 0:
        return utc_time - UTC_OFFSET + 24
    else:
        return utc_time - UTC_OFFSET


def is_dark():
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    sunrise = int(response.json()['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(response.json()['results']['sunset'].split('T')[1].split(':')[0])

    local_sunrise = convert_to_local_time(sunrise)
    local_sunset = convert_to_local_time(sunset)

    time_now = datetime.now()
    hour_now = time_now.hour
    if hour_now < local_sunrise:
        return True
    elif local_sunset < hour_now:
        return True


def send_notification_email():
    my_email = os.environ['SEND_EMAIL_ADDRESS']
    # MY_PASSWORD IS APP PASSWORD
    my_password = os.environ['EMAIL_PASSWORD']

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=os.environ['RECEIVE_EMAIL_ADDRESS'],
                            msg="Subject:ISS flying overhead right now! \n\n"
                                "The ISS is currently flying overhead! Look up!")


# BELOW IS TO FIND CURRENT PLACE'S SUNRISE AND SUNSET TIMES
MY_LAT = float(os.environ['MY_LAT'])
MY_LON = float(os.environ['My_LON'])
print(MY_LAT)
print(type(MY_LAT))
parameters = {
    "lat": MY_LAT,
    "lng": MY_LON,
    'formatted': 0
}


# BELOW IS TO FIND ISS LOCATION
response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


while True:
    time.sleep(300)
    if -5 <= iss_latitude - MY_LAT <= 5 and -5 <= iss_longitude - MY_LON <= 5:
        if is_dark():
            send_notification_email()