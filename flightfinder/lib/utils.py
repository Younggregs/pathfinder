from datetime import datetime


def get_flights(airline, date, origin, destination):
    return airline(date, origin, destination).find_flights()

def format_date_with_dash(date_string):
    datetime_object = datetime.strptime(date_string, "%d.%m.%Y")
    formatted_date = datetime_object.strftime("%Y-%m-%d")
    return formatted_date

def get_location_code(locations, name):
    for location in locations:
        if location["name"].upper() == name.upper():
            return location["code"]
    return None
