from bs4 import BeautifulSoup, Tag
from playwright.sync_api import sync_playwright
from flightfinder.lib.constants import AIRPEACE_URL


class AirPeace:
    def __init__(self, date, location, destination):
        self.url = AIRPEACE_URL.format(location=location, destination=destination, departure_date=date)
        content = self.get_html_content()
        self.soup = BeautifulSoup(content, 'html.parser')
        self.flights = []
        self.name = "AirPeace"
    
    def get_html_content(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(self.url)
            page.wait_for_load_state('load')
            page.wait_for_timeout(5000)
            html_content = page.content()
            browser.close()
        return html_content

    def find_flights(self):
        div = self.soup.find('div', class_='scheduled-flights')

        for child in div.children:
            data = self.extract_data_from_item(child)
            if data:
                self.flights.append(data)
        return self.flights
    
    def extract_data_from_item(self, item):
        if not isinstance(item, Tag):
            return
        
        try:
            # Extract the time
            time_element = item.find('span', class_='time')
            time_string = time_element.text

            # Extract the flight number
            flight_number_element = item.find('span', class_='flight-no')
            flight_number_string = flight_number_element.text
            
            # Find mobile route
            mobile_route = item.find('div', class_='mobile-route-block')
            
            # Find all spans with class 'port'
            port_elements = mobile_route.find_all('span', class_='port')

            # Extract the text
            location_string = port_elements[0].text if port_elements else None
            destination_string = port_elements[1].text if len(port_elements) > 1 else None
            
            # Extract the cost
            try: 
                price_element = item.find('span', class_='price-text-single-line')
                price_string = price_element.text
            except Exception as e:
                price_element = item.find('span', class_='price-best-offer')
                price_string = price_element.text
            
            return {
                'flight_number': flight_number_string,
                'location': location_string,
                'destination': destination_string,
                'departure_time': time_string,
                'price': price_string,
                'airline': self.name,
                'url': self.url
            }
            
        except Exception as e:
            pass
    
        return None