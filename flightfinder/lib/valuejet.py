from bs4 import BeautifulSoup, Tag
from flightfinder.lib.utils import format_date_with_dash
from playwright.sync_api import sync_playwright
from flightfinder.lib.constants import VALUE_JET_URL


class ValueJet:
    def __init__(self, date, origin, destination):
        self.url = VALUE_JET_URL.format(origin=origin, destination=destination, departure_date=format_date_with_dash(date))
        content = self.get_html_content()
        self.soup = BeautifulSoup(content, 'html.parser')
        self.flights = []
        self.name = "Value Jet"
    
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
        div = self.soup.find('div', id='outbound')
        flights_list = div.find_all('div', class_='border-gray-200')

        for child in flights_list:
            data = self.extract_data_from_item(child)
            if data:
                self.flights.append(data)
        return self.flights
    
    def extract_data_from_item(self, item):
        if not isinstance(item, Tag):
            return
        
        try:
            # Extract flight number
            flight_number_element = item.find('div', class_='basis-3')
            flight_number_string = flight_number_element.find('p').text
            
            # Find all spans with class 'port'
            port_elements = item.find_all('span', class_='basis-1')
            
            origin_element = port_elements[0].find_all('span')
            origin_string = origin_element[0].text if origin_element else None
            
            # Split origin string to get the origin
            origin = origin_string.split('\n')[0]
            
            time_string = origin_element[2].text if origin_element else None
            
            destination_element = port_elements[1].find_all('span')
            destination_string = destination_element[0].text if destination_element else None
            
            price_element = item.find('button').text
            
            return {
                'flight_number': flight_number_string.strip(),
                'origin': origin.strip(),
                'destination': destination_string.strip(),
                'departure_time': time_string.strip(),
                'price': price_element.strip(),
                'airline': self.name,
                'url': self.url
            }
            
        except Exception as e:
            pass
    
        return None