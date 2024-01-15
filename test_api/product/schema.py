import graphene 
from graphene_django import DjangoObjectType
from product.models import *
from graphene import InputObjectType
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fieds = '__all__'

class ProductDetailType(DjangoObjectType):
    class Meta:
        model = ProductsDetail
        fieds = '__all__'

class Query(object):
  all_products = graphene.List(ProductType)
  product = graphene.Field(ProductType, id=graphene.ID())

  all_product_detail = graphene.List(ProductDetailType)
  product_detail = graphene.Field(ProductDetailType, id=graphene.ID())

  def resolve_all_product_detail(self, info, **kwargs):
    return ProductsDetail.objects.all()

  def resolve_product_detail(self, info, id):
    return ProductsDetail.objects.get(pk=id)

  def resolve_all_products(self, info, **kwargs):
    return Product.objects.all()

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
    product = Product.objects.get(pk=id)
    if product is not None:
      product.delete()
    return DeleteProduct(product=product)


class DeleteProductDetail(graphene.Mutation):
  class Arguments:
    id = graphene.ID()

  product_detail = graphene.Field(ProductDetailType)

  def mutate(self, info, id):
    product_detail = ProductsDetail.objects.get(pk=id)
    if product_detail is not None:
      product_detail.delete()
    return DeleteProductDetail(product_detail=product_detail)


class UpdateProduct(graphene.Mutation):
  
  product = graphene.Field(ProductType)
  class Arguments:
    id = graphene.ID()
    type = graphene.String(required=True)
    item = graphene.String(required=True)

  def mutate(self, info, id, type,item):
    product = Product.objects.get(pk=id)
    product.type = type if type is not None else product.type
    product.item = item if item is not None else product.item
    product.save()
    return UpdateProduct(product=product)

class UpdateProductDetail(graphene.Mutation):
  productDetail = graphene.Field(ProductDetailType)

  class Arguments:
        id =graphene.ID()
        product_detail_input = InputProductDetail()


  def mutate(self, info, id, product_detail_input):
    product_detail = ProductsDetail.objects.get(pk=id)
    related_product = Product.objects.get(pk=product_detail_input.product)

    product_detail.name = product_detail_input.name
    product_detail.price = product_detail_input.price
    product_detail.img = product_detail_input.img
    product_detail.product = related_product
    
    product_detail.save()
    return UpdateProductDetail(product_detail=product_detail)



class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    create_product_detail = CreateProductDetail.Field()
    delete_product = DeleteProduct.Field()
    delete_product_detail = DeleteProductDetail.Field()
    update_product = UpdateProduct.Field()
    update_product_detail = UpdateProductDetail.Field()

