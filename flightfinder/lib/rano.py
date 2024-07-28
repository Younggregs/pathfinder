from datetime import datetime
from bs4 import BeautifulSoup, Tag
import requests
from flightfinder.lib.utils import get_location_code
from playwright.sync_api import sync_playwright, Page
from flightfinder.lib.constants import LOCATIONS, RANO_URL


class Rano:
    def __init__(self, date, origin, destination):
        self.date = self.format_date(date)
        self.origin = origin
        self.destination = destination

        self.url = ""

        content = self.get_html_content()
        self.soup = BeautifulSoup(content, "html.parser")

        self.flights = []
        self.name = "rano_air"

    def format_date(self, date):
        # Parse the original date string
        parsed_date = datetime.strptime(date, "%d.%m.%Y")

        # Add two days to the parsed date
        new_date = parsed_date.replace(day=parsed_date.day + 2)

        # Format the new date to the desired format
        formatted_date = new_date.strftime("%d-%b-%Y")

        return formatted_date

    def set_departure_date(self, page: Page, date_value):
        # JavaScript code to set the value and trigger change event
        js_code = f"""
        const input = document.querySelector('#departuredate');
        input.value = '{date_value}';
        input.dispatchEvent(new Event('change'));
        """
        page.evaluate(js_code)

    def get_availiability_url(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            page.goto(RANO_URL)

            page.wait_for_load_state("load")

            page.select_option("#Origin", self.origin)
            page.select_option("#Destination", self.destination)
            # Select one way
            # try:
            #     page.wait_for_selector('#ReturnTrip2', state='visible')
            #     page.click('#ReturnTrip2')
            # except Exception as e:
            #     print(f"Error clicking the element: {e}")
            #     # Fallback to JavaScript click
            #     page.evaluate("document.querySelector('#ReturnTrip2').click()")
            self.set_departure_date(page, self.date)

            # Submit form
            page.click("#submitButton")

            page.wait_for_load_state("load")

            page.wait_for_timeout(5000)

            new_page_url = page.url

            browser.close()

        return new_page_url

    def get_html_content(self):
        self.url = self.get_availiability_url()
        response = requests.get(self.url)
        return response.text

    def find_flights(self):
        div = self.soup.find_all("div", class_="flt-panel-heading")

        for child in div:
            data = self.extract_data_from_item(child)
            if data:
                self.flights.append(data)
        return self.flights

    def extract_data_from_item(self, item):
        if not isinstance(item, Tag):
            return

        try:
            time_element = item.find_all("div", class_="time")
            time_string = time_element[0].text if time_element else None

            locations_element = item.find_all("div", class_="city")
            origin_string = locations_element[0].text if locations_element else None

            destination_string = (
                locations_element[1].text if len(locations_element) > 1 else None
            )

            # Destination string maybe inbound so check for that
            # This is because this works for round trips for now.
            destination_code = get_location_code(LOCATIONS, destination_string)
            if destination_code == self.origin:
                raise ValueError("Destination is the same as origin")

            # Extract flight number
            flight_number_element = item.find("div", class_="flightnumber")
            flight_number_string = (
                flight_number_element.text if flight_number_element else None
            )

            price_string = item.find("div", class_="fare-price-small").text
            if price_string is None or price_string.strip().lower() == "sold out":
                price_string = "-1"

            price = (
                "-1"
                if not price_string
                else price_string.replace("NGN", "").replace(",", "")
            )

            return {
                "flight_number": flight_number_string.strip(),
                "origin": origin_string.strip(),
                "destination": destination_string.strip(),
                "departure_time": time_string.strip(),
                "price": price.strip(),
                "currency": "₦",
                "airline": self.name,
                "url": self.url,
            }

        except Exception as e:
            pass

        return None
