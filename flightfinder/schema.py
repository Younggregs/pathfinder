import graphene

from flightfinder.queries import Query
from flightfinder.mutations import Mutation

schema = graphene.Schema(query=Query)