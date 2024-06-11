from datetime import datetime
import requests
from flightfinder.lib.constants import GREEN_AFRICA_DIRECT_LINK, GREEN_AFRICA_URL


class GreenAfrica:
    def __init__(self, date, origin, destination):
        url = GREEN_AFRICA_URL.format(
            origin=origin, 
            destination=destination, 
            departure_date=self.format_date(date)
        )
        
        response = requests.get(url)
        data = response.json()
        flights = data['data']['flights']
        
        self.direct_link = GREEN_AFRICA_DIRECT_LINK.format(
            origin=origin, 
            destination=destination, 
            departure_date=self.format_date_with_dash(date)
        )
        self.flight_list = flights['flight']
        self.flight_bucket = []
        self.name = "Green Africa"
    
    def format_date(self, date_string):
        datetime_object = datetime.strptime(date_string, "%d.%m.%Y")
        formatted_date = datetime_object.strftime("%Y/%m/%d")
        return formatted_date
    
    def format_date_with_dash(self, date_string):
        datetime_object = datetime.strptime(date_string, "%d.%m.%Y")
        formatted_date = datetime_object.strftime("%Y-%m-%d")
        return formatted_date

    def getPrice(self, classes):
        # Check gSaver price
        gSaver = classes['gSaver']
        if gSaver and gSaver['totalfare'] != None:
            return f"{gSaver['currency']} {gSaver['totalfare']}"
        
        # Check gFlex price
        gFlex = classes['gFlex']
        if gFlex and gFlex['totalfare'] != None:
            return f"{gFlex['currency']} {gFlex['totalfare']}"
         
        # check gClassic price
        gClassic = classes['gClassic']
        if gClassic and gClassic['totalfare'] != None:
            return f"{gClassic['currency']} {gClassic['totalfare']}"
        
        return None
    
    def find_flights(self):
        for flight in self.flight_list:
            try: 
                journey = flight['journey'][0]
                
                code = journey['fltnum']
                origin = journey['fromcode']
                destination = journey['tocode']
                
                time_string = journey['STD']
                datetime_object = datetime.strptime(time_string, "%Y/%m/%d %H:%M:%S.%f")
                formatted_time = datetime_object.strftime("%H:%M")
                
                classes = journey['classes']
                try:
                    price = self.getPrice(classes)
                except Exception as e:
                    print ('price error: ', e)
                
                if price:
                    self.flight_bucket.append({
                        'flight_number': code,
                        'origin': origin,
                        'destination': destination,
                        'departure_time': formatted_time,
                        'price': price,
                        'airline': self.name,
                        'url': self.direct_link
                    })
                    
                    
            except Exception as e:
                pass
        
        return self.flight_bucket