import graphene
from graphene_django import DjangoObjectType
from api.models import Products, Brands, Categories, Pictures, SmallPictures, Variants

class ProductType(DjangoObjectType):
    price = graphene.Float()
    sale_price = graphene.Float()
    class Meta:
        model = Products
       
class PictureType(DjangoObjectType):
    class Meta:
        model = Pictures
class SmallPictureType(DjangoObjectType):
    class Meta:
        model = SmallPictures
class CategoryType(DjangoObjectType):
    class Meta:
        model = Categories
class BrandType(DjangoObjectType):
    class Meta:
        model = Brands
class VariantType(DjangoObjectType):
    class Meta:
        model = Variants



