from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from api.graphql.schema import schema

# from api.data.create_products import createDataView

urlpatterns = [
    path('graphiql/', 
    csrf_exempt(
        GraphQLView.as_view(
        graphiql=True, 
        schema=schema
        ))),

    path('graphql/', 
    csrf_exempt(
        GraphQLView.as_view(
        graphiql=False, 
        schema=schema
        ))),
    # path("create-products/", createDataView)    
]