from flightfinder.flights.mutations import FlightsMutation
import graphene

class Mutation(graphene.ObjectType):
    flights = FlightsMutation.Field()