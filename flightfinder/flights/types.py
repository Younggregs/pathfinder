import graphene


class FlightType(graphene.ObjectType):
    """Flight type"""

    flight_number = graphene.String()
    origin = graphene.String()
    destination = graphene.String()
    departure_time = graphene.String()
    price = graphene.String()
    currency = graphene.String()
    airline_slug = graphene.String()
    airline_name = graphene.String()
    url = graphene.String()
    created_at = graphene.String()


class FlightResponseType(graphene.ObjectType):
    """Flight response type"""

    flights = graphene.List(FlightType)
    total = graphene.Int()


class ErrorType(graphene.ObjectType):
    message = graphene.String()
