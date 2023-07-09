import dataclasses
import datetime
import requests

def convert_to_12hr(time_str):
    # convert string to datetime object
    datetime_object = datetime.datetime.strptime(time_str, '%H:%M:%S')

    # extract hours and minutes from datetime object
    hours = datetime_object.hour
    minutes = datetime_object.minute

    # determine whether it's AM or PM
    if hours < 12:
        suffix = 'AM'
    else:
        suffix = 'PM'

    # convert hours to 12-hour format
    if hours == 0:
        hours = 12
    elif hours > 12:
        hours -= 12
    
     # create a formatted string and return it
    time_12hr = '{:02d}:{:02d} {}'.format(hours, minutes, suffix)
    return time_12hr

def getETA(origin, dest):
    url = 'https://api.radar.io/v1/route/distance'
    params = {
        'origin': f"{origin['latitude']}, {origin['longitude']}" ,
        'destination': f"{dest['latitude']}, {dest['longitude']}",
        'modes': 'bike',
        'units': 'metric'
    }
    headers = {
            'Authorization': 'prj_test_sk_7f18bfd0b153e1a0f99f422c6ef649dd729d4b41',
            'Content-Type': 'application/json'
        }
    
    response = requests.get(url=url, params=params, headers=headers)

    if response.status_code == 200:
        return response.json()['routes']['bike']