from django.db import models
from apps.user.models import User

# Create your models here.

class MedicalOperator(models.Model):
    uuid = models.CharField(u'uuid', max_length=32)
    title = models.CharField(u'企业名称', max_length=100)
    owner = models.ForeignKey(User, editable=False, verbose_name=u'企业管理员', on_delete=models.CASCADE)
    mobile = models.CharField(u'管理员手机号', max_length=20)
    enterprise_id = models.IntegerField(u'基础库关联企业')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    class Meta:
        db_table = 'medicaloperator'
        verbose_name = "药品运营商"

