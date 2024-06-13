from flightfinder.flights.types import ErrorType, FlightResponseType, FlightType
from flightfinder.lib.airpeace import AirPeace
from flightfinder.lib.arik import Arik
from flightfinder.lib.greenafrica import GreenAfrica
from flightfinder.lib.ibomair import IbomAir
from flightfinder.lib.ng_eagle import NgEagle
from flightfinder.lib.utils import get_flights
import concurrent.futures
from flightfinder.lib.valuejet import ValueJet
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
            
            futures = {
                executor.submit(get_flights, Arik, date, origin, destination): 'Arik',
                
                executor.submit(get_flights, AirPeace, date, origin, destination): 'AirPeace',
                
                executor.submit(get_flights, IbomAir, date, origin, destination): 'IbomAir',
                
                executor.submit(get_flights, NgEagle, date, origin, destination): 'NgEagle',
                
                executor.submit(get_flights, GreenAfrica, date, origin, destination): 'GreenAfrica',
                
                executor.submit(get_flights, ValueJet, date, origin, destination): 'ValueJet'
            }

            results = []
            
            for future in concurrent.futures.as_completed(futures):
                airline = futures[future]
                try:
                    flights = future.result()
                    # Process flights here
                    results.extend(flights)
                except Exception as e:
                    print(f"An error occurred while getting flights for {airline}: {e}")
                    
        flights = results
        
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