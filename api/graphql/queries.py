import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from api.models import Products, Brands, Categories, Pictures, Variants
from api.graphql.types import ProductType, PictureType, CategoryType, BrandType, VariantType
from api.graphql.responses import HomeResponseType, ProductSingleType, ShopResponseType

class HomeDataQuery(graphene.ObjectType):
    home_data = graphene.Field(HomeResponseType)

    def resolve_home_data(self, info):
        print("[QUERY] home_data")
        return HomeResponseType(products=Products.objects.all())

class ProductQuery(graphene.ObjectType):
    product = graphene.Field(ProductSingleType, id=graphene.ID(), only_data=graphene.Boolean())

    def resolve_product(self, info, id, only_data):
        print("[QUERY] product")
        product = Products.objects.get(product_id=id)
        print(id, product)
        if only_data:
            return ProductSingleType(single=product)
        else:
            categories = product.category.all()
            print(categories)
            
            # related_products_excluded = list(Products.objects.filter(category__in=categories).distinct().exclude(product_id=id))
            related_products = list(Products.objects.filter(category__in=categories).distinct())
            print(related_products)
            
            index = related_products.index(product)
            print(index)
            if len(related_products) > 2:
                if index == len(related_products)-1:
                    next_product = related_products[0]
                else:
                    next_product = related_products[index+1]

                prev_product = related_products[index-1]
                print("[prev-next]", prev_product, next_product)
                return ProductSingleType(
                    single=product,
                    prev=prev_product,
                    next=next_product,
                    related=related_products[:5]
                    )
            else:
            
                
                return ProductSingleType(
                    single=product,
                    related=related_products[:5]
                    )


'''
{
    # "color": [],
    # "size": [],
    "brand": [],
    "minPrice": null,
    "maxPrice": null,
    "sortBy": "default",
    "page": 3,
    "perPage": 5,
    "list": true
}
'''

'''
{
    "searchTerm": null,
    "color": null,
    "size": null,
    "brand": ["ritsika", "ajio"],
    "minPrice": 250,
    "maxPrice": 1000,
    "category": ["earrings", "bracelets"],
    "sortBy": null,
    "page": null,
    "perPage": null,
    "list": true
}
'''

class ShopDataQuery(graphene.ObjectType):
    shop_data = graphene.Field(ShopResponseType, page=graphene.Int(), searchTerm=graphene.String(), color=graphene.List(graphene.String), brand=graphene.List(graphene.String), minPrice=graphene.Int(), maxPrice=graphene.Int(), category=graphene.List(graphene.String), sortBy=graphene.String(), perPage=graphene.Int(), search=graphene.Boolean())

    def resolve_shop_data(self, info, page, searchTerm, color, brand, minPrice, maxPrice, category, sortBy, perPage, search):
        print("[QUERY] shop_data")
        filter_list = []
        if search:
            if searchTerm: 
                print("[QUERY] shop_data search", searchTerm)
                filter_list.append(Q(name__icontains=searchTerm) | Q(short_desc__icontains=searchTerm))
                filtered_data = Products.objects.filter(*filter_list)
                products = filtered_data[:6]
                print("[QUERY] shop_data search", products)
                return ShopResponseType(
                data=products,
                total_count=filtered_data.count(),
                )
        else:
            if searchTerm: 
                print("[QUERY] searchTerm", searchTerm)
                filter_list.append(Q(name__icontains=searchTerm))
            if color:
                print("[QUERY] color", color)
                colors_list = [color.title() for color in color]
                filter_list.append(Q(color_name__in=colors_list))
            if brand:
                print("[QUERY] brand", brand)
                brands_list = [b.title() for b in brand]
                brands = Brands.objects.filter(name__in = brands_list)
                filter_list.append(Q(brands__in=brands))
            if minPrice:
                print("[QUERY] maxPrice", maxPrice)
                filter_list.append(Q(sale_price__gte=minPrice))
            if maxPrice:
                print("[QUERY] minPrice", minPrice)
                filter_list.append(Q(sale_price__lte=maxPrice))
            if category:
                if len(category) > 0:
                    category = [cat for cat in category if len(cat) > 0]
                if len(category) == 0:
                    category = None
                if category:
                    print("[QUERY] category", category)
                    category = Categories.objects.filter(slug__in=category)
                    filter_list.append(Q(category__in=category))
            if sortBy:
                print("[QUERY] sortBy", sortBy)
                print("[QUERY] filtered", Products.objects.filter(*filter_list))
                sort_by = sortBy.lower()
                if sort_by == "default":
                    filtered_data = Products.objects.filter(*filter_list).order_by("name")
                elif sort_by == "high-to-low":
                    filtered_data = Products.objects.filter(*filter_list).order_by("-price")
                elif sort_by == "low-to-high":
                    filtered_data = Products.objects.filter(*filter_list).order_by("price")
                elif sort_by == "new":
                    filtered_data = Products.objects.filter(*filter_list).order_by("new")
                else:
                    filtered_data = Products.objects.filter(*filter_list)
            else:
                filtered_data = Products.objects.filter(*filter_list)

            print("[QUERY] shop_data filter len", len(filter_list))
            if not page:
                page = 1
            if not perPage:
                perPage = 5
            (start, end) = (perPage*(page-1), perPage*page)
            products = filtered_data[start:end]
            print(products)
            return ShopResponseType(
                data=products,
                total_count=filtered_data.count(),
                )

# @api_view(['POST'])
# def GetProductsView(request):
#     print(request.body)
#     data = json.loads(request.body.decode("utf-8").replace("'",'"'))
#     print("[Data]: ", data)
    
#     query_dict = {}
#     for key, value in data.items():
#         if value is not None:
#             query_dict[key] = value
#     print("[Query dict]: ", query_dict)
#     filter_list = []
#     for key, value in query_dict.items():
#         if key == "searchTerm":
#             response_list.append(Q(name__icontains=value))
#         if key == "brand":
#             print("[Brand]: ", value)
#             brands_list = [brand.title() for brand in value]
#             brands = Brands.objects.filter(name__in = brands_list)
#             print("[Brands]: ", brands)
#             response_list.append(Q(brands__in=brands))
#         if key == "minPrice":
#             response_list.append(Q(price__gte=value))
#         if key == "maxPrice":
#             response_list.append(Q(price__lte=value))
#         if key == "category":
#             print("[Category]: ", value)
#             category = Categories.objects.filter(slug__in=value)
#             print("[Categories]: ", category)
#             response_list.append(Q(category__in=category))
#         if key == "color":
#             print("[COLOR]: ", value)
#             colors_list = [color.title() for color in value]
#             response_list.append(Q(color_name__in=colors_list))
#             print("[Colour List]: ", response_list)
#     print("[Response List]: ", response_list)
    
#     sort_by = query_dict["sortBy"].lower()

#     if sort_by == "default":
#         filtered_data = Product.objects.filter(*response_list).order_by("name")
#     elif sort_by == "high-to-low":
#         filtered_data = Product.objects.filter(*response_list).order_by("-price")
#     elif sort_by == "low-to-high":
#         filtered_data = Product.objects.filter(*response_list).order_by("price")
#     elif sort_by == "recently-added":
#         filtered_data = Product.objects.filter(*response_list).order_by("new")
#     else:
#         filtered_data = Product.objects.filter(*response_list)
#     # serailizer = ProductSerializer(response_list, many=True)
#     print("[Filtered Data]: ", filtered_data)
#     filtered_data = ProductSerializer(filtered_data, many=True).data

#     return JsonResponse(filtered_data, status=status.HTTP_200_OK, safe=False)
