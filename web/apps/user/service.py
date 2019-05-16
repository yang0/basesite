# _*_coding:utf-8_*_

import logging, json, os
from apps.user.models import *

logger = logging.getLogger(__name__)


def getUserCountByProp(prop):
    if isinstance(prop, dict):
        return User.objects.filter(**prop).count()
    else:
        logger.error("the param of prop must be the class dict")
        return False


def getUserObjByProp(prop):
    if isinstance(prop, dict):
        uList = User.objects.filter(**prop)[0:1]
        if uList:
            return uList[0]
        else:
            return None
    else:
        logger.error("the param of prop must be the class dict")
        return False


def getUserListByProp(prop):
    """用户列表"""
    if isinstance(prop, dict):
        return User.objects.filter(**prop).order_by("-id")
    else:
        logger.error("the param of prop must be the class dict")
        return False


def insertUser(obj):
    if isinstance(obj, User):
        obj.save()
        return obj.id
    else:
        logger.error("the param's class must be User")
    return False


def updateUserByProp(prop, data):
    if isinstance(prop, dict) and isinstance(data, dict):
        return User.objects.filter(**prop).update(**data)
    else:
        logger.error("the param class of prop and data must be dict")
        return False
