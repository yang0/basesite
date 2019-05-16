# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)


class MyUserManager(BaseUserManager):
    def create_user(self, tel, nick, password=None, **extra_fields):
        """
        创建一个用户，用户名是tel，和密码
        """
        now = datetime.now()
        if not tel:
            raise ValueError(u'用户名必须是手机号码')
        user = self.model(tel=tel, nick=nick, create_time=now, update_time=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tel, nick, password, **extra_fields):
        """
        创建一个超级用户
        """
        u = self.create_user(tel=tel, nick=nick, password=password, **extra_fields)
        u.is_staff = True
        u.is_superuser = True
        u.save(using=self._db)
        return u

    class Meta:
        app_label = (u'eyaos_tf')


# 用户
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.CharField(u'邮箱', max_length=50, blank=True)
    nick = models.CharField(u'昵称', max_length=20, unique=True)
    name = models.CharField(u'姓名', max_length=15, blank=True)
    tel = models.CharField(u'手机号码', max_length=15, unique=True, db_index=True)
    reg_ip = models.CharField(u'注册IP', max_length=15, blank=True)
    login_ip = models.CharField(max_length=15, blank=True)
    is_staff = models.BooleanField(u'是否内部人员', default=False)
    is_active = models.BooleanField(u'有效账号', default=True)
    create_time = models.DateTimeField(u'注册时间', auto_now_add=True)
    update_time = models.DateTimeField(null=True, auto_now=True)
    msg_num = models.IntegerField(u'未读消息数', default=0)
    sysmsg_num = models.IntegerField(u'未读的系统消息数', default=0)

    class Meta:
        db_table = 'user'
        verbose_name = verbose_name_plural = (u'用户')

    objects = MyUserManager()
    USERNAME_FIELD = 'tel'
    REQUIRED_FIELDS = ['nick']
    # 用户所在群组
    GROUPS_IDS = None

    def get_full_name(self):
        return self.tel

    def get_short_name(self):
        return self.tel

    @property
    def is_admin(self):
        """超级管理员"""
        return (1 in self.my_groups())

    @property
    def is_operator(self):
        """运营人员"""
        return (2 in self.my_groups())

    @property
    def is_user(self):
        """普通用户"""
        if self.my_groups():
            return False
        return True

    def my_groups(self):
        if self.GROUPS_IDS is None:
            self.GROUPS_IDS = []
            if self.is_authenticated():
                glist = self.groups.all()
                for g in glist:
                    self.GROUPS_IDS.append(g.id)
        return self.GROUPS_IDS

    def __unicode__(self):
        return self.tel



