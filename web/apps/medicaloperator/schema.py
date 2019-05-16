# _*_coding:utf-8_*_

"""
@author: yang0@126.com
@time:  2019/5/9 12:00

"""

import graphene

from graphene_django.types import DjangoObjectType

from .models import MedicalOperator


class MedicalOperatorType(DjangoObjectType):
    class Meta:
        model = MedicalOperator


class Query(object):
    all_medicaloperators = graphene.List(MedicalOperatorType)

    def resolve_all_medicaloperators(self, info, **kwargs):
        return MedicalOperator.objects.all()
