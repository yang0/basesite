# encoding: utf-8

from django.forms import ModelForm, Textarea, TextInput, CharField, ChoiceField
from apps.user.models import User


class ContactForm(ModelForm):
    name = CharField(max_length=15, min_length=2, required=True, label='姓名')
    tel = CharField(max_length=15, min_length=7, required=True, label='电话或手机')

    class Meta:
        model = User
        fields = ['name', 'tel']


class CreateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['tel', 'nick', 'groups', 'is_active', 'is_staff']
        # exclude = ['msg_num', 'sysmsg_num', 'create_time', 'reg_ip', 'login_ip', 'name', 'email']