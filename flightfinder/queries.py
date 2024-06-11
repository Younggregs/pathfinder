from flightfinder.flights.types import FlightResponseType
from flightfinder.lib.airpeace import AirPeace
from flightfinder.lib.arik import Arik
from flightfinder.lib.ibomair import IbomAir
from flightfinder.lib.utils import get_flights
import concurrent.futures
import graphene

class Query(graphene.ObjectType):
    """ Query class for the schema """
    get_flights = graphene.Field(FlightResponseType, date=graphene.Argument(graphene.String, required=True), origin=graphene.Argument(graphene.String, required=True), destination=graphene.Argument(graphene.String, required=True))
    
    def resolve_get_flights(self, info, date, origin, destination):
        """ Method to get flights """
        
        # Get flights concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            
            arik_future = executor.submit(get_flights, Arik, date, origin, destination)
            
            airpeace_future = executor.submit(get_flights, AirPeace, date, origin, destination)
            
            ibomair_future = executor.submit(get_flights, IbomAir, date, origin, destination)

            arik_flights = arik_future.result()
            airpeace_flights = airpeace_future.result()
            ibomair_flights = ibomair_future.result()

        flights = arik_flights + airpeace_flights + ibomair_flights
        
        return {
            'flights': flights,
            'total': len(flights)
        }