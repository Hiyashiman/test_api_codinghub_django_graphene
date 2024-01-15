import graphene 
from graphene_django import DjangoObjectType
from users_detail.models import UsersDetail
from django.contrib.auth import get_user_model, authenticate, login

class UserDetailType(DjangoObjectType):
    class Meta:
        model = UsersDetail
        fields = '__all__'

class CreateUserDetail(graphene.Mutation):
    userDetail = graphene.Field(UserDetailType)

    class Arguments:
        cardId = graphene.String(required = True)
        address = graphene.String(required = True)
        phoneNumber = graphene.String(required = True)
        fk = graphene.ID(required = True)

    def mutate(self ,info ,cardId,address,phoneNumber,fk):
        user =  user = get_user_model().objects.get(id=fk)
        userDetail = UsersDetail(
            cardId = cardId,
            address = address,
            phoneNumber = phoneNumber,
            author=user
        )
        userDetail.save()

        return CreateUserDetail(userDetail=userDetail)

class Mutation(graphene.ObjectType):
    create_user_detail = CreateUserDetail.Field()

