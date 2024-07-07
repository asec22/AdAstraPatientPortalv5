from django.contrib import admin
from .models import PatientInfo,ProviderInfo,AdministratorInfo


# Register your models here.
admin.site.register(PatientInfo)
admin.site.register(ProviderInfo)
admin.site.register(AdministratorInfo)