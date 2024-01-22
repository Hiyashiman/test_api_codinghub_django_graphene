from django.contrib.auth import get_user_model, authenticate, login ,logout
import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_jwt.shortcuts import create_refresh_token, get_token
import graphql_jwt

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        ) 
        user.set_password(password)
        user.save()
        token = get_token(user)
        refresh_token = create_refresh_token(user)

        
        return CreateUser(user=user, token=token, refresh_token=refresh_token)

class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    token = graphene.String()
    refresh_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):

        user = authenticate(username=username, password=password)

        if user is not None:
            login(info.context, user)
            token = get_token(user)  
            refresh_token = create_refresh_token(user)

            return LoginUser(user=user, token=token, refresh_token=refresh_token)      
        else:
            raise Exception("Incorrent Username or Password")
        
class LogoutUser(graphene.Mutation):
    success = graphene.Boolean()

    @login_required
    def mutate(self, info):
        user = info.context.user

        if user.is_authenticated:
            logout(info.context)
            return LogoutUser(success=True)
        else:
            raise Exception('User is not authenticated.')
        
class DeleteUser(graphene.Mutation):
    success = graphene.Boolean()

    @login_required
    def mutate(self, info):

        user = info.context.user
        # user = get_user_model().objects.get(pk = 14)
        status = user.delete()
        if status:
            return DeleteUser(success = True)
        else:
            return Exception('Can not remove this user.')




class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    verify_token = graphql_jwt.Verify.Field()
    logout_user = LogoutUser.Field()
    delete_user = DeleteUser.Field()


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)
    all_users = graphene.List(UserType)

    @login_required
    def resolve_users(self, info):
        return get_user_model().objects.all()
    
    @login_required
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure!')
        return user
    
    @login_required
    def resolve_all_users(self ,info):
        users = get_user_model().objects.all()
        return users   
    
schema = graphene.Schema(query=Query, mutation=Mutation)
