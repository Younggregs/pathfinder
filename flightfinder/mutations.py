from flightfinder.flights.find_mutations import FindFlightsMutation
from flightfinder.flights.get_mutations import GetFlightsMutation
import graphene


class Mutation(graphene.ObjectType):
    findFlights = FindFlightsMutation.Field()
    getFlights = GetFlightsMutation.Field()
