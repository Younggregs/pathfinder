def get_flights(airline, date, location, destination):
    return airline(date, location, destination).find_flights()