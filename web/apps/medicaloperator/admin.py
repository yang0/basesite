from django.contrib import admin
from .models import MedicalOperator

# Register your models here.

class MedicalOperatorAdmin(admin.ModelAdmin):
    model = MedicalOperator

admin.site.register(MedicalOperator, MedicalOperatorAdmin)