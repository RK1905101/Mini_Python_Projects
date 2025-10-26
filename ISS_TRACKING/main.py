import requests
import datetime
import smtplib

# Your current location coordinates
MY_LAT = 22.691586   # Latitude
MY_LONG = 72.863365  # Longitude

def isIssNear():
    """
    Checks if the International Space Station (ISS) is currently near your location.
    """
    # Fetch current ISS position from open API
    responseISS = requests.get("http://api.open-notify.org/iss-now.json")
    responseISS.raise_for_status()  # Raise error if request fails

    # Extract ISS latitude and longitude from API response
    longitude = float(responseISS.json()["iss_position"]["longitude"])
    latitude = float(responseISS.json()["iss_position"]["latitude"])

    # Check if ISS is within ±5° range of your location
    if (MY_LAT - 5 <= latitude <= MY_LAT + 5) and (MY_LONG - 5 <= longitude <= MY_LONG + 5):
        return True


def isNight():
    """
    Determines if it is currently nighttime at your location using sunrise-sunset API.
    """
    # Define parameters for the API request
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,  # Get time in ISO 8601 format
    }

    # Fetch sunrise and sunset times
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    # Extract sunrise and sunset times from response
    sunRise = response.json()["results"]["sunrise"]
    sunSet = response.json()["results"]["sunset"]

    # Extract hour part from sunrise and sunset times (in UTC)
    sunRiseHour = int(sunRise.split("T")[1].split(":")[0])
    sunSetHour = int(sunSet.split("T")[1].split(":")[0])

    # Get current hour (local system time)
    timeNowHour = datetime.datetime.now().hour

    # If current time is after sunset or before sunrise, it's night
    if timeNowHour >= sunSetHour or timeNowHour <= sunRiseHour:
        return True


def sendmail():
    """
    Sends an email notification if ISS is overhead at night.
    """
    # Connect to Gmail's SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()  # Secure the connection with TLS
        # Login using app password (not normal password)
        connection.login("abc@gmail.com", "idbw herb vdyh")
        # Send the email
        connection.sendmail(
            from_addr="abc@gmail.com",
            to_addrs="xyz@gmail.com",
            msg="Subject: Look Up 👆\n\nThe ISS is currently overhead! Go outside and look up!",
        )


# Main logic: check if ISS is nearby and it's night, then send an email alert
if isIssNear() and isNight():
    sendmail()
