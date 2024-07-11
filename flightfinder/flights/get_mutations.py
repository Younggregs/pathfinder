from flightfinder.flights.types import ErrorType, FlightResponseType, FlightType
from flightfinder.lib.utils import format_date_with_dash
from flightfinder.models import Airport, Flight, JourneyPath
import graphene


class GetFlightsMutation(graphene.Mutation):
    class Arguments:
        origin = graphene.String(required=True)
        destination = graphene.String(required=True)
        date = graphene.String(required=True)

    data = graphene.Field(FlightResponseType)
    errors = graphene.Field(ErrorType)
    success = graphene.Boolean()

    def mutate(self, info, origin, destination, date):
        origin_instance = Airport.objects.get(code=origin)
        destination_instance = Airport.objects.get(code=destination)

        journey_paths = JourneyPath.objects.filter(
            origin=origin_instance.id, destination=destination_instance.id
        )

        journey_paths_ids = [journey_path.id for journey_path in journey_paths]

        flight_instances = Flight.objects.filter(
            journey_path__in=journey_paths_ids, date=format_date_with_dash(date)
        )

        flights = [
            FlightType(
                flight_number=flight.flight_number,
                origin=flight.journey_path.origin.name,
                destination=flight.journey_path.destination.name,
                departure_time=flight.departure_time,
                price=flight.price,
                currency=flight.currency,
                airline=flight.journey_path.airline.slug,
                url=flight.url,
                created_at=flight.created_at,
            )
            for flight in flight_instances
        ]

        data = FlightResponseType(flights=flights, total=len(flights))

        return GetFlightsMutation(data=data, success=True, errors=None)
