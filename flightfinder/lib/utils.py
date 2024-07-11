from datetime import datetime


def get_flights(airline, date, origin, destination):
    return airline(date, origin, destination).find_flights()


def format_date_with_dash(date_string):
    datetime_object = datetime.strptime(date_string, "%d.%m.%Y")
    formatted_date = datetime_object.strftime("%Y-%m-%d")
    return formatted_date


def formate_time_string_to_date(time_string, date_string):
    # Parse the time string into a time object
    parsed_time = datetime.strptime(time_string, "%H:%M").time()

    # Convert the formatted date string back to a date object
    formatted_date = format_date_with_dash(date_string)
    date_object = datetime.strptime(formatted_date, "%Y-%m-%d").date()

    # Combine the date and time into a datetime object
    datetime_object = datetime.combine(date_object, parsed_time)

    return datetime_object


def get_location_code(locations, name):
    for location in locations:
        if location["name"].upper() == name.upper():
            return location["code"]
    return None
