from django.contrib import admin
from .models import ContactInfo,EmergencyContact,InsuranceInfo
from .models import Visit,Vitals

# Register your models here.

admin.site.register(ContactInfo)
admin.site.register(EmergencyContact)
admin.site.register(InsuranceInfo)
admin.site.register(Vitals)
admin.site.register(Visit)
