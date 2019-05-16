# _*_coding:utf-8_*_

"""
@author: yang0@126.com
@time:  2019/5/9 13:35

"""

import graphene
import graphql_jwt
import apps.medicaloperator.schema
import apps.user.schema
import graphene
import graphql_jwt

class ObtainJSONWebToken(graphql_jwt.relay.JSONWebTokenMutation):
    """认证用户时除了token，还返回用户信息
    """
    user = graphene.Field(apps.user.schema.UserNode)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Query(
    apps.user.schema.Query,
    apps.medicaloperator.schema.Query, # Add your Query objects here
    graphene.ObjectType
):
    pass

class Mutation(
    apps.user.schema.Mutation,
    graphene.ObjectType
):
    """认证用户并返回token
    """
    user_login = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)