def get_flights(airline, date, origin, destination):
    return airline(date, origin, destination).find_flights()