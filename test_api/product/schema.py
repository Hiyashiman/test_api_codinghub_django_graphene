import graphene 
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from product.models import *
from graphene import InputObjectType
from graphene import ObjectType, List, Int, String
from graphql_jwt.decorators import login_required

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fieds = '__all__'

class ProductDetailType(DjangoObjectType):
    class Meta:
        model = ProductsDetail
        fieds = '__all__'

class Query(object):
  all_products = List(ProductType, page=Int(), per_page=Int(), sort_by=String(), search=String())
  product = graphene.Field(ProductType, id=graphene.ID())

  all_product_detail = graphene.List(ProductDetailType)
  product_detail = graphene.Field(ProductDetailType, id=graphene.ID())

  def resolve_all_product_detail(self, info, **kwargs):
    return ProductsDetail.objects.all()

  def resolve_product_detail(self, info, id):
    return ProductsDetail.objects.get(pk=id)
  
  @login_required
  def resolve_all_products(self, info, page=1, per_page=10, sort_by=None, search=None):

    all_products = Product.objects.all()
    
    if sort_by:
        all_products = all_products.order_by(sort_by)

    if search:
        all_products = all_products.filter(type__icontains=search)

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_items = all_products[start_idx:end_idx]  
    return paginated_items  

  def resolve_product(self, info, id):
    return Product.objects.get(pk=id)

class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        type = graphene.String(required=True)
        item = graphene.String(required=True)

    def mutate(self, info, type,item):
        product = Product(
            type = type,
            item = item
        )
        product.save()

        return CreateProduct(product=product)

class InputProductDetail(InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    img = graphene.String()
    product = graphene.ID(required=True)

class CreateProductDetail(graphene.Mutation):
    productDetail = graphene.Field(ProductDetailType)

    class Arguments:
        product_detail_input = InputProductDetail()


    def mutate(self, info, product_detail_input):
        related_product = Product.objects.get(pk=product_detail_input.product)

        productDetail = ProductsDetail(
            name = product_detail_input.name,
            price = product_detail_input.price,
            img = product_detail_input.img,
            product = related_product
        )
        productDetail.save()
        return CreateProductDetail(productDetail=productDetail)
        
class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    product = graphene.Field(ProductType)

    def mutate(self, info, id):
        try:
            product = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            raise GraphQLError(f"Product with id {id} does not exist.")

        product.delete()
        return DeleteProduct(product=None)

class DeleteProductDetail(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    product_detail = graphene.Field(ProductDetailType)

    def mutate(self, info, id):
        try:
            product_detail = ProductsDetail.objects.get(pk=id)
        except ProductsDetail.DoesNotExist:
            raise GraphQLError(f"ProductDetail with id {id} does not exist.")

        product_detail.delete()

        return DeleteProductDetail(product_detail=None)

class UpdateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        id = graphene.ID()
        type = graphene.String(required=True)
        item = graphene.Int(required=True)

    def mutate(self, info, id, type, item):
        try:
            product = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            raise GraphQLError(f"Product with id {id} does not exist.")

        product.type = type 
        product.item = item 
        product.save()

        return UpdateProduct(product=product)


class UpdateProductDetail(graphene.Mutation):
    productDetail = graphene.Field(ProductDetailType)

    class Arguments:
        id = graphene.ID()
        product_detail_input = InputProductDetail()

    def mutate(self, info, id, product_detail_input):
        try:
            product_detail = ProductsDetail.objects.get(pk=id)
        except ProductsDetail.DoesNotExist:
            raise GraphQLError(f"ProductDetail with id {id} does not exist.")

        related_product = Product.objects.get(pk=product_detail_input.product)

        product_detail.name = product_detail_input.name
        product_detail.price = product_detail_input.price
        product_detail.img = product_detail_input.img
        product_detail.product = related_product

        product_detail.save()

        return UpdateProductDetail(productDetail=product_detail)



class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    create_product_detail = CreateProductDetail.Field()
    delete_product = DeleteProduct.Field()
    delete_product_detail = DeleteProductDetail.Field()
    update_product = UpdateProduct.Field()
    update_product_detail = UpdateProductDetail.Field()

