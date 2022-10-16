import graphene
from api.graphql.types import ProductType

class HomeResponseType(graphene.ObjectType):
    products = graphene.List(ProductType)

class ProductSingleType(graphene.ObjectType):
    single = graphene.Field(ProductType)
    prev = graphene.Field(ProductType)
    next = graphene.Field(ProductType)
    related = graphene.List(ProductType)

class ShopResponseType(graphene.ObjectType):
    data = graphene.List(ProductType)
    total_count = graphene.Int()