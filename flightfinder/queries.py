from flightfinder.constants.accra import ACCRA
from flightfinder.constants.douala import DAKAR, DOUALA, FREETOWN
from flightfinder.flights.types import FlightResponseType, FlightType
from flightfinder.lib.utils import format_date_with_dash
from flightfinder.models import Airline, Airport, Flight, JourneyPath
from flightfinder.tasks import cache_flights
import graphene


class Query(graphene.ObjectType):
    """Query class for the schema"""

    get_flights = graphene.Field(
        FlightResponseType,
        date=graphene.Argument(graphene.String, required=True),
        origin=graphene.Argument(graphene.String, required=True),
        destination=graphene.Argument(graphene.String, required=True),
    )

    def resolve_get_flights(self, info, date, origin, destination):
        print("Start control")

        airports = Airport.objects.all()
        airlines = Airline.objects.all()

        airports_dict = {airport.code: airport for airport in airports}

        airlines_dict = {airline.slug: airline for airline in airlines}

        journey_paths = []
        origin = airports_dict.get("FNA")
        for i, v in enumerate(FREETOWN):
            try:
                destination = airports_dict.get(v["name"])
                for airline in v["airlines"]:
                    airline_instance = airlines_dict.get(airline)
                    journey_paths.append(
                        JourneyPath(
                            origin=origin,
                            destination=destination,
                            airline=airline_instance,
                        )
                    )
            except Exception as e:
                print(f"An error occurred while creating journey paths: {e}")

        JourneyPath.objects.bulk_create(journey_paths)
        print("journey_paths", journey_paths)

        # origin_instance = Airport.objects.get(code=origin)
        # destination_instance = Airport.objects.get(code=destination)

        # journey_paths = JourneyPath.objects.filter(
        #     origin=origin_instance.id, destination=destination_instance.id
        # )

        # journey_paths_ids = [journey_path.id for journey_path in journey_paths]

        # flight_instances = Flight.objects.filter(
        #     journey_path__in=journey_paths_ids, date=format_date_with_dash(date)
        # )

        # flights = [
        #     FlightType(
        #         flight_number=flight.flight_number,
        #         origin=flight.journey_path.origin.name,
        #         destination=flight.journey_path.destination.name,
        #         departure_time=flight.departure_time,
        #         price=flight.price,
        #         currency=flight.currency,
        #         airline=flight.journey_path.airline.slug,
        #         url=flight.url,
        #     )
        #     for flight in flight_instances
        # ]

        return FlightResponseType(flights=[], total=len(journey_paths))
