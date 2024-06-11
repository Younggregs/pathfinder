from flightfinder.flights.types import ErrorType, FlightResponseType, FlightType
from flightfinder.lib.airpeace import AirPeace
from flightfinder.lib.arik import Arik
from flightfinder.lib.ibomair import IbomAir
from flightfinder.lib.utils import get_flights
import concurrent.futures
import graphene

class FlightsMutation(graphene.Mutation):
    class Arguments:
        origin = graphene.String(required=True)
        destination = graphene.String(required=True)
        date = graphene.String(required=True)

    data = graphene.Field(FlightResponseType)
    errors = graphene.Field(ErrorType)
    success = graphene.Boolean()

    def mutate(self, info, origin, destination, date):
        # Get flights concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            arik_future = executor.submit(get_flights, Arik, date, origin, destination)
            
            airpeace_future = executor.submit(get_flights, AirPeace, date, origin, destination)
            
            ibomair_future = executor.submit(get_flights, IbomAir, date, origin, destination)

            arik_flights = arik_future.result()
            airpeace_flights = airpeace_future.result()
            ibomair_flights = ibomair_future.result()

        flights = []
        if arik_flights:
            flights.extend(arik_flights)
        if airpeace_flights:
            flights.extend(airpeace_flights)
        if ibomair_flights:
            flights.extend(ibomair_flights)
        
        print('Flights:', flights)
        
        # Convert each flight in the list to a FlightType object
        flights = [FlightType(
            flight_number=flight['flight_number'],
            origin=flight['origin'],
            destination=flight['destination'],
            departure_time=flight['departure_time'],
            price=flight['price'],
            airline=flight['airline'],
            url=flight['url']
        ) for flight in flights]
        data = FlightResponseType(flights= flights, total= len(flights))
        
        return FlightsMutation(data=data, success=True, errors=None)