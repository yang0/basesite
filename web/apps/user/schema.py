from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphene import Node
from .models import User
from graphene_django.filter import DjangoFilterConnectionField
import graphene


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (Node, )
        only_fields = ('nick', 'tel')
        filter_fields = {
            'nick': ['exact'],
            'tel': ['exact', 'icontains', 'istartswith']
            }


class Query(graphene.ObjectType):
    user = Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)
    hello = graphene.String()
    userCurrent = graphene.Field(UserNode)

    def resolve_hello(self, info):
        return "hello worlds"

    def resolve_user_current(self, info):
        return info.context.user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserNode)

    class Arguments:
        nick = graphene.String(required=True)
        password = graphene.String(required=True)
        tel = graphene.String(required=True)

    def mutate(self, info, nick, password, tel):
        user = get_user_model()(
            nick=nick,
            tel=tel,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
