from datetime import date, datetime, time
from flightfinder.lib.utils import (
    format_date_with_dash,
    formate_time_string_to_date,
    get_flights,
)
import concurrent.futures
from flightfinder.lib.airpeace import AirPeace
from flightfinder.lib.arik import Arik
from flightfinder.lib.greenafrica import GreenAfrica
from flightfinder.lib.ibomair import IbomAir
from flightfinder.lib.max import Max
from flightfinder.lib.ng_eagle import NgEagle
from flightfinder.lib.rano import Rano
from flightfinder.lib.unitednigeria import UnitedNigeria
from flightfinder.lib.valuejet import ValueJet

from flightfinder.models import Flight, JourneyPath

from django.utils import timezone


class Merlin:
    def __init__(self, origin, destination, date):
        self.origin = origin
        self.destination = destination
        self.date = date
        self.journey_paths = []
        self.flights = []

    def prepare_magic(self):
        """Get all journey paths"""
        journey_paths = JourneyPath.objects.filter(
            origin__code=self.origin, destination__code=self.destination
        )
        self.journey_paths = journey_paths

    def abracadabra(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:

            futures = {}
            for path in self.journey_paths:
                slug = path.airline.slug
                future = executor.submit(
                    get_flights,
                    self.get_airline_by_slug(slug),
                    self.date,
                    self.origin,
                    self.destination,
                )
                futures[future] = slug

            results = []

            for future in concurrent.futures.as_completed(futures):
                airline = futures[future]
                try:
                    flights = future.result()
                    # Process flights here
                    results.extend(flights)
                except Exception as e:
                    print(f"An error occurred while getting flights for {airline}: {e}")

        self.flights = results

    def persist_magic(self):
        if not self.flights:
            return []

        try:
            flights_instances = [
                Flight(
                    journey_path=self.find_journey_path_by_slug(flight["airline"]),
                    flight_number=flight["flight_number"],
                    date=format_date_with_dash(self.date),
                    departure_time=formate_time_string_to_date(
                        flight["departure_time"], self.date
                    ),  # Make the datetime timezone-aware
                    arrival_time=timezone.make_aware(
                        datetime.combine(date.today(), time())
                    ),  # Make the datetime timezone-aware
                    price=flight["price"],
                    currency=flight["currency"],
                    url=flight["url"],
                )
                for flight in self.flights
                if self.find_journey_path_by_slug(flight["airline"])
            ]
        except Exception as e:
            print("An error occurred while preparing flights instances: ", e)
            return []

        unique_journey_path_ids = {
            flight.journey_path.id for flight in flights_instances
        }

        try:
            # Delete existing flights for the journey path
            flights_to_delete = Flight.objects.filter(
                journey_path__in=unique_journey_path_ids,
                date=format_date_with_dash(self.date),
            )
            flights_to_delete.delete()
        except Exception as e:
            print("An error occurred while deleting existing flights: ", e)

        try:
            Flight.objects.bulk_create(flights_instances)
        except Exception as e:
            print("An error occurred while creating flights: ", e)
            return []

        journey_path_ids = [path.id for path in self.journey_paths]

        flight_instances = Flight.objects.filter(
            journey_path__in=journey_path_ids, date=format_date_with_dash(self.date)
        )

        return flight_instances

    def find_journey_path_by_slug(self, slug):
        for path in self.journey_paths:
            if path.airline.slug == slug:
                return path
        return None

    def get_airline_by_slug(self, slug):
        airlines = {
            "air_peace": AirPeace,
            "arik_air": Arik,
            "green_africa": GreenAfrica,
            "ibom_air": IbomAir,
            "max_air": Max,
            "ng_eagle": NgEagle,
            "rano_air": Rano,
            "united_nigeria": UnitedNigeria,
            "value_jet": ValueJet,
        }

        return airlines.get(slug, None)
