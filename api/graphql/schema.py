import graphene
# from django.db.models import Q
from api.graphql.queries import HomeDataQuery, ProductQuery, ShopDataQuery

# class Query(graphene.ObjectType):
#     get_products = graphene.List(ProductType)
#     get_product = graphene.Field(ProductType, id=graphene.ID())
#     # home_data = graphene.Field(HomeResponseType)

#     def resolve_get_products(self, info):  # resolve_books is a resolver
#         return Products.objects.all() 

#     def resolve_get_product(self, info, id):
#         return Products.objects.get(id=id)

    # def resolve_home_data(self, info):
    #     return HomeResponseType(products=Products.objects.all())

    
        


class Query(ShopDataQuery, HomeDataQuery, ProductQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(
    query=Query,
)