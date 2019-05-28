# Generated by Django 2.2 on 2019-05-16 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalOperator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=32, verbose_name='uuid')),
                ('title', models.CharField(max_length=100, verbose_name='企业名称')),
                ('mobile', models.CharField(max_length=20, verbose_name='管理员手机号')),
                ('enterprise_id', models.IntegerField(verbose_name='基础库关联企业')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('owner', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='企业管理员')),
            ],
            options={
                'verbose_name': '药品运营商',
                'db_table': 'medicaloperator',
            },
        ),
    ]