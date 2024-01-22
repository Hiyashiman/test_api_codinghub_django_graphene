import graphene
import users.schema
import users_detail.schema
import product.schema 

class Query(users.schema.Query
            ,product.schema.Query
            , graphene.ObjectType):
    pass

class Mutation(product.schema.Mutation
               ,users.schema.Mutation
               ,users_detail.schema.Mutation
               , graphene.ObjectType):
    pass   


schema = graphene.Schema(query=Query, mutation=Mutation)