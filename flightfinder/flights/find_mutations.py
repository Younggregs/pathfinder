from flightfinder.flights.types import ErrorType, FlightResponseType, FlightType
from flightfinder.lib.merlin import Merlin
from flightfinder.lib.utils import formate_time_string_to_date
import graphene


class FindFlightsMutation(graphene.Mutation):
    class Arguments:
        origin = graphene.String(required=True)
        destination = graphene.String(required=True)
        date = graphene.String(required=True)

    data = graphene.Field(FlightResponseType)
    errors = graphene.Field(ErrorType)
    success = graphene.Boolean()

    def mutate(self, info, origin, destination, date):
        # Summon Merlin.
        merlin = Merlin(origin, destination, date)

        # Perform magic.
        merlin.prepare_magic()
        merlin.abracadabra()
        flight_instances = merlin.persist_magic()

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

        return FindFlightsMutation(data=data, success=True, errors=None)
