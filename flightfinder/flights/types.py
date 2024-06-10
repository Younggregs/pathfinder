import graphene

class FlightType(graphene.ObjectType):
    """ Flight type """
    flight_number = graphene.String()
    location = graphene.String()
    destination = graphene.String()
    departure_time = graphene.String()
    price = graphene.String()
    airline = graphene.String()
    url = graphene.String()
    
class FlightResponseType(graphene.ObjectType):
    """ Flight response type """
    flights = graphene.List(FlightType)
    total = graphene.Int()