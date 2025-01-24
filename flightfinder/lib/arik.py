import requests
from bs4 import BeautifulSoup, Tag
from flightfinder.lib.constants import ARIK_URL


class Arik:
    def __init__(self, date, origin, destination):
        self.url = ARIK_URL.format(
            origin=origin, destination=destination, departure_date=date
        )
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.text, "html.parser")
        self.flights = []
        self.name = "arik_air"

    def find_flights(self):
        div = self.soup.find("div", class_="scheduled-flights")

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
            time_element = item.find("span", class_="time")
            time_string = time_element.text

            # Extract the flight number
            flight_number_element = item.find("span", class_="flight-no")
            flight_number_string = flight_number_element.text

            # Find mobile route
            mobile_route = item.find("div", class_="mobile-route-block")

            # Find all spans with class 'port'
            port_elements = mobile_route.find_all("span", class_="port")

            # Extract the text
            origin_string = port_elements[0].text if port_elements else None
            destination_string = (
                port_elements[1].text if len(port_elements) > 1 else None
            )

            # # Extract the currency
            # try:
            #     currency_element = item.find('span', class_='currency-best-offer')
            #     currency_string = currency_element.text
            # except Exception as e:
            #     currency_element = item.find('span', class_='currency')
            #     currency_string = currency_element.text

            # Extract the cost
            try:
                price_element = item.find("span", class_="price")
                price_string = price_element.text
            except Exception as e:
                try:
                    price_element = item.find("span", class_="price-best-offer")
                    price_string = price_element.text
                except Exception as e:
                    price_string = "-1"

            if price_string != "-1":
                price_string = price_string.replace(",", "")

            return {
                "flight_number": flight_number_string,
                "origin": origin_string,
                "destination": destination_string,
                "departure_time": time_string,
                "price": price_string,
                "currency": "₦",
                "airline": self.name,
                "url": self.url,
            }

        except Exception as e:
            pass

        return None
