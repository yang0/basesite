# _*_coding:utf-8_*_

from .models import User
from django.contrib import admin
from .form import CreateUserForm


class UserAdmin(admin.ModelAdmin):
    list_display = ('tel', 'nick', 'create_time')
    model = User
    form = CreateUserForm
    search_fields = ['email', 'nick', 'name', 'tel']
    list_filter = ('groups__name',)
    date_hierarchy = 'create_time'


admin.site.register(User, UserAdmin)